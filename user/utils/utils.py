from app.app import db
from user.utils.generics import UserValidation
from activity.utils.generics import ActivityFunctions


class UserActions(UserValidation):
    def login_user(self, email, password):
        flag, user = self.check_email_password(email, password)
        if not flag:
            return flag, user
        flag, user = self.check_active(user)
        if not flag:
            return flag, user

        tokens = self.generate_tokens(user)

        # Save Activity
        ActivityFunctions().save_activity(user.id, "login")

        return True, tokens

    def login_refresh(self, email):
        response, user = self.check_email_exist(email)
        if not response:
            return response, user
        response, user = self.check_active(user)
        if not response:
            return response, user

        tokens = self.generate_tokens(user)

        return True, tokens

    def logout_user(self, email):
        response, user = self.check_email_exist(email)
        if not response:
            return response, user
        response, user = self.check_active(user)
        if not response:
            return response, user

        # Save Activity
        ActivityFunctions().save_activity(user.id, "logout")

        return True, "Logout success"

    def get_user_detail(self, email, media_root):
        response, user = self.check_email_exist(email)
        if not response:
            return response, user
        response, user = self.check_active(user)
        if not response:
            return response, user

        details = {
            "name": user.name,
            "email": user.email,
            "admin_type": self.get_user_role(user.id) if user.is_admin else None,
            "icon": self.get_icon(media_root, user.id),
        }

        return True, details

    def send_password_reset_email(self, email, site_origin):
        response, user = self.check_email_exist(email)
        if not response:
            return response, user

        response, user = self.check_active(user)
        if not response:
            return response, user

        key = self.initiate_password_reset_mail(
            user.id, email, user.name, site_origin)

        # Check for previous user_id in PasswordResetToken
        flag, password_reset_token = self.get_set_reset_token(user.id, key)
        if not flag:
            db.session.add(password_reset_token)

        db.session.commit()

        # Save Activity
        ActivityFunctions().save_activity(user.id, "reset_password_email")

        return True, "Password reset email has been sent"

    def reset_password_from_link(self, key, password1, password2):
        key = str(key).strip()
        password1 = str(password1).strip()
        password2 = str(password2).strip()

        response, password = self.verify_passwords(password1, password2)
        if not response:
            return response, password

        response, message = self.check_link_validity(key)
        if not response:
            return response, message

        reset_token = message[0]
        user = message[1]

        reset_token.is_active = False
        db.session.commit()

        user.password = self.get_hash_from_password(password)
        db.session.commit()

        # Save Activity
        ActivityFunctions().save_activity(user.id, "reset_password_done")

        return True, "Password reset success"

    def activate_user_from_link(self, key, password1, password2):
        key = str(key).strip()
        password1 = str(password1).strip()
        password2 = str(password2).strip()

        response, password = self.verify_passwords(password1, password2)
        if not response:
            return response, password

        response, message = self.check_link_validity(
            key, need_time_check=False)
        if not response:
            return response, message

        reset_token = message[0]
        user = message[1]

        reset_token.is_active = False
        db.session.commit()

        user.password = self.get_hash_from_password(password)
        user.is_active = True
        db.session.commit()

        # Save Activity
        ActivityFunctions().save_activity(user.id, "activate_account")

        return True, "Account activation success"
