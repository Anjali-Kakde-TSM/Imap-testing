import email
from email.header import decode_header


class EmailParser:

    @staticmethod
    def decode_mime(value):
        if not value: return ""
        parts = decode_header(value)
        decoded = ""
        for text, charset in parts:
            if isinstance(text, bytes):
                decoded += text.decode(charset or "utf-8", errors="ignore")
            else:
                decoded += text
        return decoded

    @staticmethod
    def parse(raw_bytes):
        msg = email.message_from_bytes(raw_bytes)

        parsed = {
            "subject": EmailParser.decode_mime(msg.get("Subject")),
            "from": EmailParser.decode_mime(msg.get("From")),
            "to": EmailParser.decode_mime(msg.get("To")),
            "date": msg.get("Date"),
            "text": "",
            "html": "",
            "attachments": []
        }

        for part in msg.walk():
            ctype = part.get_content_type()
            disp = str(part.get_content_disposition())

            if ctype == "text/plain" and "attachment" not in disp:
                parsed["text"] += part.get_payload(decode=True).decode("utf-8", errors="ignore")

            elif ctype == "text/html" and "attachment" not in disp:
                parsed["html"] += part.get_payload(decode=True).decode("utf-8", errors="ignore")

            elif disp == "attachment":
                filename = EmailParser.decode_mime(part.get_filename())
                content = part.get_payload(decode=True)
                parsed["attachments"].append({
                    "filename": filename,
                    "size_kb": round(len(content) / 1024, 2),
                    "content": content
                })

        return parsed
