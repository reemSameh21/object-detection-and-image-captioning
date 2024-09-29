import streamlit as st
from PIL import Image
from transformers import pipeline
import cv2
import torch
import gc

# Load Hugging Face models with trust_remote_code to avoid warnings
@st.cache_resource  # Cache models to avoid reloading
def load_object_detector():
    return pipeline("object-detection", model="facebook/detr-resnet-50", trust_remote_code=True)

@st.cache_resource  # Cache models to avoid reloading
def load_caption_generator():
    return pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning", trust_remote_code=True)

object_detector = load_object_detector()
caption_generator = load_caption_generator()

# Disable gradients to save memory
@torch.no_grad()
def detect_objects(image):
    image = image.convert("RGB")
    objects = object_detector(image)
    gc.collect()  # Free memory
    return objects

@torch.no_grad()
def generate_caption(image):
    image = image.convert("RGB")
    caption = caption_generator(image)[0]['generated_text']
    gc.collect()  # Free memory
    return caption

def capture_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if ret:
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return Image.fromarray(img_rgb)
    else:
        st.error("Failed to capture image from webcam.")
        return None

def resize_image(image, max_size=512):
    width, height = image.size
    if max(width, height) > max_size:
        scaling_factor = max_size / float(max(width, height))
        new_size = (int(width * scaling_factor), int(height * scaling_factor))
        return image.resize(new_size, Image.ANTIALIAS)
    return image

# Streamlit app
st.title("Object Detection and Image Captioning App")

# Option to upload an image or capture one via webcam
st.sidebar.title("Choose Image Input")
input_type = st.sidebar.radio("How would you like to provide the image?", ("Upload Image", "Capture Image"))

uploaded_image = None
if input_type == "Upload Image":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        try:
            uploaded_image = Image.open(uploaded_file)
        except Exception as e:
            st.error(f"Error loading image: {e}")

if input_type == "Capture Image":
    if st.button("Capture Image from Webcam"):
        uploaded_image = capture_image()

if uploaded_image is not None:
    resized_image = resize_image(uploaded_image)
    st.image(resized_image, caption="Uploaded/Captured Image (Resized)", use_column_width=True)

    # Object Detection
    with st.spinner("Detecting objects..."):
        try:
            objects = detect_objects(resized_image)
            st.write("Objects detected:")
            for obj in objects:
                st.write(f"- {obj['label']} with confidence {obj['score']:.2f}")
        except Exception as e:
            st.error(f"Error in object detection: {e}")

    # Image Captioning
    with st.spinner("Generating caption..."):
        try:
            caption = generate_caption(resized_image)
            st.write(f"Image Caption: {caption}")
        except Exception as e:
            st.error(f"Error in caption generation: {e}")
else:
    st.warning("Please upload an image or capture one from the webcam to get started.")