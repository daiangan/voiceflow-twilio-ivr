from flask import Flask, request, jsonify, Response
import os
from twilio.twiml.voice_response import VoiceResponse, Client, Dial
from utils.voiceflow_helpers import VoiceFlow
from utils.twilio_helpers import TwilioAPI

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        request_data = request.get_json()
        print(request_data)

        print(request.data)
        print(request.json)
        print(request.args)
        print(request.form)
        print(request.form['From'])

        response = {
            'status': 'ok',
        }

        language = 'en-US'
        voice = 'alice'

        tw_resp = VoiceResponse()
        # tw_resp.say(
        #     message='Hi, this is Alice answering your call.',
        #     voice=voice,
        #     language=language,
        # )

        vf = VoiceFlow(
            vf_id=os.getenv('VF_PROJECT_VERSION_ID'),
            vf_api_key=os.getenv('VF_API_KEY'),
            user_id=request.form['From'],
        )



        vf_messages = []

        if request.form['CallStatus'] == 'ringing':
            vf_messages = vf.send_content(content_type='launch')

        else:
            if 'Digits' in request.form:
                digits = request.form['Digits']

                choices = vf.fetch_state()['variables']['choices']

                if choices != 0:
                    choices = choices.split('|')
                    print(choices)
                    if len(choices) >= int(digits):
                        print(f'GOING TO SAY: {choices[int(digits) - 1]}')
                        vf_messages = vf.send_content(
                            user_input=choices[int(digits) - 1]
                        )
                        vf.update_variable(
                            variable_name='choices',
                            variable_value=0,
                        )

                else:
                    vf_messages = vf.send_content(user_input=digits)

            elif 'SpeechResult' in request.form:
                vf_messages = vf.send_content(user_input=request.form['SpeechResult'])



        for message in vf_messages:
            print(message)
            if message['type'] == 'text':
                tw_resp.say(
                    message=message['message'],
                    voice=voice,
                    language=language,
                )

            elif message['type'] == 'audio':
                tw_resp.play(
                    url=message['url'],
                    # loop=0,
                )

            elif message['type'] == 'choices':
                # bot_user.temp_data = '|'.join(choice['name'] for choice in message['choices'])
                # bot_user.save()
                vf.update_variable(
                    variable_name='choices',
                    variable_value='|'.join(choice['name'] for choice in message['choices']),
                )

            elif message['type'] == 'call_forwarding':
                tw_resp.dial(message['phone'])




        tw_resp.gather(
            input='dtmf speech',
            language=language,
            timeout=4,
            # speech_timeout=15,
            speech_model='numbers_and_commands',  # default, numbers_and_commands, phone_call
            # num_digits=1,
            finish_on_key='#',
            enhanced=True,
        )

        # tw = TwilioAPI()


        # dial = Dial()
        # client = Client()
        # client = tw.client
        # client.identity('user_jane')
        # client.identity(request.form['CallSid'])
        # client.parameter(name='FirstName', value='Jane')
        # client.parameter(name='LastName', value='Doe')
        # dial.append(client)
        # tw_resp.append(client)
        # print(tw_resp)

        return str(tw_resp)

        # return jsonify(response)

    else:
        return 'I am alive!'


if __name__ == '__main__':
    app.run()
