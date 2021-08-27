from flask.views import MethodView
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.app import app
from ticket.utils.utils import TicketActions


ticket_bp = Blueprint('ticket_bp', __name__, )


class TicketList(MethodView):
    decorators = [jwt_required, ]

    def get(self):
        page = request.args.get('page')
        user_type = request.args.get('user_type')

        if page is None:
            return jsonify({"detail": "page required"}), 400
        if user_type is None:
            return jsonify({"detail": "user_type required"}), 400

        response, data = TicketActions().get_ticket_list(
            get_jwt_identity()['email'], page, user_type)
        if not response:
            return jsonify({'detail': data}), 400

        return jsonify(data), 200


class TicketDetail(MethodView):
    decorators = [jwt_required, ]

    def get(self):
        id = request.args.get('id')

        if id is None:
            return jsonify({"detail": "id required"}), 400

        response, data = TicketActions().get_ticket_detail(
            get_jwt_identity()['email'], id)
        if not response:
            return jsonify({'detail': data}), 400

        return jsonify(data), 200

    def put(self):
        if not request.is_json:
            return jsonify({"detail": "Data is missing in request"}), 400

        id = request.json.get('id', None)
        action = request.json.get('action', None)

        if id is None:
            return jsonify({"detail": "id required"}), 400
        if action is None:
            return jsonify({"detail": "action required"}), 400

        response, data = TicketActions().ticket_action(
            get_jwt_identity()['email'], id, action, app.config.get('SITE_ORIGIN'))
        if not response:
            return jsonify({'detail': data}), 400

        return jsonify(data), 200


app.add_url_rule(
    "/api/ticket/list", view_func=TicketList.as_view("ticket-list"), methods=["GET"]
)
app.add_url_rule(
    "/api/ticket/detail", view_func=TicketDetail.as_view("ticket-detail"), methods=["GET", "PUT"]
)
