from flask import Blueprint, jsonify, request, render_template
from sqlalchemy import exc
from project import db
from project.api.models import User

users_blueprint = Blueprint("users", __name__, template_folder="./templates")


@users_blueprint.route("/users/ping")
def ping_pong():
    return jsonify({"status": "success", "message": "pong!"})


@users_blueprint.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        db.session.add(User(username=username, email=email))
        db.session.commit()
    users = User.query.all()
    return render_template("index.html", users=users)


@users_blueprint.route("/users", methods=["GET"])
def get_all_users():
    response = {
        "status": "success",
        "data": {"users": [user.to_json() for user in User.query.all()]},
    }
    return jsonify(response), 200


@users_blueprint.route("/users", methods=["POST"])
def add_user():
    post_data = request.get_json()
    response = {"status": "fail", "message": "Invalid payload"}

    if not post_data:
        return jsonify(response), 400

    username = post_data.get("username")
    email = post_data.get("email")

    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            db.session.add(User(username=username, email=email))
            db.session.commit()
            response["status"] = "success"
            response["message"] = f"{email} was added!"
            return jsonify(response), 201
        else:
            response["message"] = "Email already exists"
            return jsonify(response), 400
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(response), 400


@users_blueprint.route("/users/<int:user_id>")
def get_single_user(user_id):
    response = {"status": "fail", "message": "User doesn't exist"}

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify(response), 404
    else:
        response = {
            "status": "success",
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "active": user.active,
            },
        }
        return jsonify(response), 200
