import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime, timedelta
from app.settings import settings
from app.api.users.dao import UserDAO
import bcrypt

class AuthHandler():
    security = HTTPBearer()
    secret = settings.SECRET_KEY

    def __init__(self):
        self.user_dao = UserDAO()
        pass

    def get_password_hash(self, password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def verify_password(self, plain_password, hashed_password):
        return bcrypt.checkpw(plain_password.encode(), hashed_password)

    def encode_token(self, user_id) -> dict:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=50),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        token = jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )
        return {
            "access_token": token
        }

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            print("payload: ", payload)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        print("Executing auth_wrapper")
        return self.decode_token(auth.credentials)
