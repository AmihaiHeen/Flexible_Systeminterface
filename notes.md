# Notes

## UI: template_1

The first template is developed to capture the frames from the ultrasound feed on the click of a button.  
This is done so that when the clinician has frozen the image they are able to look away from the main ultrasound monitor and start the analysis manually, instead of having to look back and forth between the two monitors. Once starting the analysis the UI will update and display the captured image, and beside it an image with the overlay/mask output(segmentation) of the analysis model. This is to make it easy for the clinician to see the results visually.  
Furthermore a result-box has been implemented to display quality of the image taken, as well as other outputs of the model. These fields have been color-coded to give a non-technical illustration of the quality and output of the analysis model.  
The UI is made from KISS(Keep it simple and stupid-proof) principle, since the system is supposed to be used as a tool beside the clinicians own knowledge and help educate new clinician. Therefore there should be minimal User interaction, simple visualization(color-coding to demonstrate quality/progress).
The reasoning behind the simple UI is that the clinicians should have an easy time understanding the webpage and not draw unnecessary attention during the ultrasound procedure.  
The html page has been split into 4 blocks so that it is easy to make changes to the UI and place the different elements where they are needed/wished by the clinician to be. Due to the dark environment of the ultrasound scanning clinics, the template has been developed in a dark theme with a few important things highlighted by more presenting colors.   This is done to ease the eyes and not light up the entire room from one monitor.


## before meeting:

- Diagrams necessary
- Web application
- Risks
- Capturing images
- template UI
- Milestone diagram/Gantt chart
- Use Cases
- Image extraction
