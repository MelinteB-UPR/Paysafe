from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="Please add a username, this field should not be blank! "
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="Please add a password, this field should not be blank! "
                        )

    def post(self):
        request_data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(request_data['username']):
            return {'message': f"A user with username:{request_data['username']}, already exists!"}, 400

        user = UserModel(**request_data)
        user.save_to_db()

        return {"message": "User created successfully"}, 201
