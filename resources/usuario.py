from flask_restful import Resource, reqparse
from blacklist import BLACKLIST
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
import hmac

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="The field 'login' cannot be left brank.")
atributos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left brank.")
 

class User(Resource):
    # /usuarios/{user_id}
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404
    
    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return  {'message': 'An error ocurred trying to delete User.'}, 200 
            return  {'message': 'User deleted.'}, 200 
        return  {'message': 'User not found.'}, 404

class UserRegister(Resource):
    # /cadastro
    @jwt_required()
    def post(self):
        dados = atributos.parse_args()
        if UserModel.find_by_login(dados['login']):
            return {'message':"The login '{}' already exists.".format(dados['login'])}
        
        user = UserModel(**dados)
        user.save_user()
        return {'message':'User created sucessfully.'}, 201     # Created

class UserLogin(Resource):

    @classmethod
    def safe_str_cmp(cls, a: str, b: str) -> bool:
        """This function compares strings in somewhat constant time. This
        requires that the length of at least one string is known in advance.

        Returns `True` if the two strings are equal, or `False` if they are not.
        """
        if isinstance(a, str):
            a = a.encode("utf-8")  # type: ignore

        if isinstance(b, str):
            b = b.encode("utf-8")  # type: ignore

        return hmac.compare_digest(a, b)

    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        user = UserModel.find_by_login(dados['login'])
        cmp = cls.safe_str_cmp(user.senha, dados['senha'])

        if user and cmp:
            token_de_acesso = create_access_token(identity=user.user_id)
            return  {'access_token': token_de_acesso}, 200
        
        return {'message': 'The username ou password is incorrect'}, 401

class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] # JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully'}, 200