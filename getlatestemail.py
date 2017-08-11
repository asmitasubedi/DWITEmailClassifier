import imaplib
import csv
import io
import email
import re

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('asmita.subedi@deerwalk.edu.np', 'Iam@smita123')
mail.list()
# Out: list of "folders" aka labels in gmail.
mail.select("inbox") # connect to inbox.

result, data = mail.uid('search', None, '(UNSEEN)') # search and return uids instead
# search and return uids instead
i = len(data[0].split()) # data[0] is a space separate string
for x in range(i):
 latest_email_uid = data[0].split()[x] # unique ids wrt label selected

 result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
 # fetch the email body (RFC822) for the given ID
 raw_email = email_data[0][1]

 #continue inside the same for loop as above
 raw_email_string = raw_email
 email_message = email.message_from_bytes(raw_email_string)
 output = io.StringIO()
 with open("hello.csv", "a", newline='', encoding='utf8') as file:
  writer = csv.writer(file)
  for part in email_message.walk():
   if part.get_content_type() == "text/plain":  # ignore attachments/html
    body = part.get_payload(None, True)
    row = str(body)[1:]
    row = row.replace("\\n", " ").replace("\\r", "").replace("\\t", "").replace("\\xe1\\x90\\xa7", " ").replace("*", " ").replace("\\xc2\\xa9", " ").replace("\\xe2\\x80\\x99"," ").replace("\\xe2\\x80\\x93", " ").replace("\\xe2\\x80\\x8b", " ").replace("\\xe2\\x80\\xa2", " ")
    #row = re.sub(r'[\t\n\r]+', ' ', row)
    #print(row)
    writer.writerow([row])
   else:
    continue