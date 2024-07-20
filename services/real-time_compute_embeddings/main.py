from io import BytesIO
from typing import List

import clip
import torch
from fastapi import FastAPI, UploadFile
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
model, preprocess = clip.load("model/ViT-B-32.pt", device=device)

app = FastAPI()


def generate_embedding(content_list):
    """
    Generates CLIP embeddings for a list of image contents.

    Args:
        content_list (list): A list of image contents in bytes format.

    Returns:
        list[list[float]]: A list of lists representing the image embeddings.
    """
    lst = []
    for contents in content_list:
        image_stream = BytesIO(contents)
        pil_image = Image.open(image_stream)
        image = preprocess(pil_image).unsqueeze(0).to(device)
        lst.append(image)
    images = torch.cat(lst, 0)
    print(images.shape)
    with torch.no_grad():
        image_features = model.encode_image(images)

    image_features = image_features.tolist()

    return image_features


@app.post("/compute_embedding/")
async def compute_embedding(files: List[UploadFile]) -> EmbeddingResponse:
    """
    Endpoint to compute CLIP embeddings for multiple uploaded images.

    Args:
        files (List[UploadFile]): A list of uploaded image files.

    Returns:
        EmbeddingResponse: A JSON response containing the computed image
                           embeddings.
    """

    content_list = [await file.read() for file in files]

    embedding = generate_embedding(content_list)

    return {"embedding": embedding}
