from dotenv import load_dotenv
from keycloak import KeycloakOpenID
import jwt
import os

load_dotenv()

#configure keycloak client
keycloak_openid = KeycloakOpenID(server_url="http://192.168.10.3:8080/auth/",
                                 client_id=f'{os.getenv("KEYCLOAK_CLIENT_ID")}',
                                 realm_name=f'{os.getenv("KEYCLOAK_REALM")}',
                                 client_secret_key=f'{os.getenv("KEYCLOAK_CLIENT_SECRET")}')

def get_user(request):
  try:
    token = request.headers["Authorization"].split()[1]
    KEYCLOAK_PUBLIC_KEY = keycloak_openid.public_key()
    userinfo = jwt.decode(token, verify=False)
    user = {
        "roles": userinfo['resource_access'][os.getenv('KEYCLOAK_CLIENT_ID')]['roles'],
        "name": userinfo['name'],
        "username": userinfo['preferred_username'],
        "email": userinfo['email'],
        "first_name": userinfo['given_name'],
        "last_name": userinfo['family_name']
    }
    return user
  except Exception as e:
    print(e)
    return False


def user_has_role(request, role):
  user = get_user(request)
  if not user:
    return False
  if role in user["roles"]:
    return True
  else:
    return False
