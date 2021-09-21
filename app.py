from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

URI_KEY = os.getenv("URI_KEY")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = URI_KEY

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
CORS(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable=False, unique= True)
    password= db.Column(db.String, nullable=False)
    name = db.Column(db.string, nullable=False)

    def __init__(self,username ,name, password):
        self.username = username
        self.password = password
        self.name = name

class UserSchema(ma.Schema):
    class Meta:
        fields = ("username","name")

user_schema = UserSchema()
multiple_user_schema = UserSchema(many=True)

@app.route("/user/add", methods=["POST"])
def add_user():
    if request.content_type != "application/json":
        return jsonify("Error: Data must be sent as json")

    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")
    name = post_data.get("name")

    pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    
    new_record = User( username, pw_hash, name)
    db.session.add(new_record)
    db.session.commit()
    
    return jsonify(user_schema.dump(new_record))

@app.route("/user/verification", methods = ["POST"])
def verification():
    if request.content_type != "application/json":
        return jsonify("Error: data must be sent as JSON")

    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")

    user = db.session.query(User).filter(User.username == username).first()

    if user is None: 
        return jsonify("User NOT Verified")

    if not bcrypt.check_password_hash(user.password, password): 
        return jsonify("User NOT Verified")        

    return jsonify(user_schema.dump(user))


@app.route("/user/get", methods=["GET"] )
def get_all_users():
    all_users = db.session.query(User).all()
    return jsonify(multiple_user_schema.dump(all_users))



@app.route("/user/get/<username>", methods=["GET"])
def get_user(username):
    user = db.session.query(User).filter(User.username == username).first()
    return jsonify(user_schema.dump(user))


@app.route("/user/get/<name>", methods=["GET"])
def get_user_name(name):
    user = db.session.query(User).filter(User.name == name).first()
    return jsonify(user_schema.dump(user))






if __name__ == "__main__":
    app.run(debug=True)

