from flask.views import MethodView
from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.app import app
from owner.utils.generics import OwnerValidation
from activity.utils.utils import ActivityActions


activity_bp = Blueprint('activity_bp', __name__, )


class UserActivity(MethodView):
    decorators = [jwt_required, ]

    def get(self):
        is_owner = OwnerValidation().is_owner_account(get_jwt_identity()['email'])
        if not is_owner:
            return jsonify({"detail": "Unauthorized user"}), 401

        id = request.args.get('id')
        format = request.args.get('format')

        if id is None:
            return jsonify({"detail": "id required"}), 400

        if format is None:
            return jsonify({"detail": "format required"}), 400

        valid_format = ActivityActions(id).check_activity_format(format)
        if not valid_format:
            return jsonify({"detail": "required formats are json/csv"}), 400

        # Get all activities of the normal user
        activities = ActivityActions(id).get_activities()
        if format == 'json':
            return jsonify(activities), 200
        if format == 'csv':
            activities = ActivityActions(id).convert_activities_csv(activities)
            return Response(activities, mimetype="text/csv", headers={"Content-disposition": "attachment; filename=activities.csv"})

        return jsonify({"detail": "Invalid format"}), 400


app.add_url_rule(
    "/api/activity/detail", view_func=UserActivity.as_view("activity-detail"), methods=["GET"]
)
