from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pets.db"
db = SQLAlchemy(app)


class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    pet = db.relationship('Pet', backref='people', uselist=False)


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_type = db.Column(db.String(20), nullable=False)
    pet_name = db.Column(db.String(20), nullable=False)
    pet_age = db.Column(db.Integer)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)

def fill_database():
    people_data = [
        {"name": "Somebody", "surname": "Anybody", "age": 25, "pet_type": "cat",
         "pet_name": "Barsic", "pet_age": 6},
        {"name": "Anybody", "surname": "Somebody", "age": 45, "pet_type": "dog",
         "pet_name": "Pushok", "pet_age": 5},
        {"name": "SMBD", "surname": "ANBD", "age": 20, "pet_type": "rabit",
         "pet_name": "---", "pet_age": 2},
    ]
    for people_info in people_data:
        people = People(name=people_info["name"],
                  surname=people_info["surname"],
                  age=people_info["age"]
                  )

        db.session.add(people)

        pet = Pet(pet_type=people_info["pet_type"],
                             pet_name=people_info["pet_name"],
                             pet_age=people_info["pet_age"],
                             people=people)
        db.session.add(pet)
        db.session.commit()

@app.route("/people/<int:people_id>/pet")
def get_pet(people_id):
    people = People.query.get_or_404(people_id)
    pet = people.pet
    if pet:
        return f"{people.id}, {people.name} {people.surname}, {pet.pet_type}, {pet.pet_name}"
    else:
        return "User has no pet"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        fill_database()
    app.run(debug=True)