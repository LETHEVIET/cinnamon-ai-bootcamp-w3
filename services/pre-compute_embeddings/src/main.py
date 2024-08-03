import json

import faiss
from utils import create_faiss_index, get_image_embeddings

embeddings, image_paths = get_image_embeddings(
    "../../../common/data/images/train", device="cpu"
)
index = create_faiss_index(embeddings)
faiss.write_index(index, "../../../common/data/index.faiss")
with open("../../../common/data/image_paths.json", "w") as f:
    json.dump(image_paths, f, indent=4)
