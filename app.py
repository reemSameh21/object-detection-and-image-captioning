import streamlit as st
from PIL import Image
from transformers import pipeline
import torch
import gc
from gtts import gTTS  # Text-to-Speech library
import base64
import os

# Load Hugging Face models with trust_remote_code to avoid warnings
@st.cache_resource
def load_object_detector():
    return pipeline("object-detection", model="facebook/detr-resnet-50", trust_remote_code=True)


@st.cache_resource
def load_caption_generator():
    return pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning", trust_remote_code=True)


@st.cache_resource
def load_translator(target_language):
    return pipeline("translation", model=f"Helsinki-NLP/opus-mt-en-{target_language}", trust_remote_code=True)


# Disable gradients to save memory
@torch.no_grad()
def detect_objects(image, object_detector, threshold=0.5):
    image = image.convert("RGB")
    objects = object_detector(image)
    filtered_objects = [obj for obj in objects if obj['score'] >= threshold]  # Filter by threshold
    return filtered_objects


@torch.no_grad()
def generate_caption(image, caption_generator):
    image = image.convert("RGB")
    caption = caption_generator(image)[0]['generated_text']
    return caption


# Function to convert text to speech and return a download link
def text_to_speech(text, language):
    tts = gTTS(text, lang=language)
    audio_file_path = "caption.mp3"
    tts.save(audio_file_path)

    # Load and encode the audio file
    with open(audio_file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        audio_link = f'<a href="data:audio/mp3;base64,{audio_base64}" download="caption.mp3">Download Caption as MP3</a>'

    # Remove the audio file after reading
    os.remove(audio_file_path)
    return audio_link


# Function to translate the caption and object detection labels
def translate_text(text, target_language_code):
    if target_language_code == 'en':
        return text  # No translation needed for English
    elif target_language_code == 'ar':
        # Use a specific translation model for English to Arabic
        translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-ar", trust_remote_code=True)
        translated_text = translator(text)[0]['translation_text']
    else:
        # Use a general translation model for other languages
        translator = load_translator(target_language_code)
        translated_text = translator(text)[0]['translation_text']

    return translated_text


# Streamlit app
st.title("Multilingual Object Detection and Image Captioning App")

# Option to upload an image or capture one via webcam
st.sidebar.title("Choose Image Input")
input_type = st.sidebar.radio("How would you like to provide the image?", ("Upload Image", "Capture Image"))

# Language selection
st.sidebar.title("Select Language")
languages = {
    "English": "en",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Arabic": "ar"
}
selected_language = st.sidebar.selectbox("Choose the language for the caption", list(languages.keys()))
selected_language_code = languages[selected_language]

uploaded_image = None
if input_type == "Upload Image":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        try:
            uploaded_image = Image.open(uploaded_file)
        except Exception as e:
            st.error(f"Error loading image: {e}")

if input_type == "Capture Image":
    # Use Streamlit's camera_input for webcam capture
    captured_image = st.camera_input("Capture an image using your webcam")
    if captured_image is not None:
        try:
            uploaded_image = Image.open(captured_image)
        except Exception as e:
            st.error(f"Error capturing image: {e}")

if uploaded_image is not None:
    resized_image = uploaded_image.resize((512, 512))  # Resize early to save memory
    st.image(resized_image, caption="Uploaded/Captured Image (Resized)", use_column_width=True)

    # Object Detection Confidence Threshold
    confidence_threshold = st.slider("Set object detection confidence threshold", 0.1, 1.0, 0.5)

    # Object Detection
    with st.spinner("Detecting objects..."):
        try:
            object_detector = load_object_detector()  # Load the detector here
            objects = detect_objects(resized_image, object_detector, threshold=confidence_threshold)
            st.write("Objects detected:")
            translated_labels = []
            for obj in objects:
                translated_label = translate_text(obj['label'], selected_language_code)
                translated_labels.append(translated_label)
                st.write(f"- {translated_label} with confidence {obj['score']:.2f}")
        except Exception as e:
            st.error(f"Error in object detection: {e}")

    # Image Captioning and Translation
    with st.spinner("Generating and translating caption..."):
        try:
            caption_generator = load_caption_generator()  # Load the caption generator here
            caption = generate_caption(resized_image, caption_generator)
            translated_caption = translate_text(caption, selected_language_code)
            st.write(f"Image Caption in {selected_language}: {translated_caption}")
            # Convert caption to speech and provide download link
            st.markdown(text_to_speech(translated_caption, selected_language_code), unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error in caption generation or translation: {e}")
else:
    st.warning("Please upload an image or capture one from the webcam to get started.")

# Call garbage collection at the end to free up memory
gc.collect()