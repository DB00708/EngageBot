CREATE DATABASE engage_bot_local;

USE engage_bot_local;

CREATE TABLE user_data (
    engagebot_user_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    age INT,
    email VARCHAR(255),
    phone_number VARCHAR(15),
    location VARCHAR(63),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
