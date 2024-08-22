import streamlit as st
import cv2
from PIL import Image
import numpy as np

st.title("Image Processing App")

# Sidebar for controls
st.sidebar.title("Controls")

# Upload image in the sidebar
uploaded_file = st.sidebar.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])

# Function to resize image
def resize_image(image, width=1080, height=720):
    return cv2.resize(image, (width, height))

if uploaded_file is not None:
    # Convert the file to an OpenCV image
    image = Image.open(uploaded_file)
    image = np.array(image)
    
    # Resize image
    resized_image = resize_image(image)
    
    # Display the resized image in the main window
    st.image(resized_image, caption='Resized Image (1080x720)', use_column_width=True)
    
    # Initialize session state for sliders and buttons if not already done
    if "processing_mode" not in st.session_state:
        st.session_state.processing_mode = None
    if "blur_value" not in st.session_state:
        st.session_state.blur_value = 3
    if "edge_threshold1" not in st.session_state:
        st.session_state.edge_threshold1 = 100
    if "edge_threshold2" not in st.session_state:
        st.session_state.edge_threshold2 = 200
    
    # Sidebar buttons for different image processing tasks
    processing_mode = st.sidebar.radio("Select Processing Mode", ("Gray", "Blur", "Edge"))
    
    if processing_mode == "Gray":
        st.session_state.processing_mode = "Gray"
    elif processing_mode == "Blur":
        st.session_state.processing_mode = "Blur"
        st.session_state.blur_value = st.sidebar.slider("Select blur intensity", 1, 10, st.session_state.blur_value)
    elif processing_mode == "Edge":
        st.session_state.processing_mode = "Edge"
        st.session_state.edge_threshold1 = st.sidebar.slider("Select Canny edge threshold 1", 50, 150, st.session_state.edge_threshold1)
        st.session_state.edge_threshold2 = st.sidebar.slider("Select Canny edge threshold 2", 150, 300, st.session_state.edge_threshold2)
    
    # Display the selected image processing result in the main window
    if st.session_state.processing_mode == "Gray":
        gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
        st.image(gray_image, caption='Grayscale Image', use_column_width=True, channels='GRAY')
        
    elif st.session_state.processing_mode == "Blur":
        blurred_image = cv2.GaussianBlur(resized_image, (2 * st.session_state.blur_value + 1, 2 * st.session_state.blur_value + 1), 0)
        st.image(blurred_image, caption='Blurred Image', use_column_width=True)
        
    elif st.session_state.processing_mode == "Edge":
        edged_image = cv2.Canny(resized_image, st.session_state.edge_threshold1, st.session_state.edge_threshold2)
        st.image(edged_image, caption='Edge Image', use_column_width=True, channels='GRAY')
else:
    st.warning("Please upload an image to proceed.")
