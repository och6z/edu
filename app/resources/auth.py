from flask_restful import Resource, reqparse

from app.resources import create_or_update_resource
from app.models import User


class UserRegister(Resource):
    """Register a new user.
    URL: /api/v1/auth/register
    Request method: POST
    """

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument(
            "username",
            required=True,
            help="Kérjük, adjon meg egy felhasználónevet.")
        parser.add_argument(
            "password",
            required=True,
            help="Kérjük, adjon meg egy jelszót.")
        args = parser.parse_args()
        username, password = args["username"], args["password"]
        user = User(username=username,
                    password=password)
        return create_or_update_resource(resource=user,
                                         resource_type="user",
                                         create=True,
                                         username=username)


class UserLogin(Resource):
    """Log a user in.
    URL: /api/v1/auth/login
    Request method: POST
    """

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument(
            "username",
            required=True,
            help="Kérjük, adjon meg egy felhasználónevet.")
        parser.add_argument(
            "password",
            required=True,
            help="Kérjük, adjon meg egy jelszót.")
        args = parser.parse_args()
        username, password = args["username"], args["password"]

        if username and password:
            user = User.query.filter_by(username=username).first()
        else:
            return {"error": "Kérjük, adja meg a felhasználónevét és a jelszót!"}, 400
        if user and user.verify_password(password):
            auth_token = user.generate_auth_token(user.id)
            return {"message": "Sikeresen bejelentkezett",
                    "user_id": user.id,
                    "token": auth_token.decode()}
        else:
            return {"error": "Helytelen felhasználónév és/vagy jelszó"}, 400
