import random, os, sys, smtplib
from email.message import EmailMessage
from email.utils import formatdate

translation_table = {
        "Ö": "Oe",
        "ö": "oe",
        "Ä": "Ae",
        "ä": "ae",
        "Ü": "Ue",
        "ü": "ue"
}

def sendemail():
        TEXT1 = "Liebe(r) Bewohner/in !\n\nfolgende Kennung haben wir für den Zugriff auf den Bewohnerchat erstellt:\n"
        TEXT2 = "Benutzername=" + account + "\nPasswort=" + password + "\n\nFür den Zugriff per Browser oder als Site für die App die URL:\nhttps://messenger.prinzjochum.de/\n"
        TEXT3 = "Falls das Passwort nicht funktioniert oder vergessen wurde - einfach mit der persönlichen eMailadresse zurücksetzen lassen:\nhttps://messenger.prinzjochum.de/reset_password\n\nund hier nochmal die wi$
        TEXT = TEXT1 + TEXT2 + TEXT3
        #
        MAIL_SERVER = 'mail.privateemail.com'
        TO_ADDRESS = email
        FROM_ADDRESS = 'admin@prinzjochum.de'
        REPLY_TO_ADDRESS = 'pep-ag-it@ml.wogeno.de'
        SUBJECT = 'PEP Bewohnermessenger Anmeldung'
        #
        #msg = email.mime.multipart.MIMEMultipart()
        msg = EmailMessage()
        msg.set_content(TEXT)
        msg['to'] = TO_ADDRESS
        msg['from'] = FROM_ADDRESS
        msg['subject'] = SUBJECT
        msg.add_header('reply-to', REPLY_TO_ADDRESS)
        msg["Date"] = formatdate(localtime=True)
        server = smtplib.SMTP(MAIL_SERVER, 587)
        server.starttls()
        server.login('admin@prinzjochum.de','YBcvjqYjWAyPndKgqCPj')
        try:
                server.sendmail(msg['from'], [msg['to']], msg.as_string())
                print ('email sent to=' + msg['to'])
        except:
                print ('error sending mail')
        server.quit()


def codegenerator():
        alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-!"
        pw_length = 6
        mypw = ""
        for i in range(pw_length):
                next_index = random.randrange(len(alphabet))
                mypw = mypw + alphabet[next_index]
        return mypw

##
f = open('input','r')
myFile = open('output', 'w') # or 'a' to add text instead of truncate
int = 0

for l in f:
        if int == 0:
                #skip header in file
                print ("reading input file")
        else:
                fields = l.split()
                prename = fields[1].translate(str.maketrans(translation_table))
                surname = fields[2].translate(str.maketrans(translation_table))
                email = fields[0]
                account = (prename.lower() + "." + surname.lower())
                password = codegenerator()
                #print(prename,surname,email,account,passwd)
                cmd = "Nr." + str(int) + " Benutzer=" + account + " Password=" + password + " eMail=" + email
                print(cmd)
                myFile.write(cmd + "\n")
                sendemail()
                cmd = "/opt/mattermost/bin/mattermost user create --email " + email + " --firstname " + prename + " --lastname " + surname + " --locale de --username " + account + " --password " + password
                os.system(cmd)
                cmd = "/opt/mattermost/bin/mattermost team add wogeno-peup " + account
                os.system(cmd)
                cmd = "/opt/mattermost/bin/mattermost channel add wogeno-peup:town-square " + account
                os.system(cmd)
                cmd = "/opt/mattermost/bin/mattermost channel add wogeno-peup:wichtige-ankundigungen " + account
                os.system(cmd)
                cmd = "/opt/mattermost/bin/mattermost user verify " + account
                os.system(cmd)
        int = int + 1
myFile.close()
