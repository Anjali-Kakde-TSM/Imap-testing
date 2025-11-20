import msal
from src.utils import env

SCOPES = ["https://outlook.office.com/IMAP.AccessAsUser.All"]

def generate_outlook_token():
    app = msal.PublicClientApplication(
        env("OUTLOOK_CLIENT_ID"),
        authority=f"https://login.microsoftonline.com/{env('OUTLOOK_TENANT_ID')}"
    )

    result = app.acquire_token_interactive(SCOPES)

    print("\n--- SAVE INTO .env ---")
    print("OUTLOOK_ACCESS_TOKEN=", result["access_token"])
