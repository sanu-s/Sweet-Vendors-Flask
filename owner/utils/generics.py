import math

from config.user import USER_ROLES
from user.models import User, Role
from config.owner import OWNER_PAGE_COUNT


class OwnerValidation:
    def is_owner_account(self, email):
        user = User.query.filter_by(email=email, is_admin=True).first()
        if user is None:
            return False
        role = Role.query.filter_by(
            user_id=user.id, name=USER_ROLES['owner']['name']).first()
        if role is None:
            return False
        return True

    def get_owner_page_count(self, role_queryset):
        return math.ceil(len(role_queryset) / OWNER_PAGE_COUNT)

    def get_all_owners(self, page, search):
        end_limit = page * OWNER_PAGE_COUNT
        start_limit = end_limit - OWNER_PAGE_COUNT

        role_queryset = Role.query.filter_by(
            name=USER_ROLES['owner']['name']).all()

        page_count = self.get_owner_page_count(role_queryset)

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
