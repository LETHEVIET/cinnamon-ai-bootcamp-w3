from confluent_kafka import Consumer, KafkaError
import base64
import json
import requests as re
import numpy as np
import faiss

KAFKA_BROKER = 'localhost:9092'  # Replace with your Kafka broker address
KAFKA_TOPIC = 'image-uploads'
KAFKA_GROUP = 'image-search-group'
FAISS_INDEX_PATH = "../../common/data/index.faiss"

# Initialize Kafka consumer
consumer = Consumer({
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': KAFKA_GROUP,
    'auto.offset.reset': 'earliest'
})
consumer.subscribe([KAFKA_TOPIC])

# Load FAISS index
index = faiss.read_index(FAISS_INDEX_PATH)

def compute_image_embedding(image_data):
    url = "http://localhost:8080/compute_embedding/"
    files = {"file": ("image.jpg", image_data, 'image/jpeg')}
    response = re.post(url, files=files)
    return np.array(response.json()["embedding"])

def process_message(message):
    data = json.loads(message.value().decode('utf-8'))
    file_content = base64.b64decode(data['file_content'])
    
    # Compute image embedding
    embedding = compute_image_embedding(file_content)
    embedding = embedding.reshape(1, -1)
    
    # Search for similar images using FAISS
    num_results = 5
    distances, indices = index.search(embedding, num_results)
    
    # Save results somewhere or send them to another service
    # For example, you can store the results in a database or file

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print(msg.error())
            break
    process_message(msg)

consumer.close()
