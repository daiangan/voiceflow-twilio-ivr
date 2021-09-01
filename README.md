
![VoiceFlow - Twilio IVR](src/img/header_image.jpg)

## VoiceFlow - Twilio IVR
This is a Flask app to link your VoiceFlow project with your 
Twilio phone number and create an IVR.  

Go to VoiceFlow and grab your Project Version ID and your API Key.  

Add them to your Python environment variables with the names:  
```text
VF_PROJECT_VERSION_ID
VF_API_KEY
```

Deploy your Flask app (out of this scope) and copy your app URL.  
Then go to Twilio and set up your phone number call incoming webhook to point to
your Flask app URL.  
![Twilio webhook set up](src/img/twilio_webhook_setup.jpg)


<br>
<br>

#### About this project

This project was created and is maintained by:
<br>
__Daian Gan__<br>
Github: [daiangan](https://github.com/daiangan)<br/>
E-mail: daian@ganmedia.com<br/>
Website: https://daiangan.com<br/>