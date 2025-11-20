# **Guide to Generating Environment Variables for Gmail and Outlook IMAP Access**

This document explains how to generate all the values required in your `.env` file for Gmail and Outlook IMAP access. Each section includes simple steps and clear descriptions.

---

## **1. Gmail OAuth Variables**

These values are needed to authenticate Gmail IMAP using OAuth.

### **Environment Variables**

```env
GMAIL_CLIENT_ID=
GMAIL_CLIENT_SECRET=
GMAIL_ACCESS_TOKEN=
GMAIL_REFRESH_TOKEN=
GMAIL_EMAIL=
```

### **Step 1: Create a Google Cloud Project**

1. Open [https://console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project
3. Select the project

### **Step 2: Enable Gmail API**

1. Go to “APIs and Services”
2. Search for “Gmail API”
3. Click “Enable”

### **Step 3: Create OAuth Client**

1. Go to “APIs and Services” → “Credentials”
2. Click “Create Credentials” → “OAuth Client ID”
3. Choose “Desktop App”
4. Download the OAuth client JSON file
5. Copy the following from the file:

   * `client_id`
   * `client_secret`

Update your `.env`:

```env
GMAIL_CLIENT_ID=<client_id>
GMAIL_CLIENT_SECRET=<client_secret>
```

### **Step 4: Generate Tokens**

Run your token script:

```bash
python -m src.gmail_oauth
```

After login, the script prints:

```
GMAIL_ACCESS_TOKEN=xxxx
GMAIL_REFRESH_TOKEN=yyyy
```

Copy both into `.env`.

### **Step 5: Add your Gmail address**

```env
GMAIL_EMAIL=your_email@gmail.com
```

---

## **2. Outlook OAuth Variables**

These are required to authenticate Outlook IMAP using OAuth.

### **Environment Variables**

```env
OUTLOOK_CLIENT_ID=
OUTLOOK_TENANT_ID=common
OUTLOOK_ACCESS_TOKEN=
OUTLOOK_EMAIL=
```

### **Step 1: Create an App in Azure**

1. Open [https://portal.azure.com](https://portal.azure.com)
2. Go to “Azure Active Directory”
3. Open “App Registrations”
4. Click “New registration”
5. Set supported account types to “Accounts in any organization”
6. Copy the Application (client) ID

Update `.env`:

```env
OUTLOOK_CLIENT_ID=<client-id>
```

### **Step 2: Add Tenant**

Always set:

```env
OUTLOOK_TENANT_ID=common
```

### **Step 3: Generate Access Token**

Run:

```bash
python -m src.outlook_oauth
```

After login, the script prints:

```
OUTLOOK_ACCESS_TOKEN=xxxxx
```

Copy it into `.env`.

### **Step 4: Add your Outlook Email**

```env
OUTLOOK_EMAIL=yourname@outlook.com
```

---

## **3. Outlook Password Option Without OAuth**

You can log in using a password or app password.

### **Environment Variable**

```env
OUTLOOK_PASSWORD=
```

### **Steps**

1. Open [https://account.live.com/proofs](https://account.live.com/proofs)
2. Turn on two-step verification
3. Open “App passwords”
4. Create a new app password
5. Place it in `.env`:

```env
OUTLOOK_PASSWORD=<app-password>
```

---

## **4. Example .env File**

```env
# Gmail OAuth
GMAIL_CLIENT_ID=xxxxxxxxx
GMAIL_CLIENT_SECRET=yyyyyyyyy
GMAIL_ACCESS_TOKEN=zzzzzzzzzz
GMAIL_REFRESH_TOKEN=rrrrrrrrrr
GMAIL_EMAIL=yourname@gmail.com

# Outlook OAuth
OUTLOOK_CLIENT_ID=aaaaaaaaaaa
OUTLOOK_TENANT_ID=common
OUTLOOK_ACCESS_TOKEN=bbbbbbbbbbb
OUTLOOK_EMAIL=yourname@outlook.com

# Outlook password-only option
OUTLOOK_PASSWORD=ccccccccccc
```

---


