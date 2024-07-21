from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import httpx
import numpy as np
import faiss
import os
import json
import requests as re
from typing import List
import base64

app = FastAPI()

# Assuming the embedding dimension is 512, adjust if different
index = faiss.read_index("../../common/data/index.faiss")


@app.post("/search-similar-images/")
async def search_similar_images(file: UploadFile = File(...), num_results: int = 5):
    try:
        # # Read the uploaded image file
        # image_data = await file.read()
        
        # Get the image embedding
        # embedding = await get_image_embedding(image_data)
        url = "http://localhost:8000/compute_embedding/"
        embedding = re.post(url, files=file)

        
        # Reshape the embedding to match FAISS input requirements
        embedding = embedding.reshape(1, -1)
        
        # Search for similar images using FAISS
        distances, indices = index.search(embedding, num_results)
        
        # Get the URLs of similar images
        with open("../../common/data/image_paths.json") as f:
            image_urls = json.load(f)

        similar_image_urls = [image_urls[int(i)] for i in indices[0] if int(i) in image_urls]
        
        return JSONResponse(content={"similar_images": similar_image_urls})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))