

# **Gmail IMAP OAuth Environment Variable Setup Guide**

This document provides a step-by-step guide for generating all required environment variables to enable IMAP access for Gmail using OAuth 2.0 authentication. Follow each section carefully to ensure a complete and secure configuration.

---

## **Required Environment Variables**

Add the following variables to your `.env` file:

```env
GMAIL_CLIENT_ID=
GMAIL_CLIENT_SECRET=
GMAIL_ACCESS_TOKEN=
GMAIL_REFRESH_TOKEN=
GMAIL_EMAIL=
```

Each variable is explained in the sections below.

---

## **1. Enable IMAP in Gmail**

IMAP must be enabled in your Gmail account for the application to read emails.

**Steps:**

1. Open Gmail.
2. Navigate to **Settings → See all settings**.
3. Open the **Forwarding and POP/IMAP** tab.
4. Under **IMAP Access**, select **Enable IMAP**.
5. Save your changes.

This step is mandatory. IMAP authentication will fail if it is not enabled.

---

## **2. Create a Google Cloud Project**

1. Open the Google Cloud Console:
   [https://console.cloud.google.com](https://console.cloud.google.com)
2. Click **New Project**.
3. Enter a project name and (optionally) organization.
4. Click **Create**.
5. Select the newly created project.

---

## **3. Enable the Gmail API**

1. Navigate to **APIs & Services → Enable APIs and Services**.
2. Search for **Gmail API**.
3. Select it and click **Enable**.

---

## **4. Configure the OAuth Consent Screen**

1. Go to **APIs & Services → OAuth Consent Screen**.
2. Select the **External** user type.
3. Provide the required application information.
4. Under **Scopes**, click **Add or Remove Scopes**.
5. Add the following recommended scopes:

   * `userinfo.email`
   * `userinfo.profile`
   * `gmail.modify`
6. Save and proceed.
7. You may keep the app in **Testing** mode.

---

## **5. Create an OAuth Client (Desktop Application)**

1. Go to **APIs & Services → Credentials**.
2. Click **Create Credentials → OAuth Client ID**.
3. Choose **Desktop App** as the application type.
4. Enter a name and click **Create**.
5. Download the OAuth client JSON file.

From the downloaded file, copy:

* `client_id`
* `client_secret`

Add them to your `.env` file:

```env
GMAIL_CLIENT_ID=<client_id>
GMAIL_CLIENT_SECRET=<client_secret>
```

---

## **6. Generate Access and Refresh Tokens**

Run your Gmail OAuth script:

```bash
python -m src.gmail_oauth
```

A browser window will open prompting you to log in and authorize access.

After successful authorization, the script will output:

```
GMAIL_ACCESS_TOKEN=...
GMAIL_REFRESH_TOKEN=...
```

Insert both values into your `.env` file.

---

## **7. Add Your Gmail Address**

Include your Gmail account email:

```env
GMAIL_EMAIL=your_email@gmail.com
```

---

## **8. Example `.env` File**

```env
# Gmail OAuth
GMAIL_CLIENT_ID=1234567890-abc123.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=ABCXYZ12345
GMAIL_ACCESS_TOKEN=ya29.a0AfH6...
GMAIL_REFRESH_TOKEN=1//0gdfsg34...
GMAIL_EMAIL=yourname@gmail.com
```

---

