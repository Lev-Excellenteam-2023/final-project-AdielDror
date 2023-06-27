import subprocess
import time
from client.webAppClient import WebAppClient

# Start the Web API
web_api_process = subprocess.Popen(["python", "webAPI.py"])

# Wait for the Web API to start
time.sleep(2)

# Start the Explainer
explainer_process = subprocess.Popen(["python", "explainer.py"])

# Wait for the Explainer to start
time.sleep(2)

# Create a WebAppClient instance
client = WebAppClient('http://127.0.0.1:5000')

try:
    # Upload a sample presentation
    file_path = 'data_structures_and_relavant_packages.pptx'
    uid = client.upload(file_path)
    print(f"Uploaded file. UID: {uid}")

    # Check the status of the presentation
    status_obj = client.status(uid)
    if status_obj.is_done():
        print("Upload is done!")
        print(f"Explanation: {status_obj.explanation}")
    else:
        print("Upload is still pending.")
finally:
    # Stop the Web API and Explainer
    web_api_process.terminate()
    explainer_process.terminate()
