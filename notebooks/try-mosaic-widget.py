import marimo

__generated_with = "0.3.3"
app = marimo.App()


@app.cell
def __():
    import pandas as pd
    import yaml
    from mosaic_widget import MosaicWidget
    import requests
    import yaml
    return MosaicWidget, pd, requests, yaml


@app.cell
def __(pd):
    weather = pd.read_csv("https://uwdata.github.io/mosaic-datasets/data/seattle-weather.csv", parse_dates=['date'])
    return weather,


@app.cell
def __(weather):
    weather.head()
    return


@app.cell
def __(requests, yaml):
    url = "https://raw.githubusercontent.com/uwdata/mosaic/main/specs/yaml/weather.yaml"
    response = requests.get(url)

    if response.status_code == 200:
        spec = yaml.safe_load(response.content)
        spec.pop("data")
    else:
        print("Failed to fetch the YAML file")
    return response, spec, url


@app.cell
def __(MosaicWidget, spec, weather):
    MosaicWidget(spec, data = {"weather": weather})
    return


@app.cell
def __(spec):
    spec
    return


if __name__ == "__main__":
    app.run()
