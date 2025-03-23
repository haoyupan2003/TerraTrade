from flask import Blueprint, flash, redirect, render_template, request, url_for, session
from app.TableClasses import Users, Farms, Listings, SoilTypes, Owners, add_user, db
from app.utils import login_required, role_required
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash


views = Blueprint("views", __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('views.login'))
        return f(*args, **kwargs)
    return decorated_function

@views.route("/")
def home():
    return render_template("index.html")

@views.route('/listing', methods=['GET', 'POST'])
def listing():
    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Number of listings per page

    # Default query
    query = db.session.query(Listings)

    if request.method == 'POST':
        # Retrieve filter values from the form
        min_price = request.form.get('min_price')
        max_price = request.form.get('max_price')
        min_quantity = request.form.get('min_quantity')
        max_quantity = request.form.get('max_quantity')

        # Apply filters to the query
        if min_price:
            query = query.filter(Listings.price >= float(min_price))
        if max_price:
            query = query.filter(Listings.price <= float(max_price))
        if min_quantity:
            query = query.filter(Listings.quantity >= int(min_quantity))
        if max_quantity:
            query = query.filter(Listings.quantity <= int(max_quantity))

    # Paginate the filtered query
    pagination = query.paginate(page=page, per_page=per_page)
    listings = pagination.items

    return render_template('listing.html', listings=listings, pagination=pagination)


@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Fetch user from the database
        user = db.session.query(Users).filter_by(email=email).first()

        # Check if the user exists and password matches
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.user_id
            session['user_name'] = user.name
            session['user_role'] = user.role  # Store the user's role in the session

            # Redirect based on role
            if user.role == 'user':
                return redirect(url_for('views.user_dashboard'))
            elif user.role == 'farmer':
                return redirect(url_for('views.farmer_dashboard'))
            elif user.role == 'admin':
                return redirect(url_for('views.admin_dashboard'))
        else:
            flash('Invalid email or password!', 'danger')
            return redirect(url_for('views.login'))

    return render_template('login.html')


@views.route('/protected-page')
@login_required
def protected_page():
    return render_template('protected_page.html')

@views.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('views.home'))

@views.route('/contact')
def contact():
    return render_template('contact.html')

@views.route('/contact/<int:owner_id>')
@role_required(['user'])
def contact_owner(owner_id):
    owner = db.session.query(Owners).filter_by(owner_id=owner_id).first()
    if not owner:
        flash('Owner not found.', 'danger')
        return redirect(url_for('views.user_dashboard'))

    return render_template('contact.html', owner=owner)


@views.route('/signup')
def signup_form():
    return render_template('signup.html')

@views.route('/signup', methods=['POST'])
def signup():
    # Retrieve form data
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    address = request.form.get('address')
    phone_number = request.form.get('phone_number')
    role = request.form.get('role')

    print(f"Received form data: Name={name}, Email={email}, Password=[hidden], Address={address}, Phone Number={phone_number}, Role={role}")

    # Validate required fields
    if not name or not email or not password or not address or not phone_number or not role:
        flash('All fields are required!', 'danger')
        return redirect(url_for('views.signup'))

    try:
        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Create a new user
        new_user = Users(
            name=name,
            email=email,
            password=hashed_password,
            address=address,
            phone_number=phone_number,
            role=role  # Set the selected role
        )

        db.session.add(new_user)
        db.session.commit()
        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('views.login'))  # Redirect to login page
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('views.signup'))




@views.route('/user-dashboard')
@role_required(['user'])
def user_dashboard():
    # Join Farms with Owners to ensure valid owner_id
    farms = db.session.query(Farms).join(Owners, Farms.owner_id == Owners.owner_id).all()
    soil_types = db.session.query(SoilTypes).all()
    listings = db.session.query(Listings).all()

    return render_template(
        'user_dashboard.html',
        farms=farms,
        soil_types=soil_types,
        listings=listings
    )



@views.route('/farmer-dashboard')
@role_required(['farmer'])
def farmer_dashboard():
    user_id = session.get('user_id')  # Get the current farmer's ID from session
    listings = db.session.query(Listings).filter_by(user_id=user_id).all()  # Filter listings by user_id
    return render_template('farmer_dashboard.html', listings=listings)



@views.route('/farmer-dashboard/manage-listings', methods=['GET', 'POST'])
@role_required(['farmer'])
def manage_listings():
    user_id = session.get('user_id')  # Farmer's ID
    listings = db.session.query(Listings).filter_by(user_id=user_id).all()

    if request.method == 'POST':
        listing_id = request.form.get('listing_id')
        action = request.form.get('action')

        if action == 'delete':
            listing = db.session.query(Listings).filter_by(listing_id=listing_id).first()
            if listing:
                db.session.delete(listing)
                db.session.commit()
                flash('Listing deleted successfully!', 'success')
        elif action == 'edit':
            # Editing logic here
            pass

        return redirect(url_for('views.manage_listings'))

    return render_template('manage_listings.html', listings=listings)


@views.route('/farmer-dashboard/add-listing', methods=['GET', 'POST'])
@role_required(['farmer'])
def add_listing():
    if request.method == 'POST':
        user_id = session.get('user_id')  # Farmer's ID
        soil_id = request.form.get('soil_id')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        date = request.form.get('date')

        try:
            new_listing = Listings(
                user_id=user_id,
                soil_id=soil_id,
                price=price,
                quantity=quantity,
                date=date
            )
            db.session.add(new_listing)
            db.session.commit()
            flash('Listing added successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('views.farmer_dashboard'))

    return render_template('add_listing.html')




@views.route('/admin-dashboard')
@role_required(['admin'])
def admin_dashboard():
    users = db.session.query(Users).all()
    listings = db.session.query(Listings).all()
    farms = db.session.query(Farms).all()
    soil_types = db.session.query(SoilTypes).all()

    return render_template(
        'admin_dashboard.html',
        users=users,
        listings=listings,
        farms=farms,
        soil_types=soil_types
    )



@views.route('/farms')
def farms():
    # Query Farms and join with Listings to get related data
    farms = db.session.query(Farms, Listings).join(Listings, Farms.listing_id == Listings.listing_id).all()
    return render_template('farms.html', farms=farms)


@views.route('/farms/filter')
def filter_farms():
    min_size = request.args.get('min_size', default=0, type=float)
    farms = db.session.query(Farms).filter(Farms.size >= min_size).all()
    return render_template('farms.html', farms=farms)


@views.route('/add-farm', methods=['GET', 'POST'])
def add_farm():
    if request.method == 'POST':
        # Retrieve form data
        farm_id = request.form.get('farm_id')
        soil_id = request.form.get('soil_id')
        owner_id = request.form.get('owner_id')
        listing_id = request.form.get('listing_id')
        location = request.form.get('location')
        size = request.form.get('size')

        # Validate required fields
        if not farm_id or not listing_id or not location or not size:
            flash('Farm ID, Listing ID, Location, and Size are required!', 'danger')
            return redirect(url_for('views.add_farm'))

        try:
            # Add the new farm to the database
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
            flash('Farm added successfully!', 'success')
            return redirect(url_for('views.farms'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('views.add_farm'))

    # Render the form
    return render_template('add_farm.html')

@views.route('/add-listing-global', methods=['GET', 'POST'])
def add_global_listing():
    if request.method == 'POST':
        # Logic to add a listing
        user_id = request.form.get('user_id')
        soil_id = request.form.get('soil_id')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        date = request.form.get('date')

        if not user_id or not soil_id or not price or not quantity or not date:
            flash('All fields are required!', 'danger')
            return redirect(url_for('views.add_listing'))

        try:
            new_listing = Listings(
                user_id=user_id,
                soil_id=soil_id,
                price=price,
                quantity=quantity,
                date=date
            )
            db.session.add(new_listing)
            db.session.commit()
            flash('Listing added successfully!', 'success')
            return redirect(url_for('views.listing'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('views.add_listing'))

    soils = db.session.query(SoilTypes).all()
    return render_template('add_listing.html', soils=soils)

