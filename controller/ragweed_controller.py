from flask import Blueprint

from service import ragweed_service

ragweed_blueprint = Blueprint("ragweed_blueprint", __name__, url_prefix="/ragweed")


@ragweed_blueprint.route("/statistics/spread")
def get_spread_statistics():
    return ragweed_service.get_spread_statistics()


@ragweed_blueprint.route("/statistics/size")
def get_size_statistics():
    return ragweed_service.get_size_statistics()


@ragweed_blueprint.route("/define-districts")
def define_districts():
    return ragweed_service.define_districts()
