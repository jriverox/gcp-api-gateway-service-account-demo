import time
from dotenv import load_dotenv
import os
import google.auth.crypt
import google.auth.jwt

load_dotenv()

def generate_jwt(
    sa_keyfile,
    sa_email="account@project-id.iam.gserviceaccount.com",
    audience="your-service-name",
    expiry_length=3600,
):
    """Generates a signed JSON Web Token using a Google API Service Account."""
    now = int(time.time())
    # build payload
    payload = {
        "iat": now,
        # expires after 'expiry_length' seconds.
        "exp": now + expiry_length,
        # iss must match 'issuer' in the security configuration in your
        # swagger spec (e.g. service account email). It can be any string.
        "iss": sa_email,
        # aud must be either your Endpoints service name, or match the value
        # specified as the 'x-google-audience' in the OpenAPI document.
        "aud": audience,
        # sub and email should match the service account's email address
        "sub": sa_email,
        "email": sa_email,
    }
    # sign with keyfile
    signer = google.auth.crypt.RSASigner.from_service_account_file(sa_keyfile)
    jwt = google.auth.jwt.encode(signer, payload)

    return jwt

print(generate_jwt(
    sa_keyfile = os.getenv("SERVICE_ACCOUNT_KEY_FILE"),
    sa_email = os.getenv("SERVICE_ACCOUNT_EMAIL"),
    audience = os.getenv("AUDIENCE"),
    expiry_length = 3600
))