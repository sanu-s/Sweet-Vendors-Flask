import math

from config.user import USER_ROLES
from user.models import User, Role
from config.agent import AGENT_PAGE_COUNT


class AgentValidation:
    def is_agent_account(self, email):
        user = User.query.filter_by(email=email, is_admin=True).first()
        if user is None:
            return False
        role = Role.query.filter_by(
            user_id=user.id, name=USER_ROLES['agent']['name']).first()
        if role is None:
            return False
        return True

    def get_agent_page_count(self, role_queryset):
        return math.ceil(len(role_queryset) / AGENT_PAGE_COUNT)

    def get_all_agents(self, page, search):
        end_limit = page * AGENT_PAGE_COUNT
        start_limit = end_limit - AGENT_PAGE_COUNT

        role_queryset = Role.query.filter_by(
            name=USER_ROLES['agent']['name']).all()

        page_count = self.get_agent_page_count(role_queryset)

        roles = role_queryset[start_limit:end_limit]

        user_list = []
        for role in roles:
            user = User.query.filter_by(id=role.user_id).first()
            context = {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "is_active": user.is_active,
                "created_at": user.created_at,
            }

            user_list.append(context)

        return user_list, page_count
