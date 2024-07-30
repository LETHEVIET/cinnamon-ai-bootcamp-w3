import glob
from pathlib import Path

import clip
import faiss
import numpy as np
import torch
from dataset import ImageDataset
from torch.utils.data import DataLoader


def get_data_paths(
    dir: str | list[str], data_formats: list, prefix: str = ""
) -> list[str]:
    """
    Get list of files in a folder that have a file extension in the data_formats.

    Args:
      dir (str | list[str]): Dir or list of dirs containing data.
      data_formats (list): List of file extensions. Ex: ['jpg', 'png']
      prefix (str): Prefix for logging messages.

    Returns:
      A list of strings.
    """
    try:
        f = []  # data files
        for d in dir if isinstance(dir, list) else [dir]:
            p = Path(d)
            if p.is_dir():
                f += glob.glob(str(p / "**" / "*.*"), recursive=True)
            else:
                raise FileNotFoundError(f"{prefix}{p} does not exist")
        data_files = sorted(x for x in f if x.split(".")[-1].lower() in data_formats)
        return data_files
    except Exception as e:
        raise Exception(f"{prefix}Error loading data from {dir}: {e}") from e


def get_image_embeddings(data_dir, model_name="ViT-B/32", batch_size=32, device="cpu"):
    # Load the CLIP model
    model, preprocess = clip.load(model_name, device=device)

    # Create a dataset and dataloader
    image_paths = get_data_paths(data_dir, data_formats=["jpg", "jpeg", "png"])
    print(len(image_paths))
    dataset = ImageDataset(image_paths, preprocess)
    dataloader = DataLoader(dataset, batch_size=batch_size, num_workers=4)

    # List to store image embeddings
    image_embeddings = []

    # Process images in batches
    with torch.no_grad():
        for images in dataloader:
            images = images.to(device)
            embeddings = model.encode_image(images)
            embeddings /= embeddings.norm(dim=-1, keepdim=True)
            image_embeddings.append(embeddings.cpu().numpy())

    # Convert list to numpy array
    image_embeddings = np.vstack(image_embeddings)

    return image_embeddings, image_paths


def create_faiss_index(embeddings):
    # Determine the dimensionality of the embeddings
    d = embeddings.shape[1]

    # Initialize a FAISS index
    index = faiss.IndexFlatL2(d)

    # Add embeddings to the index
    index.add(embeddings)

    return index
