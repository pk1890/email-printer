import imaplib, cups, email, nltk, re

imap_server="imap.poczta.onet.pl"
login="mlekotest123@onet.pl"
password="Mleko123"

conn = imaplib.IMAP4_SSL(imap_server)
conn.login(login, password)

status, messages = conn.select('INBOX')    

mail_text=""
f=open("/tmp/emailMessage.txt", "w+")

if status != "OK":
  print("Incorrect mail box")
  exit()
(retcode, messages) = conn.search(None, '(UNSEEN)')
if retcode == 'OK':
  for num in messages[0].split(' '):
    type, data = conn.fetch(num, '(RFC822)')
    msg = email.message_from_string(data[0][1])
    for payload in msg.walk():
      if payload.get_content_type().lower() == 'text/plain':
        mail_text=payload.get_payload()


###################
    f.write("date: " +  msg['date'] +"\n")
    f.write("subject: " +  msg['subject'] +"\n")
    f.write("from: " +  msg['from'] + "\n")
    f.write("________________________" + "\n")
###################
    f.write(mail_text)
    f.write("==================================" + "\n\n")



f.close()
cupsConn = cups.Connection()

cupsConn.printFile("thermal", "/tmp/emailMessage.txt", " ", {"cpi": "23", "lpi": "10"})
