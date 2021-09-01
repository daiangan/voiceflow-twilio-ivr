import json
from dataclasses import dataclass, field
from typing import Literal

import requests


@dataclass
class VoiceFlowMessage:
    type: Literal[
        'text',
        'audio',
        'choices',
        'call_forwarding',
        'end'
    ]
    data: object = lambda: None


@dataclass
class VoiceFlow:
    api_base_url = 'https://general-runtime.voiceflow.com/'
    vf_id: str
    vf_api_key: str
    user_id: str
    headers: dict = field(init=False)

    def __post_init__(self):
        self.headers = {
            'Authorization': self.vf_api_key,
        }

    def interact(self,
                 content_type: str = 'text',
                 user_input: str = '') -> list:

        url = f'{self.api_base_url}state/{self.vf_id}/user/{self.user_id}/interact'

        request = {
            'type': content_type,
        }

        if content_type == 'text':
            request['payload'] = user_input

        headers = {
            'Authorization': self.vf_api_key
        }

        response = requests.post(
            url,
            json={
                'request': request
            },
            headers=headers,
        )

        vf_response = json.loads(response.text)

        messages = []

        for item in vf_response:
            message = None

            if item['type'] == 'speak':
                if item['payload']['type'] == 'message':
                    text_message = item['payload']['message']
                    if 'call_forwarding' in item['payload']['message']:
                        message = VoiceFlowMessage(
                            type='call_forwarding',
                            data=text_message[text_message.find(':') + 1:],
                        )

                    else:
                        message = VoiceFlowMessage(
                            type='text',
                            data=text_message,
                        )

                elif item['payload']['type'] == 'audio':
                    message = VoiceFlowMessage(
                        type='audio',
                        data=item['payload']['src']
                    )

            elif item['type'] == 'choice':
                message = VoiceFlowMessage(
                    type='choices',
                    data=item['payload']['buttons']
                )

            elif item['type'] == 'end':
                message = VoiceFlowMessage(
                    type='end',
                )

            if message:
                messages.append(message)

        return messages

    def fetch_state(self):
        url = f'{self.api_base_url}state/{self.vf_id}/user/{self.user_id}'

        headers = {
            'Authorization': self.vf_api_key
        }

        response = requests.get(
            url,
            headers=headers
        )

        results = json.loads(response.text)

        return results

    def update_variable(self, variable_name, variable_value):
        url = f'{self.api_base_url}state/{self.vf_id}/user/{self.user_id}/variables'
        request = {
            variable_name: variable_value,
        }

        headers = {
            'Authorization': self.vf_api_key
        }

        response = requests.patch(
            url,
            json=request,
            headers=headers
        )

        results = json.loads(response.text)

        return results
