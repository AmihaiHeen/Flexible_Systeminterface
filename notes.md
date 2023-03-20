# Flexible system interface for visualizing analysis models Notes

## Problem 1 Capturing Images from ultrasound machine
The first problem to solve in the development of the system interface is to capture the images on client demand. to resolve this problem there are several different solutions:

- Solution 1: Capture image on click of a button
- Solution 2: Capture image when the image freezes
- Solution 3: background capture of images

### Capture image on button event
To get the images from the ultrasound machine the library of OpenCV has been imported to capture the images to the backend. This can be done by continuously reading the image in a while loop and capture each frame. To test the click of a template of the interface has been developed containing a drawing the image captured from the image stream upon the click of a HTML button.  
The first iteration of the capturing of the image on a button event, the video feed being read and streamed to the client side using the flask.Response() function. The client side Captures the image by calling "url_for('function_name')". The image stream is hidden from the user.  
Using JavaScript, the current image is then captured on the click of a button, and then displayed by drawing the image on a canvas. Using Flask WebSocket, the image is then send to the backend and saved with a 'unique' name for later processing. The reasoning of using a button for the image capture is to make is easy for the user to control when to get and send an image to the analysis models.
A second iteration was made using WebSocket to register the button click and thereafter emitting the image to the client side. Though this minimizes the load on the page it has a about 3-5 seconds delay on showing the image.

### Capture image on image freeze
To capture the image when the clinician freezes the image a python function has been developed. The function starts as a background thread upon opening the webpage, and uses OpenCV to capture the image stream. Using a while loop the current image is then compared to the previous image by taking the sum of the absolute value of the 2 images returning the difference of the two images. If the two images are identical the sum would be equal to 0, and if they differ above that. This way it is possible to capture each time the clinician freezes the image on the ultrasound machine.  
To make sure that the same image is not being saved multiple times, a function controlling if the image is still frozen has been made. This is done by looking at the difference and the previous difference, then returning True if there is no difference and the image is still frozen, and false when the image changes. The frozen image is then saved and emitted to the webpage using WebSocket. The advantage of capturing the image when the clinician freezes the ultrasound image, is that it minimize the amount of clicks and actions needed by the clinician to start the analysis, as well as the possibility of human errors.
This solution do not stream the video feed into the webpage but works in the backend of the system. This is done as a separate process as a thread running in the background, which starts on the connection and ends on disconnection of the WebSocket. The thread is implemented using python classes and threading, using threading events it is possible to stop the while loop on demand by implementing a stop function that changes the event to set and ending the while loop.
This is tested on a template using a canvas and WebSocket that listens for an image. The image is emitted to the template upon the freeze of the image and are then captured by the listener and drawn on the canvas, set with a 100ms timeout to make sure that the image is set before the interface tries to draw it. Without the timeout the image is not defined before the JavaScript tries to draw it upon the canvas and the canvas stays empty.  

### Continuously capture and analyze images in the background
There was a wish for the system to be able to capture images in the background while still capturing the images on client demand. The advantage of doing this is that the models can constantly analyze the stream of images and catch unnoticed anomalies and planes while the clinician is scanning the patient.   
For the solution of capturing the images on the click of a button, the stream of images are captured and send by a WebSocket back to the backend in a specified frequency. Here the images are saved to specific folder.
In the image freeze solution there are no image stream to the frontend and the images has to be captured in the backend as a separate process. This is done in a seperate python class extended as a thread, here an administator has predefined the frequency of which the images are captured and saved. The images are saved and put into a que that can then be read and processed. A simple simulation of a processing of an image has been implemented running as a thread that reads from the que with a 1 second delay between each value fetched. This function calculates the mean of the image np.array and prints "True" if the mean is above 115 and "False" if it is below that. Once the clinician is done and clicks on the home button, the threads looking at for frozen images and the thread filling the buffer/que are then stopped. The "analysis" of the images put into the que continuous to analyze untill the que is empty. 

### UI: template_1  v.1

The first template is developed to capture the frames from the ultrasound feed on the click of a button.  
This is done so that when the clinician has frozen the image they are able to look away from the main ultrasound monitor and start the analysis manually, instead of having to look back and forth between the two monitors. Once starting the analysis the UI will update and display the captured image, and beside it an image with the overlay/mask output(segmentation) of the analysis model. This is to make it easy for the clinician to see the results visually.  
Furthermore a result-box has been implemented to display quality of the image taken, as well as other outputs of the model. These fields have been color-coded to give a non-technical illustration of the quality and output of the analysis model.  
The UI is made from KISS(Keep it simple and stupid-proof) principle, since the system is supposed to be used as a tool beside the clinicians own knowledge and help educate new clinician. Therefore there should be minimal User interaction, simple visualization(color-coding to demonstrate quality/progress).
The reasoning behind the simple UI is that the clinicians should have an easy time understanding the webpage and not draw unnecessary attention during the ultrasound procedure.  
The html page has been split into 4 blocks so that it is easy to make changes to the UI and place the different elements where they are needed/wished by the clinician to be. Due to the dark environment of the ultrasound scanning clinics, the template has been developed in a dark theme with a few important things highlighted by more presenting colors.   This is done to ease the eyes and not light up the entire room from one monitor.

### UI: template_3 v.1

This template is used to test the image capture upon freezing the image. Implementing the functions that detect if the image is frozen. Once the clinician is freezing the image the image is captured and saved to a specific directory and send to the frontend interface using WebSocket and drawn on a canvas. As well as template_1 it has a dark theme and there are minimal different elements to interact with. In this template is possible to show and hide the different analysis outputs, as well as enable "expert-mode" so that only the crucial information detected is displayed.   
The reasoning of making the frozen image template is that it is important to make the interface as user-friendly as possible, and minimize the need for user input.

## before meeting:

- Diagrams necessary
- Web application
- Risks
- Capturing images
- template UI
- Milestone diagram/Gantt chart
- Use Cases
- Image extraction

#references
- https://www.geeksforgeeks.org/python-classes-and-objects/
- https://docs.python.org/3/library/threading.html
- https://docs.python.org/3/library/queue.html#queue.Empty
