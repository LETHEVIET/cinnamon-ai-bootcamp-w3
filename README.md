# Develop & Deploy an Image-to-Image search service

This is a repository for the Week 3 - homework of Cinnamon AI Bootcamp 2024

Group Assignment: Develop & Deploy an Image-to-Image search service from COCO 128 dataset

- Requirements:
  - AI Models: Use CLIP for image encoding and FAISS for the search algorithm.
  - APIs: At least 2 API Services (one for encoding and one for searching).
  - Input: One or more image.
  - Output: Most similarity images in your database.
  - Deployment: Deploy your APIs on AWS and provide the final endpoint.
  - Document: README with overview design of your APIs system.

Overview system design

![](./overview_system_design.png)

## Repository structure

## Image Search embedding service

## Pre-compute embedding service

## Real-time-compute embedding service

This service hosts an Embedding Computation API using `ViT-B/32` model with [CLIP](https://github.com/openai/CLIP) library.

`/compute_embedding`

> Endpoint to compute CLIP embeddings for multiple uploaded images.
>
> **Args**: files (List[UploadFile]): A list of uploaded image files.
>
> **Returns**: EmbeddingResponse (list[list[float]]): A JSON response containing the computed image embeddings.

Building Docker image

```shell
docker build . -t real-time_compute_embeddings -f services/real-time_compute_embeddings/Dockerfile
```

Running Docker image

- with CPU

```shell
docker run -p 8000:8000 -d real-time_compute_embeddings
```

- with GPU (you need to install [nvidia-container-toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) for using docker with GPU)

```shell
docker run -p 8000:8000 --gpus all -d real-time_compute_embeddings
```
