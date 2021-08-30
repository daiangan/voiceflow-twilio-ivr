import json
from dataclasses import dataclass, field

import requests


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

    def send_content(self,
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

        results = json.loads(response.text)
        print(json.dumps(results, indent=4, sort_keys=True))

        messages = []

        for result in results:
            if result['type'] == 'speak':
                if result['payload']['type'] == 'message':
                    if 'call_forwarding' in result['payload']['message']:
                        text_message = result['payload']['message']
                        messages.append(
                            {
                                'type': 'call_forwarding',
                                'phone': text_message[text_message.find(':') + 1:],
                            }
                        )

                    else:
                        messages.append(
                            {
                                'type': 'text',
                                'message': result['payload']['message'],
                            }
                        )

                elif result['payload']['type'] == 'audio':
                    messages.append(
                        {
                            'type': 'audio',
                            'url': result['payload']['src'],
                        }
                    )

            elif result['type'] == 'choice':
                messages.append(
                    {
                        'type': 'choices',
                        'choices': result['payload']['buttons'],
                    }
                )

            elif result['type'] == 'path':
                messages.append(
                    {
                        'type': 'path',
                    }
                )

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
        print(json.dumps(results, indent=4, sort_keys=True))

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
        # print(json.dumps(results, indent=4, sort_keys=True))

        return results
