Sortify AI - Backend & Machine Learning API
Overview
This is the backend service for the Sortify AI platform. It serves a YOLOv8 waste detection model via a REST API, processing image uploads and returning results in JSON format. The service is containerized with Docker and deployed on Hugging Face Spaces for portability and scalability.

Features
⚙️ AI-Powered Waste Classification API: Provides a dedicated endpoint for image analysis.
👁️ YOLOv8 Model Integration: Performs inference using a custom-trained best.pt model to detect 6 classes of waste.
🖼️ Image Upload Handling: Designed to accept image inputs via multipart/form-data.
📄 Structured JSON Response: Delivers a clear output containing waste class, confidence score, and bounding box coordinates.
🐳 Dockerized for Portability: Ensures a consistent environment from local development to production.
☁️ Cloud-Deployed: Publicly hosted on Hugging Face Spaces to be accessed by the frontend application.


Tech Stack
Language: Python 3.9
Framework: Flask
WSGI Server: Gunicorn
Machine Learning: Ultralytics (YOLOv8), PyTorch, OpenCV
Others: Flask-CORS
Containerization: Docker
Prerequisites
To run this project locally, you will need:

Python (v3.9 or higher)
pip (package installer for Python)
virtualenv (recommended for creating isolated environments)
Getting Started
Follow these steps to run the server on your local machine.

Clone the repository

Bash

git clone [your-repository-url]
cd [repository-folder-name]
Create and activate a virtual environment

Bash

# Create the environment
python -m venv venv

# Activate on Windows
.\venv\Scripts\activate

# Activate on MacOS/Linux
source venv/bin/activate
Install dependencies

Bash

pip install -r requirements.txt
Run the development server
Make sure the best.pt file is in the same folder.

Bash

# Use your correct .py filename
python app_flask.py 
The server is now running on http://127.0.0.1:5000.

Project Structure
.
├── app_flask.py        # Main Flask application logic
├── best.pt             # YOLOv8 model weights file
├── Dockerfile          # Recipe for building the Docker image
├── requirements.txt    # List of required Python libraries
└── README.md           # This documentation

Prediction Endpoint
POST /predict
This endpoint is used to send an image and get detection results.

URL: https://notnith-deteksi-sampah-sprtofy.hf.space/predict

Method: POST
Body: form-data

Key: image
Type: File
Value: [Select your image file]
Success Response (200 OK):

JSON

{
  "status": "success",
  "detections": [
    {
      "waste_type": "cardboard",
      "confidence": 0.85,
      "bounding_box (xyxy)": [101.5, 202.3, 350.1, 450.9]
    }
  ]
}
Error Response (400/500):

JSON

{
  "status": "error",
  "message": "Image file not found in request."
}
Deployment
This API application is publicly deployed on Hugging Face Spaces and can be accessed via the following base URL:
https://huggingface.co/spaces/Notnith/Deteksi-sampah_sprtofy

Note: Replace with your correct Space URL if different.

License
This project is licensed under the MIT License - see the LICENSE file for details.
