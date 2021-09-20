from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://mpdkacjatcpfnp:a6614aa48fd5a54d43354f82c444ca5b001e79d0b6fe2c0d6bf14cc2757b4423@ec2-54-224-120-186.compute-1.amazonaws.com:5432/d36re597piotio"

db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable=False, unique= True)
    password= db.Column(db.String, nullable=False)

    def __init__(self,username,password):
        self.username = username
        self.password = password

class UserSchema(ma.Schema):
    class Meta:
        fields = ("username", "password")

user_schema = UserSchema()
multiple_user_schema = UserSchema(many=True)

@app.route("/user/add", methods=["POST"])
def add_user():
    if request.content_type != "application/json":
        return jsonify("Error: Data must be sent as json")

    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")
    
    new_record = User( username, password )
    db.session.add(new_record)
    db.session.commit()
    
    return jsonify(user_schema.dump(new_record))

@app.route("/user/verification", methods = ["POST"])
def verification():
    if request.content_type != "application/json":
        return jsonify("Error: data must be sent as JSON")

    post_data = request.get_json()
    username = post_data.get("username")
    username = post_data.get("password")

    user = db.session.query(User).filter(User.username == username).first()

    if user is None: 
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






if __name__ == "__main__":
    app.run(debug=True)

