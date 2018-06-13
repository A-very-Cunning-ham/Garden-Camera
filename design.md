# Design
The Garden Camera project is designed to use a Raspberry Pi and an Amazon Alexa device to monitor and control a home garden. This is acheived by using the AWS Alexa developer console linked to the Raspberry Pi with a HTTPS endpoint. All Alexa code is run locally on the RPi by using Python and the Flask-Ask module. To connect Alexa to the Python a flask server was used with ngrok HTTPS 5000 tunneling. 
## Operation
When Alexa receives an invocation request it sends a JSON file to the RPi server where flask determines the proper function to run based on the intent name. Three main intents are available to run. These intents are described below:
* GPIOControlIntent: This intent accepts two user inputs, one number slot and one literal slot. These slots allow the user to define a GPIO pin to modify and a requested state. Once invoked this function changes the GPIO output on the RPi to the user's request using the `RPi.GPIO` module. This allows for the control of numerous electrical devices that may be connected to the RPi. From fans to sprinklers to lights, a garden can be fully controlled. This intent is invoked with the format "turn pin {pin} {status}", where {pin} is a Broadcom pin number and {status} is "on" or "off".
* PlantHealth: This intent accepts one user input, a slot to define a type of photo to take. The types of photos available are unprocessed red, green, and near infrared chanel pictures, or normalized difference vegetation index processed images. Both images are initially captured as a 3D numpy array, and are then converted to images via the `Matplotlib` module. If the user requests the image unprocessed then this will be the final image. In the case of a NDVI request the numpy array is first processed pixel by pixel using the formula `NDVI = nir-red / nir+red` where the result is a grayscale 2D array with values between -1 and 1. This is then colorized using a lookup table. Processed images are then saved locally and uploaded to Google Drive using the Drive API. This processes occurs using both the Python 2.0 garden_camera.py and Python 3.0 captureUpload.py scripts with a `subprocess.Popen()` command.  This intent is invoked with the format "Show me my garden in {picture}" where picture is a format of "NDVI" or "NIR".
* pictureIntent: This intent is essentially a stripped down version of the PlantHealth intent for immediate and easily quantifiable results. Calling to the cameraSum.py script with a `subprocess.check_output()` function, a NDVI image is captured and the average NDVI value across all pixels is determined. This is returned to the main function and is compared to the prior value from this call. The magnitude and direction of the change in plant health is determined and returned to the user. This metric could be helpful in achieving measures to improve plant health in case of stress with GPIOControlIntent, or prompting further inquiry with the PlantHealth intent.  This intent is invoked with the format "Tell me how are my plants are doing".