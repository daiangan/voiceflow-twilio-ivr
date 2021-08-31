import os

from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse

from utils.voiceflow_helpers import VoiceFlow

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        request_data = request.form
        print(request_data)

        language = 'en-US'
        voice = 'alice'

        tw_resp = VoiceResponse()

        vf = VoiceFlow(
            vf_id=os.getenv('VF_PROJECT_VERSION_ID'),
            vf_api_key=os.getenv('VF_API_KEY'),
            user_id=request_data['From'],
        )

        vf_messages = []

        if request_data['CallStatus'] == 'ringing':
            vf_messages = vf.interact(content_type='launch')

        else:
            if 'Digits' in request_data:
                digits = request_data['Digits']

                try:
                    choices = vf.fetch_state()['variables']['choices']
                except Exception as e:
                    print(e)
                else:
                    if choices != 0:
                        choices = choices.split('|')
                        if len(choices) >= int(digits):
                            vf_messages = vf.interact(
                                user_input=choices[int(digits) - 1]
                            )
                            vf.update_variable(
                                variable_name='choices',
                                variable_value=0,
                            )

                    else:
                        vf_messages = vf.interact(user_input=digits)

            elif 'SpeechResult' in request_data:
                vf_messages = vf.interact(
                    user_input=request_data['SpeechResult']
                )

        for message in vf_messages:
            if message.type == 'text':
                tw_resp.say(
                    message=message.data,
                    voice=voice,
                    language=language,
                )

            elif message.type == 'audio':
                tw_resp.play(
                    url=message.data,
                )

            elif message.type == 'choices':
                vf.update_variable(
                    variable_name='choices',
                    variable_value='|'.join(choice['name'] for choice in message.data),
                )

            elif message.type == 'call_forwarding':
                tw_resp.dial(message.data)

            elif message.type == 'end':
                tw_resp.hangup()

        tw_resp.gather(
            input='dtmf speech',
            language=language,
            timeout=5,
            # speech_timeout=15,
            speech_model='numbers_and_commands',
            # num_digits=1,
            finish_on_key='#',
            enhanced=True,
        )

        print(tw_resp)

        return str(tw_resp)

    else:
        return 'VoiceFlow - Twilio IVR'


if __name__ == '__main__':
    app.run()
