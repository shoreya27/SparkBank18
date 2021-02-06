from spark18bank.settings import sender_email, sender_pass
import smtplib, ssl
from email.message import EmailMessage

'''
This Module will be used to create an Email for Every Transaction done by User ---- Deposit/Withdraw
'''

port = 465
smtp_server = "smtp.gmail.com"
context = ssl.create_default_context()


class SendMailInterface:

    def __init__(self,amount,balance,receiver,deposit=False,withdraw=False):
        self.deposit = deposit
        self.withdraw = withdraw
        self.amount = amount
        self.message = None
        self.receiver = receiver
        self.balance = balance
        self.subject = None

        if self.deposit:
            self.depositmessage()
        elif self.withdraw:
            self.withdrawmessage()

    def depositmessage(self):
        self.message = '''This message is sent from SparkBank18.\nYour Account has been credited with {money}Rs,\nTotal Balance:{bal}\nThank You For choosing us!!.
                        '''.format(money=self.amount, bal=self.balance)
        self.subject = "Credited Amount"

    def withdrawmessage(self):
        self.message = '''This message is sent from SparkBank18.\nYour Account has been debited with {money}Rs,\nTotal Balance:{bal}\nThank You For choosing us!!.
                        '''.format(money=self.amount, bal=self.balance)
        self.subject = "Debited Amount"
    def sendmail(self):
        server = smtplib.SMTP_SSL(smtp_server, port)
        server.login(sender_email, sender_pass)
        msg = EmailMessage()
        msg.set_content(self.message)
        msg['Subject'] = self.subject
        msg['From'] = sender_email
        msg['To'] = self.receiver
        server.send_message(msg)
        server.quit()