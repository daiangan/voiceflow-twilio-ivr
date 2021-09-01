
<p align="center">
  <img src="https://ganmedia-projects.s3.amazonaws.com/voiceflow-twilio-ivr/header_image.jpg" alt="VoiceFlow - Twilio IVR"/>
</p>

## VoiceFlow - Twilio IVR
This is a Flask app to link your VoiceFlow project with your 
Twilio phone number and create an IVR.  

Go to VoiceFlow and grab your Project VERSION_ID and your API_KEY from 
the Integration tab.  
<img src="https://ganmedia-projects.s3.amazonaws.com/voiceflow-twilio-ivr/vf_api_key.jpg" width="450" alt="Voiceflow keys"/>


Add them to your Python environment variables with the names:  
```text
VF_PROJECT_VERSION_ID
VF_API_KEY
```

Deploy your Flask app (out of this scope) and copy your app URL.
  
Then go to Twilio and paste your app's URL as the webhook for the incoming calls 
to your phone number.  

<img src="https://ganmedia-projects.s3.amazonaws.com/voiceflow-twilio-ivr/twilio_webhook_setup.jpg" width="450" alt="Twilio webhook set up"/>


<br>

#### Settings
Change the following variables to your best options in [app.py](app.py):  
```python
language = 'en-US'
voice = 'alice'
timeout = 5
```

You also need to add a VoiceFlow variable named __choices__. 
This is important for the choices mapping to phone keypad input (more details in __Features__ below).

<br>

#### Features
1. The script will handle VF choices block to let you input each choice as
number options in the phone dial pad, and of course, keeping the voice input available.  
   <img src="https://ganmedia-projects.s3.amazonaws.com/voiceflow-twilio-ivr/keypad_mapping.jpg" width="350" alt="Choices mapping"/>  
   _Do not forget to add the __choices__ variable to your VF project._  
   


2. To forward a call, just use the text __call_forwarding__ followed by the phone 
number to redirect the call.  
   For example:  
   <img src="https://ganmedia-projects.s3.amazonaws.com/voiceflow-twilio-ivr/call_forwarding.jpg" width="350" alt="Call forwarding feature"/>


<br>

#### Known issues:
- __Audio support:__ The issue is that when you upload a file to VF using the Audio 
  block, the URL you get in the API is pointing to an __application/octet-stream__
  MIME type and Twilio API does not support that kind of audio files.  
  A possible solution could be just place the URL to your correct encoded audio
  file in VF.


<br>
<br>

#### About this project

This project was created by:
<br>
__Daian Gan__<br>
Github: [daiangan](https://github.com/daiangan)<br/>
E-mail: daian@ganmedia.com<br/>
Website: https://daiangan.com<br/>