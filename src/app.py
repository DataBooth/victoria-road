import streamlit as st
from streamlit_folium import st_folium
from victoria_road.traffic_data import TrafficDataApp

TRANSPORT_DOC_URL = "https://opendata.transport.nsw.gov.au/dataset/ef2b0bd2-db1e-48f3-9ea1-2bb9e6bc6504/resource/13d061b1-1606-49b5-b182-d36ce0801f14/download/rms-dataset-documentation-nsw-traffic-volume-counts_0.pdf"

st.sidebar.link_button(
    label="RMS Dataset Documentation - NSW Traffic Volume Counts", url=TRANSPORT_DOC_URL
)

app = TrafficDataApp()

app.load_data()

st.sidebar.title("Traffic Data App")

station = st.sidebar.selectbox(label="Station (`full_name`)", options=["ALL"] + sorted(app.station_df["full_name"].unique()))

update_data = st.sidebar.checkbox("Update data", value=False)

if update_data:
    # app.update_data()
    pass


distance = st.sidebar.slider("Station cutoff distance (km)", min_value=2, max_value=20, value=5)




tab_stats, tab_plots, tab_data, tab_schema, tab_map = st.tabs(
    ["Stats", "Plots", "Data", "Schema", "Map"]
)

with tab_stats:
    st.write(app.get_stats())

with tab_plots:
    hour = st.sidebar.slider("Select Hour", 0, 23, 0, format="%02d")
    st.write(app.plot_data(hour))

with tab_data:
    st.write(app.counts_df.size)
    st.dataframe(app.counts_df)

with tab_schema:
    app.get_schema()

with tab_map:
    folium_map = app.create_map(station, distance)
    st_folium(folium_map, width=725, height=500)
