import powerPointProcessor
import time
import json

from openApi import OpenAIAPI


class PresentationAnalyzer:
    def __init__(self, file_name, api_key):
        self.file_name = file_name
        self.api_key = api_key

    def analyze_presentation(self):
        powerpoint = powerPointProcessor.PowerPointProcessor(self.file_name)
        powerpoint.load_presentation()
        slides = powerpoint.process_slides()

        openai_api = OpenAIAPI(self.api_key)

        storage_list = []
        for slide_text in slides:
            prompt = slide_text + " Give me more explanation"
            chat_response = openai_api.create_completion(prompt)
            storage_list.append(chat_response)
            print(f'ChatGPT: {chat_response}')
            time.sleep(20)

        # Write the JSON string to a file
        with open(self.file_name + '.json', 'w') as file:
            json.dump(storage_list, file, indent=4)
