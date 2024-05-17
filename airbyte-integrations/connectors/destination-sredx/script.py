import requests
from requests_oauthlib import OAuth2Session
from requests_oauth2client import OAuth2Client

# Configuration
client_id = "scoring-sredx-home"
client_secret = "BRZS1NtZ7Hx4XXQdfF5nq1899Nc9aRxI"
token_url = "http://localhost:8081/auth/realms/sredx/protocol/openid-connect/token"


# oauth2client = OAuth2Client(
#     token_endpoint="http://localhost:8081/auth/realms/sredx/protocol/openid-connect/token",
#     client_id = "scoring-sredx-home",
#     client_secret = "BRZS1NtZ7Hx4XXQdfF5nq1899Nc9aRxI"
# )
# token=oauth2client.client_credentials(scope="myscope")

# Obtenez un jeton d'accès OAuth2 Client Credentials
response2 = requests.post("http://localhost:8080/api/v2/airbyte2/postPullRequests", json=[{"object": "afa"}])
print(f'{response2}')
# headers = {'Content-Type': 'application/x-www-form-urlencoded'}
# token_response = requests.post(token_url, data={
#     'grant_type': 'client_credentials',
#     'client_id': client_id,
#     'client_secret': client_secret
# },headers=headers)
# print(f'token response :{token_response.json()}')

# # Vérifiez si la requête a réussi et obtenez le jeton d'accès
# if token_response.status_code == 200:
#     access_token = token_response.json().get('access_token')
#     print("acces : "+access_token)
    
#     # Utilisez le jeton d'accès pour effectuer une requête HTTP POST vers l'API SREDX
#     headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
#     data = {"id": "qq12", "object": "afa"}
#     response = requests.post("http://localhost:8080/api/v2/airbyte2/postPullRequests", json=data, headers=headers)

    
#     # Traitement de la réponse
#     print(response.json())

# else:
#     print("Échec de l'obtention du jeton d'accès.")
# response2 = requests.post("http://localhost:8080/api/v2/airbyte2/postPullRequests", json={"id": "qq12", "object": "afa"})
# print(f'hehe{response2}')



