# **IMAP OAuth2 Viewer — Multi-User Gmail & Outlook Client**

A full-stack email platform that supports **multi-user authentication**, **multi-account OAuth2 email connections**, and **asynchronous IMAP mail retrieval** for Gmail and Outlook.

The system consists of:

* **Streamlit Frontend** — Login UI, account management, email viewer
* **FastAPI Backend** — OAuth2 flows, token storage + encryption, access-token refresh
* **Async IMAP Engine** — Fast parallel IMAP email fetching
* **SQLite Database** (default) — Users & Email Accounts
* **AES-GCM Encryption** for refresh tokens

---

## 🚀 **Features**

### **User & Account Management**

* Login / Register (bcrypt password hashing)
* Each user can connect **multiple Gmail or Outlook accounts**
* Secure encrypted storage of refresh tokens (AES-256-GCM)

### **OAuth2 Support**

* **Google OAuth** (Gmail IMAP)
* **Microsoft OAuth** (Outlook / Office365 IMAP)
* Backend securely exchanges refresh tokens for access tokens
* No secrets are exposed to the frontend

### **Async IMAP Email Fetching**

* Super fast & efficient
* Supports XOAUTH2 for Gmail & Outlook
* Fetches latest emails + attachments
* Parses full MIME message → text, HTML, attachments

### **Frontend (Streamlit)**

* Login system
* Add Gmail/Outlook accounts via OAuth
* Select an account → fetch emails
* Tabs:

  * Overview
  * Text
  * HTML
  * Attachments
  * Raw JSON
* Works in both Dark & Light mode

---

## 🏗 **Architecture**

```
Streamlit UI  ←→  FastAPI Backend  ←→  Gmail / Microsoft OAuth
     │                   │
     │                   └──► Stores encrypted refresh tokens
     │
     └──► Requests access token per account
                         │
                         └──► AsyncIMAPClient fetches email
```

---

## ⚙️ **Environment Variables**

Create a **.env** file in the project root:

```env
##############################################
# Frontend & Backend
##############################################
FRONTEND_URL=http://localhost:8501
BACKEND_URL=http://localhost:8000

##############################################
# Database
##############################################
DATABASE_URL=sqlite:///./app.db

##############################################
# Encryption
# Generate using the command below
##############################################
TOKEN_ENCRYPTION_KEY=YOUR_GENERATED_KEY_HERE

##############################################
# Google OAuth (Gmail)
##############################################
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/oauth/google/callback

##############################################
# Microsoft OAuth (Outlook)
##############################################
OUTLOOK_CLIENT_ID=your-outlook-client-id
OUTLOOK_CLIENT_SECRET=your-outlook-client-secret
OUTLOOK_TENANT_ID=your-tenant-id
OUTLOOK_REDIRECT_URI=http://localhost:8000/oauth/outlook/callback
```

### Generate a secure token encryption key:

```python
import secrets, base64
print(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode())
```

---

## 🔧 **Installation**

### 1️⃣ Install dependencies

```
uv sync
```

### 2️⃣ Start FastAPI backend

```
cd src/backend
fastapi dev main.py
```

Backend:
👉 [http://localhost:8000](http://localhost:8000)
Docs:
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

### 3️⃣ Start Streamlit frontend

```
streamlit run app.py
```

Frontend:
👉 [http://localhost:8501](http://localhost:8501)

---

## 🔐 OAuth Setup

### 🔵 Google OAuth Setup (Gmail IMAP)

1. Create a project → [https://console.cloud.google.com](https://console.cloud.google.com)
2. Enable **Gmail API**
3. OAuth consent screen → External
4. Add scopes:

```
https://mail.google.com/
openid
email
profile
offline_access
```

5. Create OAuth client → Desktop app
6. Add redirect URI:

```
http://localhost:8000/oauth/google/callback
```

7. Paste **client ID + secret** into `.env`

---

### 🟣 Outlook OAuth Setup (Microsoft Azure)

1. Azure Portal → App Registrations → New

2. Supported account types:
   ✔ Personal Microsoft Accounts
   ✔ Work/School Accounts

3. Add redirect:

```
http://localhost:8000/oauth/outlook/callback
```

4. Authentication tab:
   ✔ Allow public client flows
   ✔ Allow Authorization Code flow

5. Expose API → Add scopes:

```
offline_access
openid
email
profile
IMAP.AccessAsUser.All
```

6. Paste into `.env`:

* `OUTLOOK_CLIENT_ID`
* `OUTLOOK_CLIENT_SECRET`
* `OUTLOOK_TENANT_ID=common`

---

## 🧪 **Usage Flow**

### Step 1 — Login / Register on Streamlit

Uses bcrypt password hashing.

### Step 2 — Connect Gmail / Outlook account

The app shows two buttons:

* **Connect Gmail**
* **Connect Outlook**

This opens OAuth login in a **popup**.
After successful authorization:

* Backend stores the refresh token (encrypted)
* Account appears in your sidebar list

### Step 3 — Fetch Emails

Select account → Click “Connect & Fetch”
Emails load fast using async IMAP.

---

## 🛡 Security Notes

* Refresh tokens stored encrypted with AES-256-GCM
* Only backend handles token exchange
* Frontend never receives refresh tokens
* Passwords hashed using bcrypt
* Tokens rotate automatically when expired
* Multi-tenant safe design

---

## 🧩 Optional Future Enhancements

* Webhooks for new mail notifications
* Per-user IMAP caching
* PostgreSQL support
* Dockerized deployment
* Admin dashboard

---

## 🙌 **Credits**

Built with:

* FastAPI
* Streamlit
* SQLAlchemy
* Aiosmtpd / IMAP Async
* Passlib (bcrypt)
