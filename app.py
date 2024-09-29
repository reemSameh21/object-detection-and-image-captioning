import streamlit as st
from PIL import Image
from transformers import pipeline
import cv2
import numpy as np

# Load Hugging Face models
object_detector = pipeline("object-detection", model="facebook/detr-resnet-50")
caption_generator = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")

def detect_objects(image):
    # Ensure the image is in PIL format (RGB)
    image = image.convert("RGB")
    return object_detector(image)

def generate_caption(image):
    # Ensure the image is in PIL format (RGB)
    image = image.convert("RGB")
    return caption_generator(image)[0]['generated_text']

def capture_image():
    cap = cv2.VideoCapture(0)  # Access the webcam (device 0)
    ret, frame = cap.read()
    cap.release()  # Release the webcam
    if ret:
        # Convert the captured image (frame) from BGR to RGB
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return Image.fromarray(img_rgb)
    else:
        st.error("Failed to capture image from webcam.")
        return None

# Streamlit app
st.title("Object Detection and Image Captioning App")

# Option to upload an image or capture one via webcam
st.sidebar.title("Choose Image Input")
input_type = st.sidebar.radio("How would you like to provide the image?", ("Upload Image", "Capture Image"))

# Image upload
uploaded_image = None
if input_type == "Upload Image":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        try:
            # Convert the uploaded file to a PIL Image
            uploaded_image = Image.open(uploaded_file)
        except Exception as e:
            st.error(f"Error loading image: {e}")

# Real-time image capture
if input_type == "Capture Image":
    if st.button("Capture Image from Webcam"):
        uploaded_image = capture_image()

if uploaded_image is not None:
    # Display the uploaded or captured image
    st.image(uploaded_image, caption="Uploaded/Captured Image", use_column_width=True)

    # Object Detection
    with st.spinner("Detecting objects..."):
        try:
            objects = detect_objects(uploaded_image)
            st.write("Objects detected:")
            for obj in objects:
                st.write(f"- {obj['label']} with confidence {obj['score']:.2f}")
        except Exception as e:
            st.error(f"Error in object detection: {e}")

    # Image Captioning
    with st.spinner("Generating caption..."):
        try:
            caption = generate_caption(uploaded_image)
            st.write(f"Image Caption: {caption}")
        except Exception as e:
            st.error(f"Error in caption generation: {e}")
else:
    st.warning("Please upload an image or capture one from the webcam to get started.")