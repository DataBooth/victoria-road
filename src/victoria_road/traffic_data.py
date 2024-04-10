import os
import re
from datetime import datetime, timedelta
from functools import cache
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

import duckdb
import folium
import httpx
import pandas as pd
import plotly.graph_objs as go
import streamlit as st
from haversine import haversine
from loguru import logger

DOWNLOAD_THRESHOLD_DAYS = 2

TABLE_NAME_COUNTS = "road_traffic_counts"
TABLE_NAME_STATIONS = "station_reference"

CSV_FILES_PATH = "data/road_traffic_counts_hourly_permanent/"

HOURLY_COUNTS_ZIP = "https://opendata.transport.nsw.gov.au/dataset/ef2b0bd2-db1e-48f3-9ea1-2bb9e6bc6504/resource/bca06c7e-30be-4a90-bc8b-c67428c0823a/download/road_traffic_counts_hourly_permanent.zip"
STATION_REFERENCE = "https://opendata.transport.nsw.gov.au/dataset/ef2b0bd2-db1e-48f3-9ea1-2bb9e6bc6504/resource/c65ad7b4-0257-4cc6-953e-5299ac8d27ba/download/road_traffic_counts_station_reference.csv"


# def find_integer_in_filename(filename):
#     match = re.search(r'\d+', filename)
#     return int(match.group()) if match else None


class TrafficDataApp:
    def __init__(
        self, user_latitude=-33.8511, user_longitude=151.1545, data_dir=CSV_FILES_PATH, n_csv_history=1
    ):
        self.n_csv_history = max(n_csv_history, 1)
        self.data_dir = Path(data_dir)
        self.station_df = None
        self.counts_df = None
        self.csv_data = None
        self.con = duckdb.connect()
        self.user_location = (user_latitude, user_longitude)

    def download_and_extract_zip(self, zip_url, extract_to):
        """Download and extract a ZIP file."""
        with httpx.Client() as client:
            response = client.get(zip_url)
        with ZipFile(BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(extract_to)

    def update_data(self, force_update=False):
        """Update data if older than 2 days or forced."""
        need_update = force_update
        if not need_update:
            # Check if update is needed based on file modification times
            try:
                first_file = next(self.data_dir.glob("*"))
                file_mod_time = datetime.fromtimestamp(os.path.getmtime(first_file))
                if datetime.now() - file_mod_time > timedelta(days=2):
                    need_update = True
            except StopIteration:
                need_update = True  # Directory is empty, need to download

        if need_update:
            hourly_counts_zip_url = HOURLY_COUNTS_ZIP
            station_reference_url = STATION_REFERENCE
            self.download_and_extract_zip(hourly_counts_zip_url, self.data_dir)
            # Assuming station reference is a single CSV file
            self.download_and_extract_zip(station_reference_url, self.data_dir / "station_reference.csv")
            st.success("Data updated successfully.")

    def get_csv_data_files(self):
        # Ensure the data directory exists
        if not self.data_dir.exists():
            print(f"Data directory {self.data_dir} does not exist.")
            return []
        csv_files = [path.as_posix() for path in self.data_dir.glob("*.csv")]
        # Check if the list is empty
        if not csv_files:
            print("No CSV files found in the data directory.")
            return []
        return csv_files[-self.n_csv_history :]

    @cache
    def load_data(self):
        self.csv_data = self.get_csv_data_files()
        logger.info(f"{len(self.csv_data)} CSV files loaded: {self.csv_data}")
        # Stations
        self.con.execute(
            f"CREATE TABLE {TABLE_NAME_STATIONS} AS SELECT * FROM read_csv_auto('{STATION_REFERENCE}')"
        )
        logger.info(
            f"CREATE TABLE {TABLE_NAME_STATIONS} AS SELECT * FROM read_csv_auto('{STATION_REFERENCE}')"
        )
        self.station_df = self.con.sql(f"SELECT * FROM {TABLE_NAME_STATIONS}").to_df()

        # Traffic counts
        # Assume the first file defines the table structure
        self.con.execute(
            f"CREATE TABLE {TABLE_NAME_COUNTS} AS SELECT * FROM read_csv_auto('{self.csv_data[0]}')"
        )
        logger.info(
            f"CREATE TABLE {TABLE_NAME_COUNTS} AS SELECT * FROM read_csv_auto('{self.csv_data[0]}')"
        )
        # For each subsequent file, insert the data into the existing table
        for csv_file in self.csv_data[1:]:
            self.con.execute(
                f"INSERT INTO {TABLE_NAME_COUNTS} SELECT * FROM read_csv_auto('{csv_file}')"
            )
            logger.info(f"INSERT INTO {TABLE_NAME_COUNTS} SELECT * FROM read_csv_auto('{csv_file}')")
        self.counts_df = self.con.sql(f"SELECT * FROM {TABLE_NAME_COUNTS}").to_df()

    def calc_distances_to_stations(self):
        dmap = {"latitude": "wgs84_latitude", "longitude": "wgs84_longitude"}
        self.station_df["distance_to_user"] = self.station_df.apply(
            lambda row: haversine(self.user_location, (row[dmap["latitude"]], row[dmap["longitude"]])),
            axis=1,
        )

    def get_stats(self):
        counts_stats = pd.DataFrame(self.counts_df.describe())
        counts_stats_all = pd.DataFrame(self.counts_df.describe(include="all"))

    def get_schema(self):
        """Return schema information for the datasets."""
        # Placeholder: Implement retrieval of schema information for self.station_df and self.counts_df
        return "Schema not implemented yet."

    def plot_data(self, hour):
        """Generate and return plots for the specified hour."""
        # Placeholder: Implement plotting logic based on the selected hour
        return "Plotting not implemented yet."

    @cache
    def create_map(self, station, distance=10):
        # Assuming df has 'wgs84_latitude', 'wgs84_longitude', 'station_id', 'station_key', and 'full_name' columns
        self.calc_distances_to_stations()
        m = folium.Map()
        fg = folium.FeatureGroup()  # Create a feature group
        station_df = self.station_df.copy()
        if station != "ALL":
            station_df = station_df[station_df["full_name"] == station]
        for row in station_df[station_df["distance_to_user"] <= distance].itertuples():
            popup_text = (
                f"Station ID (Key): {row.station_id} ({row.station_key})<br>Full Name: {row.road_name}"
            )
            marker = folium.Marker(
                [row.wgs84_latitude, row.wgs84_longitude],
                popup=folium.Popup(popup_text, max_width=450),
            )
            fg.add_child(marker)
        m.add_child(fg)
        m.fit_bounds(fg.get_bounds())
        return m
