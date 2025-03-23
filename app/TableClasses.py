from app import db  # Use the db instance from __init__.py
from datetime import datetime


# Database Models
class SoilTypes(db.Model):
    __tablename__ = 'Soil_Types'
    soil_id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer)
    pH_level = db.Column(db.Integer)
    type = db.Column(db.String(255))
    NPK_level = db.Column(db.Float)
    quantity = db.Column(db.Float)
    availability = db.Column(db.String(255))
    location = db.Column(db.String(255))


class Owners(db.Model):
    __tablename__ = 'Owners'
    owner_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    email = db.Column(db.String(255))


class Users(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)  # Ensure email is unique
    password = db.Column(db.String(255), nullable=False)  # Store hashed passwords for security



class Farms(db.Model):
    __tablename__ = 'Farms'
    farm_id = db.Column(db.String(255), primary_key=True)
    soil_id = db.Column(db.Integer, db.ForeignKey('Soil_Types.soil_id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('Owners.owner_id'))
    listing_id = db.Column(db.Integer, db.ForeignKey('Listings.listing_id'))
    location = db.Column(db.String(255))
    size = db.Column(db.Float)


class Listings(db.Model):
    __tablename__ = 'Listings'
    listing_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    soil_id = db.Column(db.Integer, db.ForeignKey('Soil_Types.soil_id'))
    price = db.Column(db.Float)
    quantity = db.Column(db.Float)
    date = db.Column(db.Date)

# Helper Functions
def add_user(name, address, role, phone_number):
    try:
        print("About to add a new user...")
        new_user = Users(
            name=name,
            address=address,
            role=role,
            phone_number=phone_number,
            email=email,
            password=hashed_password
        )
        db.session.add(new_user)
        print("User added to session, committing...")
        db.session.commit()
        print(f"User {name} added to the database successfully.")
        return new_user
    except Exception as e:
        print(f"Error adding user: {e}")
        raise




def add_soil_type(provider_id, pH_level, soil_type, NPK_level, quantity, availability, location):
    new_soil = SoilTypes(
        provider_id=provider_id,
        pH_level=pH_level,
        type=soil_type,
        NPK_level=NPK_level,
        quantity=quantity,
        availability=availability,
        location=location
    )
    db.session.add(new_soil)
    db.session.commit()
    return new_soil


def add_farm(farm_id, soil_id, owner_id, listing_id, location, size):
    # Validate foreign keys
    soil = SoilTypes.query.get(soil_id)
    owner = Owners.query.get(owner_id)
    listing = Listings.query.get(listing_id)
    if not soil:
        raise ValueError(f"Soil with ID {soil_id} does not exist")
    if not owner:
        raise ValueError(f"Owner with ID {owner_id} does not exist")
    if not listing:
        raise ValueError(f"Listing with ID {listing_id} does not exist")

    # Add farm
    new_farm = Farms(
        farm_id=farm_id,
        soil_id=soil_id,
        owner_id=owner_id,
        listing_id=listing_id,
        location=location,
        size=size
    )
    db.session.add(new_farm)
    db.session.commit()
    return new_farm


def add_owner(name, phone_number, email):
    # Check if email is unique
    existing_owner = Owners.query.filter_by(email=email).first()
    if existing_owner:
        raise ValueError(f"Owner with email {email} already exists")

    # Add owner
    new_owner = Owners(name=name, phone_number=phone_number, email=email)
    db.session.add(new_owner)
    db.session.commit()
    return new_owner


def add_listing(user_id, soil_id, price, quantity, date):
    # Validate foreign keys
    user = Users.query.get(user_id)
    soil = SoilTypes.query.get(soil_id)
    if not user:
        raise ValueError(f"User with ID {user_id} does not exist")
    if not soil:
        raise ValueError(f"Soil with ID {soil_id} does not exist")

    # Add listing
    new_listing = Listings(
        user_id=user_id,
        soil_id=soil_id,
        price=price,
        quantity=quantity,
        date=date
    )
    db.session.add(new_listing)
    db.session.commit()
    return new_listing
