import requests
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Status:
    status: str
    filename: str
    timestamp: datetime
    explanation: str
    finish_time: datetime

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

    def upload(self, file_path, email=None):
        """
        Uploads a file to the web application.

        Args:
            file_path (str): The path of the file to upload.
            email (str, optional): The email address of the user. Default is None.

        Returns:
            str: The unique identifier (UID) of the uploaded file.

        Raises:
            Exception: If the upload request fails.
        """
        upload_url = f"{self.base_url}/upload"

        with open(file_path, 'rb') as file:
            data = {'email': email} if email else None
            response = requests.post(upload_url, files={'file': file}, data=data)

        if response.status_code != 200:
            raise Exception(f"Upload failed with status code: {response.status_code}")

        return response.json()['uid']

    def status_by_uid(self, uid):
        """
        Retrieves the status of a processed file from the web application using its unique identifier (UID).

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

        finish_time_str = json_data.get('finish_time')
        finish_time = datetime.strptime(finish_time_str, '%Y-%m-%d %H:%M:%S.%f') if finish_time_str else None

        return Status(status, filename, timestamp, explanation, finish_time)

    def status_by_filename_and_email(self, filename, email):
        """
        Retrieves the status of a processed file from the web application using its filename and email.

        Args:
            filename (str): The filename of the file.
            email (str): The email address of the user.

        Returns:
            Status: An object representing the status of the file.

        Raises:
            Exception: If the status request fails.
        """
        status_url = f"{self.base_url}/status/{filename}"
        params = {'email': email}
        response = requests.get(status_url, params=params)

        if response.status_code != 200:
            raise Exception(f"Status request failed with status code: {response.status_code}")

        json_data = response.json()
        status = json_data['status']
        filename = json_data['filename']
        timestamp = datetime.strptime(json_data['timestamp'], '%Y%m%d%H%M%S')
        explanation = json_data['explanation']

        finish_time_str = json_data.get('finish_time')
        finish_time = datetime.strptime(finish_time_str, '%Y-%m-%d %H:%M:%S.%f') if finish_time_str else None

        return Status(status, filename, timestamp, explanation, finish_time)

    def history(self, email):
        """
        Retrieves a JSON summary of past uploads for a user based on their email.

        Args:
            email (str): The email address of the user.

        Returns:
            list: A list of upload summaries (dict objects).

        Raises:
            Exception: If the history request fails or the email is not valid.

        """
        history_url = f"{self.base_url}/history?email={email}"

        try:
            response = requests.get(history_url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"History request failed: {e}")
