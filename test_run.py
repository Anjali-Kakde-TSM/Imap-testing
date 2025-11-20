from src.imap_client import IMAPClient
from src.email_parser import EmailParser
from src.utils import env


def show(parsed):
    print("\n=========================")
    print("Subject:", parsed["subject"])
    print("From:", parsed["from"])
    print("To:", parsed["to"])
    print("Text:", parsed["text"][:200], "...")
    print("HTML:", parsed["html"][:200], "...")
    print("Attachments:", len(parsed["attachments"]))

def run():
    print("\n--- GMAIL IMAP ---")
    gmail = IMAPClient(
        provider="gmail",
        email=env("GMAIL_EMAIL"),
        credential=env("GMAIL_ACCESS_TOKEN"),
        use_oauth=True
    )
    gmail.connect()
    for raw in gmail.fetch_latest(2):
        show(EmailParser.parse(raw))

    print("\n--- OUTLOOK IMAP ---")
    outlook = IMAPClient(
        provider="outlook",
        email=env("OUTLOOK_EMAIL"),
        credential=env("OUTLOOK_PASSWORD"),  # or OUTLOOK_ACCESS_TOKEN
        use_oauth=False
    )
    outlook.connect()
    for raw in outlook.fetch_latest(2):
        show(EmailParser.parse(raw))


if __name__ == "__main__":
    run()
