# Garden Camera :seedling:
This is an IoT project that allows Amazon Alexa to control a smart gardening system with infrared image plant health monitoring.
## Operation
* Turn any device connected to your Raspberry Pi on or off by saying "turn pin {pin} {status}", where {pin} is a Broadcom pin number and {status} is "on" or "off". For example turning a sprinkler system connected to pin 17 on would be accomplished by saying "Alexa, open Garden Camera and turn pin 17 on". This will work for sprinklers, lights, fans, pumps, speakers, and many more devices.
* Determine the health of your garden by assessing the photosynthesis levels using the Pi NoIr Camera. With a blue filter installed over your camera and pointed in the direction of your plants simply say "Alexa, open Garden Camera and tell me about my plants". This will give you a percentage and change from the last time the intent was called.
* Need a closer look at your garden? Just say "Alexa, open Garden Camera and show me my garden in NDVI" to get a current image of your plants with NDVI processing. Prefer an unprocessed image? Just ask for it in a NIR format instead. 


## Installation
To get this running with your own system you will need to follow these steps. This assumes you have a Raspberry Pi running Raspbian, a Pi NOiR module, and moderate knowledge of linux and the Pi.
1. First, SSH into your RPi. It will make the whole process a lot easier.
2. Clone the code in this repository ```git clone https://github.com/A-very-Cunning-ham/Garden-Camera.git```
3. Install python, flask, and flask ask:
      ```
      sudo apt-get update && sudo apt-get upgrade -y
      sudo apt-get install python2.7-dev python-dev python-pip
      sudo pip install Flask flask-ask
      ```
4. Download the proper version of ngrok from https://ngrok.com/download and install it using `unzip /home/pi/ngrok-stable-linux-arm.zip`
5. Install screen with `apt-get install screen` and run it with `screen`. This will let you leave your ssh session and keep your server alive 
6. Run ngrok using `sudo ./ngrok http 5000` and make note of the https forwarding address
7. Create a custom Amazon Alexa skill at https://developer.amazon.com/alexa/console and set its endpoint to the https address you made note of earlier
8. Drag the alexa.json file into the Alexa "JSON Editor" page. Save and build your Alexa skill.
9. Follow the tutorial at https://developers.google.com/drive/api/v3/quickstart/python to create your client_secret.json and credentials.json files. These are needed to upload images to your Google Drive.
10. To get your flask skill working open a new ssh session and run:

      ```
      screen
      export FLASK_APP=/home/pi/alexaCamera/garden_camera.py
      python -m flask run
      ```
      Make sure to update the file path to match your working directory.
11. Test your skill in the Alexa Console.

### Acknowledgements
Parts of this project are adapted from PatrickD126's Instructable at http://www.instructables.com/id/Control-Raspberry-Pi-GPIO-With-Amazon-Echo-and-Pyt/
