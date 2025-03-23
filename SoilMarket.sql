use soilmarket;

-- Tables below are the required tables for our website, created as per the data model. 
CREATE TABLE Soil_Types (
    soil_id INT PRIMARY KEY,
    provider_id INT,
    pH_level INT,
    type VARCHAR(255),
    NPK_level DECIMAL,
    Quantity DECIMAL,
    availability VARCHAR(255),
    location VARCHAR(255)
);

CREATE TABLE Owners (
    owner_id INT PRIMARY KEY,
    name VARCHAR(255),
    phone_number VARCHAR(255),
    email VARCHAR(255)
);

CREATE TABLE Users (
    user_id INT PRIMARY KEY,
    name VARCHAR(255),
    address VARCHAR(255),
    role VARCHAR(255),
    phone_number INT
);

CREATE TABLE Farms (
    farm_id VARCHAR(255) PRIMARY KEY,
    soil_id INT,
    owner_id INT,
    listing_id INT,
    location VARCHAR(255),
    size DECIMAL,
    FOREIGN KEY (soil_id) REFERENCES Soil_Types(soil_id),
    FOREIGN KEY (owner_id) REFERENCES Owners(owner_id),
    FOREIGN KEY (listing_id) REFERENCES Listings(listing_id)
);

CREATE TABLE Listings (
    listing_id INT PRIMARY KEY,
    user_id INT,
    soil_id INT,
    price DECIMAL,
    quantity DECIMAL,
    date DATE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (soil_id) REFERENCES Soil_Types(soil_id)
);

-- Above are all tables required for the website

