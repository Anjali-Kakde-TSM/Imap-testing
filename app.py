import time
import mimetypes
import streamlit as st
from src.imap_client import IMAPClient
from src.email_parser import EmailParser
from src.utils import env

st.set_page_config(page_title="IMAP Email Viewer POC", layout="wide")

st.title("IMAP Email Viewer")

# -------------------- Sidebar: Connection Settings --------------------
with st.sidebar.form("conn_form"):
    st.header("Connection Settings")

    provider = st.selectbox("Provider", ["gmail", "outlook"]) 
    use_env = st.checkbox("Use credentials from .env (recommended)", value=True)

    # Load credentials
    if use_env:
        try:
            if provider == "gmail":
                email_addr = env("GMAIL_EMAIL")
                credential = env("GMAIL_ACCESS_TOKEN")
            else:
                email_addr = env("OUTLOOK_EMAIL")
                credential = env("OUTLOOK_PASSWORD") if env("OUTLOOK_PASSWORD") else env("OUTLOOK_ACCESS_TOKEN")
        except Exception as e:
            st.error(f"Failed to load from .env: {e}")
            email_addr = st.text_input("Email")
            credential = st.text_input("Credential", type="password")
    else:
        email_addr = st.text_input("Email")
        credential = st.text_input("Credential (access token or password)", type="password")

    use_oauth = st.checkbox("Use OAuth (XOAUTH2)", value=True)
    fetch_limit = st.slider("Fetch latest N emails", min_value=1, max_value=50, value=10)

    connect_btn = st.form_submit_button("Connect & Fetch")

# -------------------- Session State Setup --------------------
if "connected" not in st.session_state:
    st.session_state.connected = False
if "imap_obj" not in st.session_state:
    st.session_state.imap_obj = None
if "parsed_messages" not in st.session_state:
    st.session_state.parsed_messages = []

# -------------------- Connect + Fetch Function --------------------
def connect_and_fetch(provider, email_addr, credential, use_oauth, limit):
    try:
        start = time.time()

        client = IMAPClient(provider=provider, email=email_addr, credential=credential, use_oauth=use_oauth)
        client.connect()
        raw_list = client.fetch_latest(limit)
        parsed = [EmailParser.parse(raw) for raw in raw_list]

        end = time.time()
        total_time = round(end - start, 2)

        st.session_state.imap_obj = client
        st.session_state.parsed_messages = parsed
        st.session_state.connected = True

        st.success(f"Connected to {provider} as {email_addr} — fetched {len(parsed)} emails in {total_time} seconds")

    except Exception as e:
        st.session_state.connected = False
        st.session_state.imap_obj = None
        st.session_state.parsed_messages = []
        st.error(f"Connection or fetch failed: {e}")


if connect_btn:
    connect_and_fetch(provider, email_addr, credential, use_oauth, fetch_limit)

# -------------------- Main UI: Email List + Viewer --------------------
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Inbox — Latest Emails")

    if not st.session_state.connected:
        st.info("Not connected. Use the sidebar to connect and fetch emails.")

    else:
        parsed = st.session_state.parsed_messages
        options = [
            f"{i+1}. {m['subject'] or '(no subject)'} — {m['from']}"
            for i, m in enumerate(parsed)
        ]

        # ⭐ START TIMER FOR EMAIL PREVIEW
        preview_start = time.time()

        selected = st.selectbox("Select message", options=options)
        selected_index = options.index(selected)
        msg = parsed[selected_index]

        # ⭐ END TIMER
        preview_time = round(time.time() - preview_start, 3)
        st.info(f"⏱ Email loaded in {preview_time} seconds")

        st.markdown("### Email Info")
        st.write({
            "Subject": msg["subject"],
            "From": msg["from"],
            "To": msg["to"],
            "Date": msg["date"],
            "Attachments": len(msg["attachments"])
        })

        st.markdown("---")
        st.subheader("Plain Text")
        st.code(msg.get("text", "")[:4000] or "(no plain text)")

        st.subheader("HTML Preview")
        if msg.get("html"):
            st.markdown(msg["html"], unsafe_allow_html=True)
        else:
            st.info("No HTML body found.")

        # -------------------- Attachments Section --------------------
        if msg.get("attachments"):
            st.subheader("Attachments")

            for attachment in msg["attachments"]:
                fn = attachment.get("filename") or "attachment"
                size = attachment.get("size_kb", 0)
                content = attachment.get("content", b"")

                mime_type, _ = mimetypes.guess_type(fn)
                mime_type = mime_type or "application/octet-stream"

                st.write(f"📎 **{fn}** — {size} KB")

                st.download_button(
                    label=f"Download {fn}",
                    data=content,
                    file_name=fn,
                    mime=mime_type
                )

                st.markdown("**Preview:**")

                # IMAGE
                if mime_type.startswith("image/"):
                    st.image(content, caption=fn, use_column_width=True)

                # PDF
                elif mime_type == "application/pdf":
                    import base64
                    base64_pdf = base64.b64encode(content).decode("utf-8")
                    st.markdown(
                        f"""
                        <iframe src="data:application/pdf;base64,{base64_pdf}"
                        width="100%" height="600px"></iframe>
                        """,
                        unsafe_allow_html=True
                    )

                # TEXT
                elif mime_type.startswith("text/"):
                    st.code(content.decode("utf-8", errors="ignore"))

                # HTML
                elif mime_type == "text/html":
                    st.markdown(content.decode("utf-8", errors="ignore"), unsafe_allow_html=True)

                else:
                    st.info("Preview not available — download to view.")


with col2:
    st.subheader("Raw Parsed JSON (Debug)")
    if st.session_state.parsed_messages:
        st.json(st.session_state.parsed_messages[selected_index])
    else:
        st.info("No parsed messages to display.")

# -------------------- Footer --------------------
st.markdown("---")
st.caption("IMAP Viewer — Generated with Best Practices (Streamlit)")
