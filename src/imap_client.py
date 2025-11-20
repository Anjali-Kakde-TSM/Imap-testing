import imaplib


class IMAPClient:
    """Unified IMAP Client for Gmail + Outlook."""

    GMAIL_IMAP = "imap.gmail.com"
    OUTLOOK_IMAP = "outlook.office365.com"

    def __init__(self, provider, email, credential, use_oauth=True):
        self.provider = provider.lower()
        self.email = email
        self.credential = credential
        self.use_oauth = use_oauth
        self.imap = None

    def connect(self):
        if self.provider == "gmail":
            return self._connect_gmail_oauth()

        if self.provider == "outlook":
            return self._connect_outlook()

        raise Exception("Unsupported provider")

    # ---------------- Gmail OAuth ----------------
    def _connect_gmail_oauth(self):
        try:
            self.imap = imaplib.IMAP4_SSL(self.GMAIL_IMAP)
            auth_string = self._oauth_string()

            self.imap.authenticate("XOAUTH2", lambda x: auth_string)
            self.imap.select("INBOX")

            print("Gmail IMAP connected (OAuth2)")
            return self.imap

        except Exception as e:
            raise Exception(f"Gmail OAuth IMAP failed: {e}")

    # ---------------- Outlook ----------------
    def _connect_outlook(self):
        try:
            self.imap = imaplib.IMAP4_SSL(self.OUTLOOK_IMAP)

            if self.use_oauth:
                auth_string = self._oauth_string()
                self.imap.authenticate("XOAUTH2", lambda x: auth_string)
                print("Outlook IMAP connected (OAuth2)")
            else:
                self.imap.login(self.email, self.credential)
                print("Outlook IMAP connected (password login)")

            self.imap.select("INBOX")
            return self.imap

        except Exception as e:
            raise Exception(f"Outlook IMAP failed: {e}")

    def _oauth_string(self):
        return f"user={self.email}\1auth=Bearer {self.credential}\1\1"

    # ---------------- Fetch latest emails ----------------
    def fetch_latest(self, limit=5):
        status, msg_ids = self.imap.search(None, "ALL")
        msg_ids = msg_ids[0].split()[-limit:]

        emails = []
        for mid in msg_ids:
            _, msg_data = self.imap.fetch(mid, "(RFC822)")
            emails.append(msg_data[0][1])
        return emails
