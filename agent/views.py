from flask.views import MethodView
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.app import app
from agent.utils.utils import AgentActions


agent_bp = Blueprint('agent_bp', __name__, )


class AgentList(MethodView):
    decorators = [jwt_required, ]

    def get(self):
        page = request.args.get('page')
        search = request.args.get('search')

        if page is None:
            return jsonify({"detail": "page required"}), 400

        response, data = AgentActions().get_agent_list(
            get_jwt_identity()['email'], page, search)
        if not response:
            return jsonify({'detail': data}), 400

        return jsonify(data), 200


class AgentAccount(MethodView):
    decorators = [jwt_required, ]

    def get(self):
        id = request.args.get('id')

        if id is None:
            return jsonify({"detail": "id required"}), 400

        response, data = AgentActions().get_agent_detail(
            get_jwt_identity()['email'], id)
        if not response:
            return jsonify({'detail': data}), 400

        return jsonify(data), 200

    def post(self):
        if not request.is_json:
            return jsonify({"detail": "Data is missing in request"}), 400

        name = request.json.get('name', None)
        email = request.json.get('email', None)
        phone = request.json.get('phone', None)
        company = request.json.get('company', None)
        website = request.json.get('website', None)
        address = request.json.get('address', None)
        country = request.json.get('country', None)
        state = request.json.get('state', None)
        district = request.json.get('district', None)
        city = request.json.get('city', None)
        postalcode = request.json.get('postalcode', None)
        aadhar = request.json.get('aadhar', None)

        if name is None:
            return jsonify({"detail": "name required"}), 400
        if email is None:
            return jsonify({"detail": "email required"}), 400
        if phone is None:
            return jsonify({"detail": "phone required"}), 400
        if company is None:
            return jsonify({"detail": "company required"}), 400
        if website is None:
            return jsonify({"detail": "website required"}), 400
        if address is None:
            return jsonify({"detail": "address required"}), 400
        if country is None:
            return jsonify({"detail": "country required"}), 400
        if state is None:
            return jsonify({"detail": "state required"}), 400
        if district is None:
            return jsonify({"detail": "district required"}), 400
        if city is None:
            return jsonify({"detail": "city required"}), 400
        if postalcode is None:
            return jsonify({"detail": "postalcode required"}), 400
        if aadhar is None:
            return jsonify({"detail": "aadhar required"}), 400

        response, data = AgentActions().create_agent(get_jwt_identity()['email'], name, email, phone, company, website,
                                                     address, country, state, district, city, postalcode, aadhar, app.config.get('SITE_ORIGIN'))
        if not response:
            return jsonify({'detail': data}), 401

        return jsonify(data), 200


app.add_url_rule(
    "/api/agent/list", view_func=AgentList.as_view("agent-list"), methods=["GET"]
)
app.add_url_rule(
    "/api/agent/account", view_func=AgentAccount.as_view("agent-account"), methods=["GET", "POST"]
)
