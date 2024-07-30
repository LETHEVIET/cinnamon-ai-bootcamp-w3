import json

import faiss
import numpy as np
import requests as re
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()

# Assuming the embedding dimension is 512, adjust if different
index = faiss.read_index("../../common/data/index.faiss")


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

        similar_image_urls = [
            image_urls[int(i)] for i in indices[0] if int(i) in image_urls
        ]

        return JSONResponse(content={"similar_images": similar_image_urls})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
