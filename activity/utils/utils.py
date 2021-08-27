import pandas as pd

from activity.utils.generics import ActivityFunctions


class ActivityActions(ActivityFunctions):
    def __init__(self, user_id):
        self.user_id = user_id

    def get_activities(self):
        activities = self.retrieve_activity_from_db(self.user_id)
        return activities

    def convert_activities_csv(self, activities):
        df = pd.DataFrame(activities)
        df.columns = ['Activity', 'Time']
        return df.to_csv(index=False)
