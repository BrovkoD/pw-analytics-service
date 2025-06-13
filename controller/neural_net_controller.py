from flask import Blueprint, request

from service import neural_net_service

neural_net_blueprint = Blueprint("neural_net_blueprint", __name__)


@neural_net_blueprint.route("/predict-pollinosis")
def get_neural_net():
    return neural_net_service.get_neural_net(request.args.get("freq"),
                                             request.args.get("retrain", False, bool),
                                             request.args.get("years", 10, int))
