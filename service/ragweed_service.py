import flask
import matplotlib.path as mplt_path
import pandas as pd
import plotly.express as px
import json

with open("resources/kyiv_districts.geojson", 'r') as file:
    counties = json.load(file)

from dao import district_dao, ragweed_dao
from dao.ragweed_dao import count_ragweed_amount_per_district, count_ragweed_size_per_district, find_all
from dto.district_border_dto import DistrictBorderDTO


def get_spread_statistics(all_locations: bool):
    define_districts()

    data = count_ragweed_amount_per_district()
    kyiv_districts = data[data["territory"] != "other regions"]

    if not all_locations:
        data = kyiv_districts
        data = data.rename(columns={"territory": "district"})
        px.bar(data, x="district", y="amount", text="amount", color="amount",
               color_continuous_scale=px.colors.sequential.Oranges).show()

        fig = px.choropleth_mapbox(data, geojson=counties, locations='id', color='amount',
                                   color_continuous_scale=px.colors.sequential.Oranges,
                                   mapbox_style="carto-positron",
                                   zoom=8.5, center={"lat": 50.4500, "lon": 30.5245},
                                   opacity=0.7)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.show()
    else:
        kyiv_spread_sum = pd.DataFrame([["Kyiv", kyiv_districts.sum(numeric_only=True)["amount"]]], columns=[
            "territory", "amount"])
        data = pd.concat([kyiv_spread_sum, data[data["territory"] == "other regions"]])
        fig = px.bar(data, x="territory", y="amount", text="amount", color="amount", color_continuous_scale=px.colors
                     .sequential.Oranges)
        fig.update_layout(
            bargap=0.8
        )
        fig.show()

        map_df = find_all()
        map_df["size"] = map_df["size"].replace({"1-2 unit(s)": 1, "3-10 units": 2, "11-50 units": 3, ">50 units": 4})
        fig = px.scatter_geo(map_df, lat="latitude", lon="longitude", color="size", color_continuous_scale=px.colors
                             .sequential.Oranges, color_continuous_midpoint=1, size="size", projection="natural earth")

        fig.update_layout(
            geo=dict(
                showland=True,
                landcolor="rgb(217, 217, 217)",
                subunitcolor="rgb(255, 255, 255)",
                countrycolor="rgb(255, 255, 255)",
                showlakes=True,
                lakecolor="rgb(255, 255, 255)",
                showsubunits=True,
                showcountries=True,
                # resolution=50
            )
        )

        for trace in fig.data:
            if trace.name == 1:
                trace.name = "1-2 unit(s)"
            elif trace.name == 2:
                trace.name = "3-10 units"
            elif trace.name == 3:
                trace.name = "11-50 units"
            elif trace.name == 4:
                trace.name = ">50 units"

        fig.show()

    resp = flask.Response(data.to_json())
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp


def get_size_statistics():
    px.sunburst(count_ragweed_size_per_district(), path=['district', 'size'], values='amount').show()
    resp = flask.Response(count_ragweed_size_per_district().to_json())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


def define_districts():
    unmarked_ragweed = ragweed_dao.find_where_district_is_null()
    if len(unmarked_ragweed) == 0:
        return "No data"

    district_borders = []
    for district in district_dao.find_all():
        district_borders.append(DistrictBorderDTO(district, district_dao.find_by_district_id(district.id)))

    for ragweed in unmarked_ragweed:
        define_district(district_borders, ragweed)

    return "Success"


def define_district(_district_borders, _ragweed):
    marked = False

    for district_border in _district_borders:
        path = mplt_path.Path(district_border.border)
        if path.contains_points([[_ragweed.latitude, _ragweed.longitude]]):
            _ragweed.district_id = district_border.district.id
            ragweed_dao.update(_ragweed)
            marked = True
            break

    if not marked:
        _ragweed.district_id = 0
        ragweed_dao.update(_ragweed)
