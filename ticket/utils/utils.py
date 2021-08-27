from app.app import db
from profile.utils.utils import ProfileActions
from owner.utils.generics import OwnerValidation
from ticket.utils.generics import TicketValidation
from activity.utils.generics import ActivityFunctions


class TicketActions(ProfileActions, TicketValidation, OwnerValidation):
    def get_ticket_detail(self, email, id):
        is_owner = self.is_owner_account(email)
        if not is_owner:
            return is_owner, "Unauthorized user"

        response, user = self.check_email_exist(email)
        if not response:
            return response, user
        response, user = self.check_active(user)
        if not response:
            return response, user

        profile_info = self.get_profile_info(id)
        return True, profile_info

    def get_ticket_list(self, email, page, user_type):
        try:
            page = int(page)
        except (KeyError, ValueError):
            return False, "Invalid page value"

        is_owner = self.is_owner_account(email)
        if not is_owner:
            return is_owner, "Unauthorized user"

        response, user = self.check_email_exist(email)
        if not response:
            return response, user
        response, user = self.check_active(user)
        if not response:
            return response, user

        response = self.check_ticket_user(user_type)
        if not response:
            return response, "Invalid user_type"

        ticket_list, page_count = self.get_all_tickets(page, user_type)
        context = {
            "ticket_list": ticket_list,
            "page": page,
            "page_count": page_count,
        }

        # Save Activity
        ActivityFunctions().save_activity(
            user.id, "ticket_list_view", [user_type, page])

        return True, context

    def ticket_action(self, email, id, action, site_origin):
        response, user = self.check_email_exist(email)
        if not response:
            return response, user
        response, user = self.check_active(user)
        if not response:
            return response, user

        response = self.is_ticket_action_valid(action)
        if not response:
            return response, "Invalid action"

        ticket = self.get_ticket_query(id)
        if ticket is None:
            return False, "Ticket not found"

        new_user = self.get_user_from_id(id)
        if new_user is None:
            return False, "User not found"

        role_name = self.get_user_role(id)
        if role_name is None:
            return False, "User role not found"

        # Send email to set password
        key = self.initiate_activation_mail(
            new_user.id, email, new_user.name, site_origin)

        # Check for previous user_id in PasswordResetToken
        flag, password_reset_token = self.get_set_reset_token(new_user.id, key)
        if not flag:
            db.session.add(password_reset_token)

        db.session.commit()

        ticket.status = self.get_action_status(action)
        db.session.commit()

        # Save Activity
        ActivityFunctions().save_activity(user.id, "ticket_action", [
            role_name, new_user.email, action, email])

        return True, "Ticket action success"
