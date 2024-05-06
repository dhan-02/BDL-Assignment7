import sys
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.models import Sequential
from fastapi import FastAPI, File, UploadFile
from typing import List
from PIL import Image
from io import BytesIO
import uvicorn
import os

app = FastAPI(docs_url="/docs")

# Function to load the model from the specified path
def load_my_model(path: str) -> Sequential:
    """
    Load the model saved at the supplied path on the disk.

    Args:
    path (str): The path to the saved model on disk.

    Returns:
    keras.src.engine.sequential.Sequential: The loaded Keras Sequential model.

    Raises:
    ValueError: If the path is empty or does not exist.
    IOError: If there is an issue with reading the model file.
    """

    # Check if the path is empty
    if not path:
        raise ValueError("The path cannot be empty.")

    # Check if the file exists at the given path
    if not os.path.exists(path):
        raise ValueError(f"The file '{path}' does not exist.")

    # Check if the path is a file
    if not os.path.isfile(path):
        raise ValueError(f"'{path}' is not a file.")

    try:
        # Load the model using the keras function
        loaded_model = load_model(path)
        return loaded_model
    except IOError as e:
        raise IOError(f"Error reading model file: {e}")
    
# Function to predict the digit using the loaded model
def predict_digit(model: Sequential, data_point: list) -> str:
    """
    Predict the digit using the loaded model.

    Args:
    model (keras.src.engine.sequential.Sequential): The loaded Keras Sequential model.
    data_point (list): The image serialized as an array of 784 elements.

    Returns:
    str: The predicted digit as a string.

    Raises:
    ValueError: If the model is not provided or the data_point is not a list of 784 elements.
    """
    # Check if model is provided
    if model is None:
        raise ValueError("Model is not provided.")

    # Check if data_point is a list of 784 elements
    if not isinstance(data_point, list) or len(data_point) != 784:
        raise ValueError("Data point must be a list of 784 elements.")

    # Preprocess the data_point (reshape and normalize)
    data_point = np.array(data_point).reshape(1, -1)
    
    # Predict the digit
    prediction = model.predict(data_point)
    
    # Get the predicted digit
    predicted_digit = np.argmax(prediction)
    
    # Return the predicted digit as a string
    return str(predicted_digit)

def format_image(img):
    """
    Resize any given image to 28x28 pixels.

    Args:
    img: The input image.

    Returns:
    Image: The resized image.
    """
    # Resize the image to 28x28
    resized_img = img.resize((28, 28)) 
    
    return resized_img

def preprocess_image(file) -> List[float]:
    """
    Helper function to Preprocesses the uploaded image.

    Args:
    file: The uploaded file object.

    Returns:
    List[float]: Serialized array of image pixels after preprocessing.
    """
    if file is None:
        raise ValueError("File is not provided.")
    
    # Open the PIL Image
    img = Image.open(BytesIO(file))

    # Format the image (resize to 28x28) : extra in task2
    img = format_image(img)

    # Convert to grayscale
    img = img.convert('L')

    # Convert into np array  
    img_array = np.array(img)

    # Flatten to 1D array
    img_array = img_array.reshape(1, 28*28)  

    # Normalize pixel values
    img_array = img_array / 255.0 

    return img_array.tolist()[0]

@app.post("/predict")
async def predict_image_digit(file: UploadFile = File(...)):
    """
    API Endpoint to predict the digit from the uploaded image file.

    Args:
    file (UploadFile): The uploaded image file.

    Returns:
    dict: A dictionary containing the predicted digit.
    """
    # Read the bytes from the uploaded image
    contents = await file.read()
    
    # Preprocess the image to create a serialized array of 784 elements
    processed_image = preprocess_image(contents)
    
    # Get the path to the model from the command line argument
    model_path = sys.argv[1]
    
    # Load the model
    loaded_model = load_my_model(model_path)

    # Predict the digit using the serialized array
    predicted_digit = predict_digit(loaded_model, processed_image)
    
    # Return the predicted digit to the client
    return {"digit": predicted_digit}

if __name__ == "__main__":

    # Check if the path to the model is provided as a command line argument
    if len(sys.argv) != 2:
        print("Usage: python task2.py <path_to_model>")
        sys.exit(1)
    
    # Run the FastAPI app
    uvicorn.run(app, host="127.0.0.1", port=5000)
