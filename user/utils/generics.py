import os
import base64
import threading
from datetime import datetime

from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import check_password_hash, generate_password_hash

from user.models import User, Role

from core.sendemail import SendEmail
from core.cryptograph import CryptoGraphs
from user.models import PasswordResetToken
from core.fileprocess import get_profile_thumbnail_dir


class UserValidation:
    def generate_tokens(self, user):
        jwt_content = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
        }

        tokens = {
            'access_token': create_access_token(identity=jwt_content),
            'refresh_token': create_refresh_token(identity=jwt_content),
        }

        return tokens

    def check_email_exist(self, email):
        user = User.query.filter_by(email=email).first()
        if user is None:
            return False, "User account does not exist"
        return True, user

    def check_email_password(self, email, password):
        response, user = self.check_email_exist(email)
        if not response:
            return response, user
        if not check_password_hash(user.password, password):
            return False, "Incorrect password"
        return True, user

    def check_active(self, user):
        if user.is_deleted:
            return False, "Deleted account"
        if not user.is_active:
            return False, "User account is not active"
        return True, user

    def get_icon(self, media_root, user_id):
        icon = None
        icon_dir = get_profile_thumbnail_dir(media_root, user_id)
        if os.path.isdir(icon_dir):
            icon_file = os.path.join(icon_dir, f"{user_id}.png")
            if os.path.isfile(icon_file):
                with open(icon_file, "rb") as image_file:
                    icon = base64.b64encode(image_file.read()).decode('utf-8')
        return icon

    def get_user_role(self, user_id):
        role = Role.query.filter_by(user_id=user_id).first()
        return None if role is None else role.name

    def verify_passwords(self, password1, password2):
        if password1 != password2:
            return False, "Mismatched passwords"
        if len(password1) < 8:
            return False, "Password must contain 8 characters"
        if len(password1) > 20:
            return False, "Password must not exceed 20 characters"
        return True, password1

    def verify_name(self, name):
        if len(name) < 3:
            return False, "Name must be contain 3 characters"
        if len(name) > 20:
            return False, "Only 20 characters are allowed for name field"
        if not name.replace(' ', '').isalpha():
            return False, "Only alphabhets are allowed as name."
        return True, "Success"

    def check_link_validity(self, key, need_time_check=True):
        data_list = CryptoGraphs().crypto_decrypt_msg(key).split('||')
        if len(data_list) != 3:
            return False, "Activation link is invalid"

        email = data_list[1]
        date_string = data_list[2]

        response, user = self.check_email_exist(email)
        if not response:
            return response, user

        if need_time_check:
            url_generated_time = datetime.strptime(
                date_string, "%Y-%m-%d %H:%M:%S.%f")

            time_difference = datetime.now() - url_generated_time
            minutes_difference = time_difference.seconds / 60
            if minutes_difference > 15:
                return False, "Your account password reset link expired"

            response, user = self.check_active(user)
            if not response:
                return response, user

        # Check the key is valid or not
        reset_token = PasswordResetToken.query.filter_by(
            user_id=user.id, is_active=True, token=key).first()
        if reset_token is None:
            return False, "Activation link is invalid or expired"

        return True, [reset_token, user]

    def initiate_password_reset_mail(self, user_id, email, user_name, site_origin):
        message = f"{user_id}||{email}||{datetime.now()}"
        key = CryptoGraphs().crypto_encrypt_msg(message)
        pwd_reset_link = f"{site_origin}/change-password?auth={key}"

        # Send password to the user via email
        t = threading.Thread(target=SendEmail().pwd_reset_email, args=[
                             email, user_name, pwd_reset_link])
        t.start()

        return key

    def initiate_activation_mail(self, user_id, email, user_name, site_origin):
        message = f"{user_id}||{email}||{datetime.now()}"
        key = CryptoGraphs().crypto_encrypt_msg(message)
        pwd_reset_link = f"{site_origin}/activate-account?auth={key}"

        # Send password to the user via email
        t = threading.Thread(target=SendEmail().activate_account_email, args=[
                             email, user_name, pwd_reset_link])
        t.start()

        return key

    def get_set_reset_token(self, user_id, key):
        flag = True
        reset_token = PasswordResetToken.query.filter_by(
            user_id=user_id).first()
        if reset_token is None:
            flag = False
            reset_token = PasswordResetToken(user_id=user_id)

        reset_token.is_active = True
        reset_token.token = key
        reset_token.created_at = datetime.utcnow()

        return flag, reset_token

    def get_hash_from_password(self, password):
        return generate_password_hash(password, method='sha256')

    def verify_email(self, email):
        if len(email) < 7:
            return False, "Invalid email address"
        email_split = email.split('@')
        if len(email_split) != 2:
            return False, "Invalid email address"
        if '.' not in email_split[1]:
            return False, "Invalid email address"
        extension = email_split[1].split('.')
        if not extension[-1].isalpha():
            return False, "Invalid email address"
        return True, "Success"

    def get_user_from_id(self, id):
        return User.query.filter_by(id=id).first()
