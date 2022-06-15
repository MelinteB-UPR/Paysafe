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
    parser.add_argument('host',
                        type=str,
                        required=True,
                        help="Please add a hostname, this field should not be blank! "
                        )
    parser.add_argument('port',
                        type=int,
                        required=True,
                        help="Please add a port, this field should not be blank! "
                        )
    def post(self):
        request_data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(request_data['username']):
            return {'message': f"A user with username:{request_data['username']}, already exists!"}, 400

        user = UserModel(**request_data)
        user.save_to_db()

        return {"message": "User created successfully"}, 201

class User(Resource):
    """
    This resource can be useful when testing our Flask app. We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful when we are manipulating data regarding the users.
    """
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User Not Found'}, 404
        return user.json(), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User Not Found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted.'}, 200