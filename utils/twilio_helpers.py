import os
from dataclasses import dataclass, field

from twilio.rest import Client


@dataclass
class TwilioAPI:
    account_sid: str = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token: str = os.getenv('TWILIO_TOKEN')
    client: Client = field(init=False)

    def __post_init__(self):
        self.client = Client(self.account_sid, self.auth_token)


    def send_sms(self,
                 from_number: str,
                 to_number: str,
                 message: str):
        '''
        Send an SMS using Twilio API
        :param from_number: Should have this format: +17863221234
        :param to_number:  Should have this format: +18293101390
        :return: Response from Twilio
        '''

        # client = Client(self.account_sid, self.auth_token)

        response = 'Success'

        try:
            twilio_response = self.client.messages.create(
                to=to_number,
                from_=from_number,
                body=message,
                persistent_action=['abcd12345'],
            )

        except Exception as e:
            response = 'ERROR sending the message.\n'
            response += str(e)

        return response

    def send_mms(self,
                 from_number: str,
                 to_number: str,
                 message: str,
                 media_url: str):
        '''
        Send an MMS using Twilio API
        :param from_number: Should have this format: +17863221909
        :param to_number:  Should have this format: +18293101545
        :param message:  MMS body text
        :param media_url:  URL of the image
        :return: Response from Twilio
        '''

        client = Client(self.account_sid, self.auth_token)

        response = 'Success'

        try:
            twilio_response = client.messages.create(
                to=to_number,
                from_=from_number,
                body=message,
                media_url=[media_url],
            )

        except Exception as e:
            response = 'ERROR sending the message.\n'
            response += str(e)

        return response

    def call(self,
             from_number: str,
             to_number: str,
             message: str):
        '''
        Make a call and say something using Twilio API
        :param from_number: Should have this format: +17863221909
        :param to_number:  Should have this format: +18293101545
        :return: Response from Twilio
        '''

        # client = Client(self.account_sid, self.auth_token)

        response = 'Success'

        # twiml = '<Response>'
        # twiml += '<Gather action="https://daian3.loca.lt/manychat/apps/twilio-empty/?message=hello" method="POST" timeout="10" numDigits="1">'
        # twiml += '<Say>Here is some information, to repeat it press #</Say>'
        # twiml += '</Gather>'
        # twiml += '</Response>'

        try:
            twilio_response = self.client.calls.create(
                twiml=f'<Response><Say>{message}</Say></Response>',
                # twiml=twiml,
                to=to_number,
                from_=from_number,
            )
            print(twilio_response)

        except Exception as e:
            response = 'ERROR making the phone call.\n'
            response += str(e)

        else:
            print('ok')

        return response
