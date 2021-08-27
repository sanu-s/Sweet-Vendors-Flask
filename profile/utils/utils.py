import os

from PIL import Image
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

from app.app import db
from user.utils.generics import UserValidation
from profile.utils.generics import ProfileValidation
from activity.utils.generics import ActivityFunctions
from core.fileprocess import create_dir, get_profile_picture_dir, get_profile_thumbnail_dir


class ProfileActions(UserValidation, ProfileValidation):
    def get_profile_detail(self, email, media_root):
        response, user = self.check_email_exist(email)
        if not response:
            return response, user
        response, user = self.check_active(user)
        if not response:
            return response, user

        admin_type = self.get_user_role(user.id) if user.is_admin else None
        profile_info = self.get_profile_info(user.id)

        details = {
            "name": user.name,
            "email": user.email,
            "admin_type": admin_type,
            "icon": self.get_icon(media_root, user.id),
        }

        details.update(profile_info)

        # Save activity
        ActivityFunctions().save_activity(user.id, "view_profile")

        return True, details

    def update_detail(self, req_email, name, phone, company, website, address, country, state, district, city, postalcode, aadhar):
        response, user = self.check_email_exist(req_email)
        if not response:
            return response, user
        response, user = self.check_active(user)
        if not response:
            return response, user

        name = str(name)
        phone = str(phone)
        company = str(company)
        website = str(website)
        address = str(address)
        country = str(country)
        state = str(state)
        district = str(district)
        city = str(city)
        postalcode = str(postalcode)
        aadhar = str(aadhar)

        response, message = self.verify_name(name)
        if not response:
            return response, message

        response, message = self.verify_phone(phone)
        if not response:
            return response, message

        response, message = self.verify_company(company)
        if not response:
            return response, message

        response, message = self.verify_website(website)
        if not response:
            return response, message

        response, message = self.verify_address(address)
        if not response:
            return response, message

        response, message = self.verify_country_state_district(
            country, state, district)
        if not response:
            return response, message

        response, message = self.verify_city(city)
        if not response:
            return response, message

        response, message = self.verify_postalcode(postalcode)
        if not response:
            return response, message

        response, message = self.verify_aadhar(aadhar)
        if not response:
            return response, message

        # Check for existing profile with same phone number
        response = self.is_profile_exists(phone, user.id)
        if response:
            return False, "Profile already exist with this phone number"

        user.name = name
        db.session.commit()

        profile = self.get_profile_table(user.id)
        profile.phone = phone
        profile.company = company
        profile.website = website
        profile.address = address
        profile.country = country
        profile.state = state
        profile.district = district
        profile.city = city
        profile.postalcode = postalcode
        profile.aadhar = aadhar
        db.session.commit()

        details = {
            "name": user.name,
            "phone": phone,
            "company": company,
            "website": website,
            "address": address,
            "country": country,
            "state": state,
            "district": district,
            "city": city,
            "postalcode": postalcode,
            "aadhar": aadhar,
        }

        # Save Activity
        ActivityFunctions().save_activity(user.id, "edit_profile")

        return True, details

    def upload_profile_pic(self, email, file, media_root):
        response, user = self.check_email_exist(email)
        if not response:
            return response, user
        response, user = self.check_active(user)
        if not response:
            return response, user

        file_name = file.filename
        if not self.allowed_profile_pics(file_name):
            return False, "File format is not supported"

        dir_name = get_profile_picture_dir(media_root, user.id)
        create_dir(dir_name)
        thumb_dir = get_profile_thumbnail_dir(media_root, user.id)
        create_dir(thumb_dir)

        file_full_name = os.path.join(dir_name, secure_filename(file_name))
        thumbnail_file = os.path.join(thumb_dir, f"{user.id}.png")

        # Save original file
        file.save(file_full_name)

        # Get file-size and convert to MB
        file_size = os.stat(file_full_name).st_size
        file_size_mb = file_size * (10 ** -6)
        if file_size_mb > 4:
            return False, "File exceeded the allowed size of 4 MB"

        image = Image.open(file_full_name)

        image_dim = image.size
        if image_dim[0] < 180:
            return False, "Image width is less than 180"
        if image_dim[1] < 180:
            return False, "Image height is less than 180"
        thumb_dim = self.get_thumb_size(image_dim, width_max=180)

        image = image.resize(thumb_dim, Image.ANTIALIAS)
        image.save(thumbnail_file, quality=90)

        icon = self.get_icon(media_root, user.id)

        # Save Activity
        ActivityFunctions().save_activity(user.id, "change_picture")

        return True, icon

    def change_password(self, email, password1, password2, passwordold):
        password1 = '' if password1 is None else str(password1)
        password2 = '' if password2 is None else str(password2)
        passwordold = '' if passwordold is None else str(passwordold)

        response, password = self.verify_passwords(password1, password2)
        if not response:
            return response, password

        if password == passwordold:
            return False, "Old password and new password are same"

        response, user = self.check_email_password(email, passwordold)
        if not response:
            return response, user

        user.password = generate_password_hash(password, method='sha256')
        db.session.commit()

        # Save Activity
        ActivityFunctions().save_activity(user.id, "change_password")

        return True, "Password changed"

    def register_profile(self, creator, user_id, phone, company, website, address, country, state, district, city, postalcode, aadhar):
        account_profile = self.init_register_profile(
            creator, user_id, phone, company, website, address, country, state, district, city, postalcode, aadhar)

        db.session.add(account_profile)
        db.session.commit()
