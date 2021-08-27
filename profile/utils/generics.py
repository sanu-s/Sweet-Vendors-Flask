from config.location import LOCATIONS
from profile.models import AccountProfile
from config.profile import ALLOWED_PICS, ALLOWED_COUNTRIES


class ProfileValidation:
    def allowed_profile_pics(self, filename):
        return '.' in filename and filename.rsplit('.')[-1].lower() in ALLOWED_PICS

    def get_thumb_size(self, image_dimension, width_max):
        width_rate = image_dimension[0] / width_max
        height_rate = image_dimension[1] / width_rate
        return (int(width_max), int(height_rate))

    def verify_company(self, company):
        if len(company) < 3:
            return False, "Company must be contain 3 characters"
        if len(company) > 25:
            return False, "Only 25 characters are allowed for company field"
        return True, "Success"

    def verify_phone(self, phone):
        if not phone.isnumeric() or len(phone) != 10:
            return False, "Invalid phone"
        return True, "Success"

    def verify_website(self, website):
        if '.' not in website or len(website) < 6:
            return False, "Invalid website"
        if len(website) > 100:
            return False, "Only 100 characters are allowed for website field"
        return True, "Success"

    def verify_address(self, address):
        if len(address) < 10:
            return False, "Address must be contain 10 characters"
        if len(address) > 300:
            return False, "Only 300 characters are allowed for address field"
        return True, "Success"

    def verify_country(self, country):
        if country not in ALLOWED_COUNTRIES:
            return False
        return True

    def verify_state_district(self, state, district):
        state_flag, district_flag = False, False
        for i in LOCATIONS:
            if i['state'] == state:
                state_flag = True
                if district in i['districts']:
                    district_flag = True
                break
        if not state_flag:
            return False, "Invalid state"
        if not district_flag:
            return False, "Invalid district"
        return True, "Success"

    def verify_country_state_district(self, country, state, district):
        result = self.verify_country(country)
        if not result:
            return result, "Invalid country"

        result, message = self.verify_state_district(state, district)
        return result, message

    def verify_city(self, city):
        if len(city) < 3:
            return False, "City must be contain 3 characters"
        if len(city) > 30:
            return False, "Only 30 characters are allowed for city field"
        if not city.replace(' ', '').isalpha():
            return False, "Only alphabhets are allowed as city."
        return True, "Success"

    def verify_postalcode(self, postalcode):
        if not postalcode.isnumeric() or len(postalcode) != 6:
            return False, "Invalid postalcode"
        return True, "Success"

    def verify_aadhar(self, aadhar):
        if not aadhar.isnumeric() or len(aadhar) != 12:
            return False, "Invalid aadhar"
        return True, "Success"

    def get_profile_table(self, user_id):
        return AccountProfile.query.filter_by(user_id=user_id).first()

    def is_profile_exists(self, phone, user_id=None):
        account = AccountProfile.query.filter_by(phone=phone).first()
        if account is not None and user_id is not None:
            if account.user_id == user_id:
                account = None

        return False if account is None else True

    def init_register_profile(self, creator, user_id, phone, company, website, address, country, state, district, city, postalcode, aadhar):
        account_profile = AccountProfile(user_id=user_id, phone=phone, company=company, website=website, address=address,
                                         country=country, state=state, district=district, city=city, postalcode=postalcode, aadhar=aadhar, created_by=creator)

        return account_profile

    def get_profile_info(self, user_id):
        account = AccountProfile.query.filter_by(user_id=user_id).first()
        if account is None:
            context = {
                "phone": None,
                "company": None,
                "website": None,
                "address": None,
                "country": None,
                "state": None,
                "district": None,
                "city": None,
                "postalcode": None,
                "aadhar": None,
            }

            return context

        context = {
            "phone": account.phone,
            "company": account.company,
            "website": account.website,
            "address": account.address,
            "country": account.country,
            "state": account.state,
            "district": account.district,
            "city": account.city,
            "postalcode": account.postalcode,
            "aadhar": account.aadhar,
        }
        return context
