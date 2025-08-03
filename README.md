# Hand-Sign-Detection-Complete-System
This repository contains a Flask web application for real-time hand gesture recognition. The application uses a custom-trained YOLO model (model.pt) to detect and classify several hand signs, including "hello," "ok," "no," "ilv," and "thank you." The system includes user authentication with a login and signup page, and a video stream that displays the detected hand gestures in real-time.

Getting Started
To run this application, you will need the following:

python

flask

ultralytics

opencv-python

Prerequisites
A custom-trained YOLO model file named model.pt.

A users.txt file in the same directory for user credentials.

The necessary HTML template files (intro.html, login.html, signup.html, home.html, webcam.html).

Usage
Clone this repository: git clone [repository_url]

Make sure you have all the prerequisite files and directories.

Install the required Python packages: pip install flask ultralytics opencv-python

Run the application: python app.py

Access the application in your web browser at http://127.0.0.1:5000.

You can then sign up or log in to access the webcam feed with hand gesture detection.
