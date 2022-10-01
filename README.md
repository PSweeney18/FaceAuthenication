# FaceAuthenication
Implemented a Flask web Application to test my personal Face Authenication system, using AWS


# app.py
The application require's a Software Development Kit to be implemented. User's will make a request to an AWS account that requests for two images to be compared. The first image that will be compared will be an image that is taken using the JS file, and then returned to the python script to upload said image to the AWS. The second image will be an image that will be permanently stored inside of a AWS bucket to always compare the images uploaded. 

Most of the python code has been pretty well documented, however, some of the code may need further explanation. Each time the code execute, it deletes the previous image that was uploaded. The delete() function is there just to make it much simpler when checking, as every image uploaded has the same name, and only having two images in the AWS account's bucket makes it easier to troubleshoot issues in regards to the image. (Initially there were camera issues)

# index.js
Originally, was using the OpenCV module, however, there was a fundamental flaw that was made clear to me by someone else. Web applications that are running can not request for the user's camera running on the backend. Therefore, I had to reimplement the camera function by acessing the camera and taking a photo of the screen all in JS using the built fetch method

# index.html and styles.css
In terms of the HTML and CSS, I pulled from a codepen that had a pretty looking background to help with the UI. 
 Source of the HTML and CSS: https://codepen.io/beshoooo/pen/jmbGNd
