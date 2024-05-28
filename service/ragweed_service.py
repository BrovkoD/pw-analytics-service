import flask
import matplotlib.path as mplt_path
import plotly.express as px

from dao import district_dao, ragweed_dao
from dao.ragweed_dao import count_ragweed_amount_per_district, count_ragweed_size_per_district
from dto.district_border_dto import DistrictBorderDTO


def get_spread_statistics(all_locations: bool):
    define_districts()

    data = count_ragweed_amount_per_district()
    if not all_locations:
        data = data[data["district"] != "Not in Kyiv"]

    px.bar(data, x="district", y="amount", text="amount", color="amount",
           color_continuous_scale=px.colors.sequential.Oranges).show()

    resp = flask.Response(count_ragweed_amount_per_district().to_json())
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
