### README.md

```
# Soil Market

Soil Market is a web-based platform designed to connect farmers, gardeners, and small businesses for sustainable and localized soil resource sharing. The system facilitates soil database management, listing creation, and communication between users.

## Features
- User registration and login
- Farmer and admin dashboards
- Soil and farm listing management
- Filtering and searching soil listings
- Contacting listing owners
- Location-based matching for soil resources

```

```
## Project Structure

project-directory/
├── run.py
├── SoilMarket.sql
├── __pycache__/
│   ├── run.cpython-313.pyc
├── app/
│   ├── __init__.py
│   ├── utils.py
│   ├── config.py
│   ├── db_manager.py
│   ├── TableClasses.py
│   ├── views.py
│   ├── __pycache__/
│   │   ├── __init__.cpython-313.pyc
│   │   ├── TableClasses.cpython-313.pyc
│   │   ├── utils.cpython-313.pyc
│   │   ├── views.cpython-313.pyc
│   ├── templates/
│   │   ├── index.html
│   │   ├── listing.html
│   │   ├── contact.html
│   │   ├── add_farm.html
│   │   ├── add_listing.html
│   │   ├── add-listing-global.html
│   │   ├── admin_dashboard.html
│   │   ├── farmer_dashboard.html
│   │   ├── farms.html
│   │   ├── login.html
│   │   ├── protected_page.html
│   │   ├── signup.html
│   │   ├── user_dashboard.html
│   ├── static/
│   │   ├── css/
│   │   │   ├── styles.css
│   │   │   ├── styles2.css
│   │   ├── images/
│   │   ├── js/
│   │   │   ├── app.js
│   ├── models/
│   │   ├── user.py
```

````
## Prerequisites

- **Python 3.8+**
- **Flask** (for web application development)
- **MySQL** (or a compatible database system)
- **Virtual Environment** (optional but recommended)

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd project-directory
````

### 2. Set Up a Virtual Environment (Optional)

```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

Install required Python packages:

```bash
pip install flask pymysql
```

### 4. Set Up the Database

1. Create a MySQL database:

   ```sql
   CREATE DATABASE SoilMarket;
   ```

2. Import the provided SQL schema:

   ```bash
   mysql -u <username> -p SoilMarket < SoilMarket.sql
   ```

3. Update the database URI in `config.py`:

   ```python
   SQLALCHEMY_DATABASE_URI = "mysql+pymysql://<username>:<password>@<host>/SoilMarket"
   ```

Replace `<username>`, `<password>`, and `<host>` with your database credentials.

### 5. Run the Application

Start the Flask server:

```bash
python run.py
```

The application will be available at `http://127.0.0.1:5000/`.

------

## Key Features

### Frontend

- **HTML Templates**: Located in `app/templates/`, including:
  - `index.html` - Homepage
  - `login.html` and `signup.html` - User authentication pages
  - `listing.html` - Soil listings with filtering options
  - `farmer_dashboard.html` - Farmer's management dashboard
  - `admin_dashboard.html` - Admin panel for managing the platform
- **Static Assets**:
  - CSS: `styles.css` and `styles2.css`
  - JavaScript: `app.js` for dynamic functionalities

### Backend

- **Routes and Views**: Defined in `views.py` for handling user actions like login, signup, and CRUD operations.
- **Database Management**: Handled by `db_manager.py` and `TableClasses.py` for efficient data interaction.

------

## How to Use

1. **Sign Up and Log In**: Create an account and log in to access personalized dashboards.
2. **Add Listings**: Farmers can add and manage soil listings via their dashboard.
3. **Browse Listings**: Users can filter and search listings based on price, quantity, and soil type.
4. **Contact Owners**: Users can contact listing owners directly from the platform.

------

## Future Enhancements

- Advanced analytics for farmers and admins
- Enhanced search filters (e.g., pH level, soil type)
- Integration with geolocation APIs for location-based recommendations

------

## Contributors

- **Stefan Martinelli** (Team Lead)
- **Anush** (Database Development)
- **Kenneth** (Python Developer)
- **Andrew Pan** (Database Architect)

------

## License

This project is licensed under the MIT License.
