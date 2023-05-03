#Podemos generar un token para el usuario
from jwt import encode, decode
#Solo son de ejemplos
def create_token(data: dict) ->str:
    token: str = encode(payload=data, key='my_secrete_key', algorithm='HS256')
    return token
#Validacion de token
def validate_token(token: str) ->dict:
    data: dict = decode(token, key='my_secrete_key', algorithms=['HS256'])
    return data