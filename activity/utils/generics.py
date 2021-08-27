from app.app import db
from activity.models import Activity
from config.activity import ACTIVITIES, ACTIVITY_FORMATS


class ActivityFunctions:
    def check_activity_format(self, fmt):
        if fmt not in ACTIVITY_FORMATS:
            return False
        return True

    def get_activity_description(self, action, params):
        description = ACTIVITIES[action]
        for param in params:
            description = description.replace("##value##", str(param), 1)
        return description

    def save_activity(self, user_id, action, params=[]):
        description = self.get_activity_description(action, params)

        activity = Activity(user_id=user_id, name=action,
                            description=description)
        db.session.add(activity)
        db.session.commit()

    def retrieve_activity_from_db(self, user_id):
        data = []
        activities = Activity.query.filter_by(
            user_id=user_id).order_by(Activity.created_at.desc()).limit(500).all()
        for activity in activities:
            context = {
                "description": activity.description,
                "time": activity.created_at,
            }
            data.append(context)

        return data
