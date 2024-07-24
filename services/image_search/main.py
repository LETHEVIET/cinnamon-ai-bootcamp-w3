from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import numpy as np
import faiss
import os
import json
import requests as re
import base64
from io import BytesIO

app = FastAPI()

# Assuming the embedding dimension is 512, adjust if different
index = faiss.read_index("../../common/data/index.faiss")

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


def pil_image_to_base64(image) -> str:
    # Create a BytesIO object to hold the image data
    buffered = BytesIO()

    # Save the image to the BytesIO object in the desired format (e.g., JPEG, PNG)
    image.save(buffered, format="JPEG")

    # Get the byte data from the BytesIO object
    img_byte = buffered.getvalue()

    # Encode the byte data to a base64 string
    img_base64 = base64.b64encode(img_byte).decode('utf-8')

    return img_base64


@app.post("/search-similar-images/")
async def search_similar_images(file: UploadFile = File(...), num_results: int = 5):
    try:
        # # Read the uploaded image file
        image_data = await file.read()
        
        # Get the image embedding
        # embedding = await get_image_embedding(image_data)
        url = "http://34.209.51.63:8080/compute_embedding/"
        files = {"file": (file.filename, image_data, file.content_type)}
        embedding = re.post(url, files=files).json()
        embedding = np.array(embedding["embedding"])
        
        # Reshape the embedding to match FAISS input requirements
        embedding = embedding.reshape(1, -1)
        
        # Search for similar images using FAISS
        distances, indices = index.search(embedding, num_results)
        
        # Get the URLs of similar images
        with open("../../common/data/image_paths.json") as f:
            image_urls = json.load(f)

        similar_image_urls = [image_urls[int(i)] for i in indices[0]]
        base64_images = ["data:image/png;base64," +
                         pil_image_to_base64(Image.open(url))
                         for url in similar_image_urls]
        
        return {"similar_images": base64_images}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
