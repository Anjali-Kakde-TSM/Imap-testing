from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://mail.google.com/"]

def generate_gmail_oauth():
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    creds = flow.run_local_server(port=0,
                                 authorization_prompt_message="Please authorize the app.",
                                 authorization_url_params={"access_type": "offline", "prompt": "consent"})
    print("\n--- SAVE THESE INTO .env ---")
    print("GMAIL_ACCESS_TOKEN=", creds.token)
    print("GMAIL_REFRESH_TOKEN=", creds.refresh_token)
    
if __name__ == "__main__":
    generate_gmail_oauth()
