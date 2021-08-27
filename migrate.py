import random
from datetime import datetime

from werkzeug.security import generate_password_hash

from app.app import app, db
from user.views import user_bp
from owner.views import owner_bp
from agent.views import agent_bp
from ticket.views import ticket_bp
from user.models import User, Role
from config.user import USER_ROLES
from profile.views import profile_bp
from config.location import LOCATIONS
from activity.views import activity_bp
from profile.models import AccountProfile


# Register Blueprints
app.register_blueprint(user_bp)
app.register_blueprint(owner_bp)
app.register_blueprint(agent_bp)
app.register_blueprint(ticket_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(activity_bp)


def generate_random_number(length):
    value = ''
    for _x in range(length):
        value += str(random.randint(0, 9))
    return value


def generate_state_district():
    i = random.randrange(len(LOCATIONS))
    state = LOCATIONS[i]['state']
    district = random.choice(LOCATIONS[i]['districts'])
    return state, district


if __name__ == "__main__":
    # Build the databases
    drop_ask = input(
        "Do you want to delete all tables before migration? [y/N]")
    if drop_ask.lower().strip() == 'y':
        db.drop_all()
        print("All database tables are droped.")
        print("Trying to create all database tables.")

    db.create_all()
    print("Database Migration Complete.\n")

    admin_ask = input("Do you want to create an owner account? [y/N]")
    if admin_ask.lower().strip() == 'y':
        print("Creating Admin User Account.\n")

        name = None
        while name is None:
            name = input("Enter name:").strip()
            if len(name) < 3:
                name = None
                print("Name must contain at least 3 characters.")
                continue
            if len(name) > 20:
                name = None
                print("Only 20 characters are allowed for name field.")
                continue
            if not name.replace(' ', '').isalpha():
                name = None
                print("Only alphabhets are allowed in name.")
                continue

        email = None
        while email is None:
            email = input("Enter email:").strip()
            if len(email) < 7:
                email = None
                print('Email address is invalid.')
                continue
            email_split = email.split('@')
            if len(email_split) != 2:
                email = None
                print('Email address is invalid.')
                continue
            if '.' not in email_split[1]:
                email = None
                print('Email address is invalid.')
                continue
            user = User.query.filter_by(email=email).first()
            if user is not None:
                email = None
                print("User account already exist with this email.")
                continue

        password = None
        while password is None:
            password = input("Enter password:").strip()
            if len(password) < 8:
                password = None
                print("Password must contain at least 8 characters.")
                continue
            if len(password) > 20:
                password = None
                print("Password must contain atmost 20 characters.")
                continue

        password = generate_password_hash(password, method='sha256')
        user = User(name=name, email=email, password=password,
                    is_admin=True, is_active=True)
        db.session.add(user)
        db.session.commit()

        role = Role(user_id=user.id, name=USER_ROLES['owner']
                    ['name'], description=USER_ROLES['owner']['description'])
        db.session.add(role)
        db.session.commit()

        phone = int(generate_random_number(10))
        while True:
            account_profile = AccountProfile.query.filter_by(
                phone=phone).first()
            if account_profile is None:
                break
            phone = int(generate_random_number(10))

        company = 'SweetVendors'
        website = 'sweetvendors.com'
        address = '0/0, XYZ, India'
        country = 'India'
        state, district = generate_state_district()
        city = 'CITY'
        creator = 0
        postalcode = int(generate_random_number(6))
        aadhar = int(generate_random_number(12))
        account_profile = AccountProfile(user_id=user.id, phone=phone, company=company, website=website, address=address,
                                         country=country, state=state, district=district, city=city, postalcode=postalcode, aadhar=aadhar, created_by=creator)
        db.session.add(account_profile)
        db.session.commit()

        print("Default Owner Account is Created.")
