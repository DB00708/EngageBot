import uuid
from flask import Flask, jsonify
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from src.chatbot.chatbot_backend import gather_user_data
from database_connection import DB_USER, DB_PASSWORD, DB_HOST, DB_DATABASE

app = Flask(__name__)
db_uri = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class UserData(db.Model):
    engagebot_user_id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    age = db.Column(db.Integer)
    email = db.Column(db.String(255))
    phone_number = db.Column(db.String(15))
    location = db.Column(db.String(63))

    def __init__(self, engagebot_user_id, name, age, email, phone_number, location, created_at):
        self.engagebot_user_id = engagebot_user_id
        self.name = name
        self.age = age
        self.email = email
        self.phone_number = phone_number
        self.location = location
        self.created_at = created_at

    @staticmethod
    def add_user_details(name, age, email, phone_number, location):

        new_squad = UserData(
            engagebot_user_id=str(uuid.uuid4()),
            name=name,
            age=age,
            email=email,
            phone_number=phone_number,
            location=location,
            created_at=datetime.now(tz=timezone.utc)
        )

        db.session.add(new_squad)
        db.session.commit()


@app.route('/add_user_data', methods=['POST'])
def add_user():
    name, age, email, phone_number, location = gather_user_data()
    UserData.add_user_details(name, age, email, phone_number, location)
    return jsonify({"name": name, "email": email, "phone_number": phone_number, "location": location, "age": age}), 200


if __name__ == '__main__':
    app.run(debug=True)
