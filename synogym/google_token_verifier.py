from dataclasses import dataclass
import os

@dataclass
class GoogleUserInfo:
    email: str
    first_name: str
    last_name: str

class GoogleTokenVerifier:
    def __init__(self, client_id: str | None = None):
        self.client_id = client_id or os.environ.get("GOOGLE_CLIENT_ID")

    def verify(self, credential: str) -> GoogleUserInfo:
        if not self.client_id:
            raise ValueError("GOOGLE_CLIENT_ID is not configured")
        token = self._verify_token(credential)
        return self._create_user_info(token)

    def _verify_token(self, credential: str) -> dict:
        from google.auth.transport import requests
        from google.oauth2 import id_token
        return id_token.verify_oauth2_token(credential, requests.Request(), self.client_id)

    def _create_user_info(self, token: dict) -> GoogleUserInfo:
        if not token.get("email_verified"):
            raise ValueError("Google email is not verified")
        return GoogleUserInfo(token["email"], token.get("given_name", ""), token.get("family_name", ""))
