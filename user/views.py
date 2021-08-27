from flask.views import MethodView
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, get_jwt_identity

from app.app import app
from user.utils.utils import UserActions


user_bp = Blueprint('user_bp', __name__, )


class UserLogin(MethodView):
    def post(self):
        if not request.is_json:
            return jsonify({"detail": "Data is missing in request"}), 400

        email = request.json.get('email', None)
        password = request.json.get('password', None)
        if email is None:
            return jsonify({"detail": "email required"}), 400
        if password is None:
            return jsonify({"detail": "password required"}), 400

        response, data = UserActions().login_user(email, password)
        if not response:
            return jsonify({'detail': data}), 401

        return jsonify(data), 200


class UserRefresh(MethodView):
    decorators = [jwt_refresh_token_required, ]

    def post(self):
        response, data = UserActions().login_refresh(
            get_jwt_identity()['email'])
        if not response:
            return jsonify({'detail': data}), 401

        return jsonify(data), 200


class UserLogout(MethodView):
    decorators = [jwt_required, ]

    def delete(self):
        response, data = UserActions().logout_user(get_jwt_identity()['email'])

        if not response:
            return jsonify({'detail': data}), 401

        return jsonify({'detail': data}), 200


class UserDetail(MethodView):
    decorators = [jwt_required, ]

    def get(self):
        response, message = UserActions().get_user_detail(
            get_jwt_identity()['email'], app.config.get('MEDIA_ROOT'))
        if not response:
            return jsonify({"detail": message}), 400

        return jsonify(message), 200


class ResetPassword(MethodView):
    def get(self):
        key = request.args.get('key')

        if key is None:
            return jsonify({"detail": "key required"}), 400

        response, message = UserActions().check_link_validity(key)
        if not response:
            return jsonify({"detail": message}), 400

        return jsonify({"detail": "Link is valid"}), 200

    def post(self):
        if not request.is_json:
            return jsonify({"detail": "Data is missing in request"}), 400

        email = request.json.get('email', None)

        if email is None:
            return jsonify({"detail": "email required"}), 400

        response, message = UserActions().send_password_reset_email(
            email, app.config.get('SITE_ORIGIN'))
        if not response:
            return jsonify({"detail": message}), 400

        return jsonify({"detail": message}), 200

    def put(self):
        if not request.is_json:
            return jsonify({"detail": "Data is missing in request"}), 400

        key = request.json.get('key', None)
        password1 = request.json.get('password1', None)
        password2 = request.json.get('password2', None)

        if key is None:
            return jsonify({"detail": "key required"}), 400
        if password1 is None:
            return jsonify({"detail": "password1 required"}), 400
        if password2 is None:
            return jsonify({"detail": "password2 required"}), 400

        response, message = UserActions().reset_password_from_link(key, password1, password2)
        if not response:
            return jsonify({"detail": message}), 400

        return jsonify({"detail": message}), 200


class UserActivate(MethodView):
    def put(self):
        if not request.is_json:
            return jsonify({"detail": "Data is missing in request"}), 400

        key = request.json.get('key', None)
        password1 = request.json.get('password1', None)
        password2 = request.json.get('password2', None)

        if key is None:
            return jsonify({"detail": "key required"}), 400
        if password1 is None:
            return jsonify({"detail": "password1 required"}), 400
        if password2 is None:
            return jsonify({"detail": "password2 required"}), 400

        response, message = UserActions().activate_user_from_link(key, password1, password2)
        if not response:
            return jsonify({"detail": message}), 400

        return jsonify({"detail": message}), 200


app.add_url_rule(
    "/api/user/login", view_func=UserLogin.as_view("user-login"), methods=["POST"]
)
app.add_url_rule(
    "/api/user/refresh", view_func=UserRefresh.as_view("user-refresh"), methods=["POST"]
)
app.add_url_rule(
    "/api/user/logout", view_func=UserLogout.as_view("user-logout"), methods=["DELETE"]
)
app.add_url_rule(
    "/api/user/detail", view_func=UserDetail.as_view("user-detail"), methods=["GET"]
)
app.add_url_rule(
    "/api/user/reset-password", view_func=ResetPassword.as_view("reset-password"), methods=["GET", "POST", "PUT"]
)
app.add_url_rule(
    "/api/user/activate", view_func=UserActivate.as_view("user-activate"), methods=["PUT"]
)
