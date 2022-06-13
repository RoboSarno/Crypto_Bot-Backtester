import os
from twilio.rest import Client


class Twil:
    def __init__(self):
        """_summary_
            - init Twilio object variables
        """
        self.accountSid = os.environ.get('TWILIO_accountSid', '-1')
        self.authToken = os.environ.get('TWILIO_authToken', '-1')

    def buy_sig_hit(self, m):
        """_summary_
            - send buy sms message 
        Args:
            m (string): message to send
        """

        client = Client(self.accountSid, self.authToken)

        message = client.messages \
                        .create(
                            body=m,
                            from_='+16625038144',
                            to='+16619935567'
                        )   
                              
    def sell_sig_hit(self, m):
        """_summary_
            - send sell sms message 
        Args:
            m (string): message to send
        """
        client = Client(self.accountSid, self.authToken)

        message = client.messages \
                        .create(
                            body=m,
                            from_='+16625038144',
                            to='+16619935567'
                        )

