# EngageBot

EngageBot is an AI-powered chatbot that uses sentiment analysis and natural language processing to interact with users in a friendly and empathetic manner. This project includes functionalities such as extracting entities from user input, sentiment analysis, and combatting prompt injection attacks.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Setting Up the MySQL Database](#setting-up-the-mysql-database)
- [Running the API](#running-the-api)

## Prerequisites

Before you begin, ensure you have the following software installed on your system:

- Python 3.12
- MySQL 8.0 or higher
- pip (Python package installer)

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/DB00709/engagebot.git
    ```

2. **Install the required Python packages**:

    ```bash
    pip install -r requirements.txt
    ```

## Setting Up the MySQL Database

1. **Start the MySQL server** and log in as a user with permissions to create databases:

    ```bash
    mysql -u root -p
    ```

2. **Create the database** and import the schema from the `engagebot.sql` file:

    ```sql
    CREATE DATABASE engagebot_db;
    USE engagebot_db;
    SOURCE engagebot.sql;
    ```

3. **Update the database configuration** in the `database_connection.py` file:
    Replace `yourpassword` with your actual MySQL root password for the function set_db_password(laptop_name).

4. **Update `.env` file:
    Replace `GROQ_API_KEY` with your actual groq api key. You can make one, reference:- `https://console.groq.com/keys`

## Running the API

1. **Run the API server**:

    ```bash
    python main.py
    ```

    The server will start running on `http://localhost:5000`.

2. **Test the `add_user_data` API**:
    Use a tool like Postman, or any HTTP client to make a POST request to the `/add_user_data` endpoint.


### POST /add_user_data

Adds a user's data to the database.

**Request Body**:

```json
{
    "name": "string",
    "email": "string",
    "phone_number": "string",
    "location": "string",
    "age": "integer"
}
