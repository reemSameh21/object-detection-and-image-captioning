
# Object Detection and Image Captioning Web App

## Overview

This project is a web application that uses pre-trained models from Hugging Face to perform **object detection** and **image captioning** on user-uploaded images or images captured in real-time via webcam. The application is built using **Streamlit** and is deployed using **Streamlit Cloud**. Continuous integration and deployment (CI/CD) are managed via **GitHub Actions**.

### Key Features:
- **Object Detection**: Automatically detect objects in images using Hugging Face's `facebook/detr-resnet-50` model.
- **Image Captioning**: Generate descriptive captions for images using Hugging Face's `nlpconnect/vit-gpt2-image-captioning` model.
- **Real-time Image Capture**: Capture images directly from the webcam for analysis.
- **Easy-to-use Interface**: Upload or capture images via the interactive web interface.

## Tech Stack
- **Frontend**: Streamlit (Python framework for building web apps)
- **Backend**: Hugging Face pre-trained models for object detection and image captioning
- **CI/CD**: GitHub Actions
- **Deployment**: Streamlit Cloud

---

## Project Setup

### Prerequisites
Before starting, ensure that you have the following installed on your machine:
- **Python 3.8+**
- **Pip (Python Package Manager)**
- **Git** (optional but recommended for version control)

### Step 1: Clone the Repository
To get started, clone the repository to your local machine:
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### Step 2: Create a Virtual Environment (Optional but recommended)
It’s a good practice to use a virtual environment for this project:
```bash
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

The `requirements.txt` file includes the following dependencies:
```text
streamlit
transformers
torch
Pillow
opencv-python
```

### Step 4: Run the App
After installing the dependencies, you can run the Streamlit application locally:
```bash
streamlit run app.py
```

### Step 5: Access the App
Once the app is running, open your browser and go to:
```
http://localhost:8501
```

---

## Usage Instructions

### Upload or Capture an Image
- You can either **upload an image** (`.jpg`, `.jpeg`, or `.png`) or **capture an image in real-time** using your webcam.
- Use the sidebar to select between the two options.

### Object Detection
- Once an image is uploaded or captured, the app will detect objects in the image using the pre-trained `facebook/detr-resnet-50` model.
- Detected objects are displayed along with their labels and confidence scores.

### Image Captioning
- A descriptive caption for the image is generated using the pre-trained `nlpconnect/vit-gpt2-image-captioning` model.
- The caption is displayed below the detected objects.

---

## Real-Time Image Capture
If you want to capture an image directly from your webcam, follow these steps:
1. In the sidebar, select **Capture Image**.
2. Click the button "Capture Image from Webcam".
3. The app will access your webcam, capture the image, and use it for object detection and captioning.

---

## Project Structure

```bash
.
├── app.py                 # Main Streamlit application file
├── requirements.txt       # Python dependencies
├── .github                # GitHub Actions CI/CD workflows
│   └── workflows
│       └── ci-cd.yml     # GitHub Actions workflow for deploying to Streamlit Cloud
└── README.md              # Detailed project instructions
```

---

## CI/CD Pipeline with GitHub Actions

This project is set up for continuous integration and continuous deployment (CI/CD) using **GitHub Actions**. Each time you push changes to the repository, GitHub Actions will:
1. **Install dependencies** and run any **tests** (if applicable).
2. **Deploy the updated app** to **Streamlit Cloud**.

### GitHub Actions Workflow
The CI/CD process is automated using the following workflow:

`.github/workflows/deploy.yml`:
```yaml
name: Object Detection and Image Captioning

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Free up disk space
      run: |
        sudo apt-get clean
        sudo rm -rf /usr/share/dotnet /usr/local/lib/android /opt/ghc
        sudo rm -rf /home/runner/.cache/pip
        df -h

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: |
        pip install --upgrade pip setuptools wheel datasets transformers
        pip install -r requirements.txt

    - name: Deploy to Streamlit Cloud
      run: streamlit deploy app.py
      env:
        STREAMLIT_API_KEY: ${{ secrets.STREAMLIT_API_KEY }}
```

### Streamlit Cloud Deployment
To deploy the app to Streamlit Cloud:
1. Create a [Streamlit Cloud](https://streamlit.io/cloud) account.
2. Connect your GitHub repository to Streamlit Cloud.
3. Add your **Streamlit API Key** to your GitHub repository's secrets under `Settings > Secrets > Actions > New repository secret` with the key `STREAMLIT_API_KEY`.

Once configured, every change pushed to the `main` branch will trigger an automatic build and deploy process.

---

## Troubleshooting

- **Webcam Access Issue**: Ensure your browser or system allows access to the webcam if you're using the real-time image capture feature.
- **Streamlit Deployment Issues**: If Streamlit fails to deploy, check the logs in the GitHub Actions tab of your repository to identify any issues.
- **Model Loading Error**: Ensure you have an active internet connection, as the models will be downloaded from Hugging Face the first time you run the app.

---

## Learning Outcomes

By completing this project, you will:
- Gain experience using **pre-trained models** for object detection and image captioning.
- Learn how to build and deploy a **Streamlit web application**.
- Understand how to implement **CI/CD pipelines** using **GitHub Actions**.
- Work with **real-time webcam input** for image processing tasks.

---