from io import BytesIO
from typing import List

import clip
import torch
from fastapi import FastAPI, UploadFile, File
from PIL import Image
from pydantic import BaseModel


class EmbeddingResponse(BaseModel):
    """
    Pydantic model for the embedding response.

    Attributes:
        embedding (List[List[float]]): A list of lists representing
                                the image embeddings.
    """

    embedding: List[List[float]]


device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("./model/ViT-B-32.pt", device=device)

app = FastAPI()


def generate_embedding(content):
    """
    Generates CLIP embeddings for a list of image contents.

    Args:
        content_list (list): A list of image contents in bytes format.

    Returns:
        list[list[float]]: A list of lists representing the image embeddings.
    """
    image_stream = BytesIO(content)
    pil_image = Image.open(image_stream)
    image = preprocess(pil_image).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image)

    image_features = image_features.tolist()

    return image_features


@app.post("/compute_embedding/")
async def compute_embedding(file: UploadFile = File(...)) -> EmbeddingResponse:
    """
    Endpoint to compute CLIP embeddings for multiple uploaded images.

    Args:
        file (UploadFile): An uploaded image files.

    Returns:
        EmbeddingResponse: A JSON response containing the computed image
                           embeddings.
    """

    content = await file.read()

    embedding = generate_embedding(content)

    return {"embedding": embedding}
