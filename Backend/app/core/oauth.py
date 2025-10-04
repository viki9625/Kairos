from authlib.integrations.starlette_client import OAuth
from .config import settings

oauth = OAuth()

# This is the corrected configuration.
# Instead of using 'server_metadata_url' which was failing, we are providing
# the required authorization and token endpoints directly. This is a more
# robust method that avoids the failing network discovery call.
oauth.register(
    name='google',
    client_id=settings.google_client_id,
    client_secret=settings.google_client_secret,
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
    authorize_params=None,
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    refresh_token_url=None,
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
    client_kwargs={'scope': 'openid email profile'}
)

