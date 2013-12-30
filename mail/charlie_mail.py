# Import smtplib for the actual sending function
import smtplib
from email.mime.text import MIMEText

class CharlieMail:
    def __init__(self, smtp_host, user, password, smtp_lib = smtplib):
        self.smtp = smtp_lib.SMTP(smtp_host)
        self.smtp.ehlo() # for tls add this line
        self.smtp.starttls() # for tls add this line
        self.smtp.ehlo() # for tls add this line
        self.smtp.login(user, password)
        
    def send_message(self, from_mail, to_mails = [], subject = "", body = ""):
        print "Charlie is carrying your message to the receiver... :)"
        # Create a text/plain message
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = from_mail
        msg['To'] = ", ".join(to_mails)
        self.smtp.sendmail(from_mail, to_mails, msg.as_string())
        self.smtp.quit()        
        print "Charlie has delivered your message. Give him a cookie! :)"
        return True
        

# ================================================================================

import unittest
from mockito import *
class TestCharlieMail(unittest.TestCase):

    def setUp(self):
        self.smtp_lib = mock()
        self.smtp = mock()
        when(self.smtp_lib).SMTP("smtp.gmail.com").thenReturn(self.smtp)
        self.cm = CharlieMail("smtp.gmail.com", "igordeoliveirasa@gmail.com", "123mudar!", smtp_lib = self.smtp_lib)
        verify(self.smtp).starttls()
        verify(self.smtp).login("igordeoliveirasa@gmail.com", "123mudar!")

    def test_send_message(self):
        self.cm.send_message(
            "igordeoliveirasa@gmail.com", 
            ["igordeoliveirasa@gmail.com", "igor.sa@gastecnologia.com.br"], 
            "This is the subject...", 
            "This is the body of the message!"
        )
        ret = verify(self.smtp).sendmail("igordeoliveirasa@gmail.com", 
                                   ["igordeoliveirasa@gmail.com", "igor.sa@gastecnologia.com.br"], 
                                   "This is the body of the message!")
        verify(self.smtp).quit()
        self.assertTrue(ret)

if __name__ == "__main__":
    unittest.main()