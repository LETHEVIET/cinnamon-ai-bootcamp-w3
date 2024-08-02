from locust import HttpUser, TaskSet, task, between
import os


class ImageUploadTaskSet(TaskSet):

    @task
    def upload_image(self):
        # Specify the image file path
        image_path = "/home/pc/cinnamon-ai-bootcamp-w3/common/data/images/test/aeroplane/000000000081_jpg.rf.01074c9f618f95461ff0aae0a678b060.jpg"
        
        # Open the image file in binary mode
        with open(image_path, "rb") as image_file:
            # Prepare the files dictionary for the POST request
            files = {"file": ("image.jpg", image_file, "image/jpeg")}
            data = {"num_results": 5}

            self.client.post("/search-similar-images", files=files, data=data)


class WebsiteUser(HttpUser):
    tasks = [ImageUploadTaskSet]
    wait_time = between(1, 5)  # Time to wait between tasks
        