import jwt
from datetime import datetime, timedelta
from configs.settings import SECRET_KEY

def gerar_tokens(user_id):
    agora = datetime.utcnow()
    expiracao_acesso = agora + timedelta(hours=6)
    expiracao_refresh = agora + timedelta(days=1)

    payload_acesso = {
        'token_type': 'access',
        'exp': expiracao_acesso,
        'iat': agora,
        'jti': 'access_token',
        'user_id': user_id,
    }

    payload_refresh = {
        'token_type': 'refresh',
        'exp': expiracao_refresh,
        'iat': agora,
        'jti': 'refresh_token',
        'user_id': user_id,
    }

    token_acesso = jwt.encode(payload_acesso, SECRET_KEY, algorithm='HS256')
    token_refresh = jwt.encode(payload_refresh, SECRET_KEY, algorithm='HS256')

    return token_acesso, token_refresh


def renovar_token(refresh_token):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=['HS256'])

        if payload['token_type'] == 'refresh':
            user_id = payload['user_id']
            novo_token_acesso, novo_token_refresh = gerar_tokens(user_id)
            return novo_token_acesso, novo_token_refresh
        else:
            raise jwt.InvalidTokenError("Token de refresh inválido")

    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError("Token de refresh expirado")
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError("Token de refresh inválido")
