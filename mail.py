import imaplib
import email
from email.header import decode_header
import time

IMAP_SERVER = "email.koreatech.ac.kr"
EMAIL_ACCOUNT = "woosangbyum@koreatech.ac.kr"
PASSWORD = "Pear1595!"

def check_new_mails(seen_uids):
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, PASSWORD)
        mail.select("INBOX")

        status, messages = mail.search(None, "UNSEEN")  # 읽지 않은 메일만

        new_uids = set(messages[0].split()) - seen_uids
        for uid in new_uids:
            status, data = mail.fetch(uid, "(RFC822)")
            msg = email.message_from_bytes(data[0][1])
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8", errors="ignore")
            from_ = msg.get("From")
            date = msg.get("Date")

            print("📩 새 메일 도착!")
            print("From:", from_)
            print("Subject:", subject)
            print("Date:", date)
            print("-" * 50)

        return seen_uids.union(new_uids)
    except Exception as e:
        print("⚠️ 에러 발생:", e)
        return seen_uids

# 🕒 반복적으로 실행
seen_uids = set()
print("📡 메일 수신 대기 중... (Ctrl+C로 종료)")
try:
    while True:
        seen_uids = check_new_mails(seen_uids)
        time.sleep(30)  # 30초마다 체크
except KeyboardInterrupt:
    print("⏹ 종료합니다.")