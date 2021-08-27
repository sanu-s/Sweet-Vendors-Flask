from random import choice
from string import ascii_uppercase

from app.app import db
from user.models import User, Role
from config.user import USER_ROLES
from config.location import LOCATIONS
from profile.utils.utils import ProfileActions
from owner.utils.generics import OwnerValidation
from agent.utils.generics import AgentValidation
from ticket.utils.generics import TicketValidation
from activity.utils.generics import ActivityFunctions


class AgentActions(ProfileActions, AgentValidation, OwnerValidation, TicketValidation):
    def get_agent_detail(self, email, id):
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

    def create_agent_account(self, name, email):
        password = ''.join(choice(ascii_uppercase) for i in range(8))
        password = self.get_hash_from_password(password)
        user = User(name=name, email=email, password=password,
                    is_admin=True, is_active=False)
        db.session.add(user)
        db.session.commit()

        role = Role(user_id=user.id, name=USER_ROLES['agent']
                    ['name'], description=USER_ROLES['agent']['description'])
        db.session.add(role)
        db.session.commit()

        return user

    def create_agent(self, auth_email, name, email, phone, company, website, address, country, state, district, city, postalcode, aadhar, site_origin):
        is_owner = self.is_owner_account(auth_email)
        if not is_owner:
            return is_owner, "Unauthorized user"

        response, user = self.check_email_exist(auth_email)
        if not response:
            return response, user
        response, user = self.check_active(user)
        if not response:
            return response, user

        name = str(name)
        email = str(email)
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

        response, message = self.verify_email(email)
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

        # Check for existing account
        response, _ = self.check_email_exist(email)
        if response:
            return False, "User account already exist"
        # Check for existing profile
        response = self.is_profile_exists(phone)
        if response:
            return False, "Profile already exist with this phone number"

        # Create user account and profile
        new_user = self.create_agent_account(name, email)

        self.register_profile(user.id, new_user.id, phone, company, website,
                              address, country, state, district, city, postalcode, aadhar)

        # Create Ticket Entry
        ticket = self.make_ticket(new_user.id, 'agent')
        db.session.add(ticket)
        db.session.commit()

        # Save Activity
        ActivityFunctions().save_activity(
            new_user.id, "agent_create_request", ['Agent', user.email])

        context = {
            'id': new_user.id,
            'name': name,
            'email': email,
            'phone': phone,
            'company': company,
            'website': website,
            'address': address,
            'country': country,
            'state': state,
            'district': district,
            'city': city,
            'postalcode': postalcode,
            'aadhar': aadhar,
            'is_active': new_user.is_active,
            'created_at': new_user.created_at,
        }

        return True, context

    def get_agent_list(self, email, page, search):
        try:
            page = int(page)
        except (KeyError, ValueError):
            return False, "Invalid page value"

        search = '' if search is None else str(search).strip()

        is_owner = self.is_owner_account(email)
        if not is_owner:
            return is_owner, "Unauthorized user"

        response, user = self.check_email_exist(email)
        if not response:
            return response, user
        response, user = self.check_active(user)
        if not response:
            return response, user

        agent_list, page_count = self.get_all_agents(page, search)
        context = {
            "agent_list": agent_list,
            "page": page,
            "search": search,
            "page_count": page_count,
        }

        # Save Activity
        ActivityFunctions().save_activity(user.id, "agent_list_view", [page])

        return True, context
