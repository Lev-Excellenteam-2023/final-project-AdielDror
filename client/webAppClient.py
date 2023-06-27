import requests
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Status:
    status: str
    filename: str
    timestamp: datetime
    explanation: str

    def is_done(self):
        """
        Checks if the status is 'done'.

        Returns:
            bool: True if the status is 'done', False otherwise.
        """
        return self.status == 'done'


class WebAppClient:
    def __init__(self, base_url):
        """
        Initializes a client for interacting with the web application API.

        Args:
            base_url (str): The base URL of the web application API.
        """
        self.base_url = base_url

    def upload(self, file_path):
        """
        Uploads a file to the web application.

        Args:
            file_path (str): The path of the file to upload.

        Returns:
            str: The unique identifier (UID) of the uploaded file.

        Raises:
            Exception: If the upload request fails.
        """
        upload_url = f"{self.base_url}/upload"
        with open(file_path, 'rb') as file:
            response = requests.post(upload_url, files={'file': file})

        if response.status_code != 200:
            raise Exception(f"Upload failed with status code: {response.status_code}")

        return response.json()['uid']

    def status(self, uid):
        """
        Retrieves the status of a processed file from the web application.

        Args:
            uid (str): The unique identifier (UID) of the file.

        Returns:
            Status: An object representing the status of the file.

        Raises:
            Exception: If the status request fails.
        """
        status_url = f"{self.base_url}/status/{uid}"
        response = requests.get(status_url)

        if response.status_code != 200:
            raise Exception(f"Status request failed with status code: {response.status_code}")

        json_data = response.json()
        status = json_data['status']
        filename = json_data['filename']
        timestamp = datetime.strptime(json_data['timestamp'], '%Y%m%d%H%M%S')
        explanation = json_data['explanation']

        return Status(status, filename, timestamp, explanation)
