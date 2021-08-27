from flask.views import MethodView
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequestKeyError
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.app import app
from profile.utils.utils import ProfileActions


profile_bp = Blueprint('profile_bp', __name__, )


class ProfileDetail(MethodView):
    decorators = [jwt_required, ]

    def get(self):
        response, message = ProfileActions().get_profile_detail(
            get_jwt_identity()['email'], app.config.get('MEDIA_ROOT'))
        if not response:
            return jsonify({"detail": message}), 400

        return jsonify(message), 200

    def put(self):
        if not request.is_json:
            return jsonify({"detail": "Data is missing in request"}), 400

        name = request.json.get('name', None)
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

        response, message = ProfileActions().update_detail(get_jwt_identity(
        )['email'], name, phone, company, website, address, country, state, district, city, postalcode, aadhar)
        if not response:
            return jsonify({"detail": message}), 400

        return jsonify(message), 200


class ProfilePicture(MethodView):
    decorators = [jwt_required, ]

    def post(self):
        try:
            file = request.files['file']
        except BadRequestKeyError:
            return jsonify({"detail": "file is missing in request"}), 400

        response, message = ProfileActions().upload_profile_pic(
            get_jwt_identity()['email'], file, app.config.get('MEDIA_ROOT'))
        if not response:
            return jsonify({"detail": message}), 400

        return jsonify({"detail": message}), 200


class ChangePassword(MethodView):
    decorators = [jwt_required, ]

    def put(self):
        if not request.is_json:
            return jsonify({"detail": "Data is missing in request"}), 400

        password1 = request.json.get('password1', None)
        password2 = request.json.get('password2', None)
        passwordold = request.json.get('passwordold', None)

        if password1 is None:
            return jsonify({"detail": "password1 required"}), 400
        if password2 is None:
            return jsonify({"detail": "password2 required"}), 400
        if passwordold is None:
            return jsonify({"detail": "passwordold required"}), 400

        response, message = ProfileActions().change_password(
            get_jwt_identity()['email'], password1, password2, passwordold)
        if not response:
            return jsonify({"detail": message}), 400

        return jsonify({"detail": message}), 200


app.add_url_rule(
    "/api/profile/detail", view_func=ProfileDetail.as_view("profile-detail"), methods=["GET", "PUT"]
)
app.add_url_rule(
    "/api/profile/picture", view_func=ProfilePicture.as_view("profile-picture"), methods=["POST"]
)
app.add_url_rule(
    "/api/profile/change-passsword", view_func=ChangePassword.as_view("change-password"), methods=["PUT"]
)
