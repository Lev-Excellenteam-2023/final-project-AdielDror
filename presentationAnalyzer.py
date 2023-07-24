import asyncio
import powerPointProcessor
import json

from openApi import OpenAIAPI


class PresentationAnalyzer:
    """
    Class for analyzing presentations.
    """

    def __init__(self, file_name, api_key):
        """
        Initializes the PresentationAnalyzer object.

        Args:
            file_name (str): The name of the presentation file.
            api_key (str): The API key for the OpenAI service.
        """
        self.file_name = file_name
        self.api_key = api_key

    async def analyze_slide(self, openai_api, slide_text):
        """
        Analyzes a slide of the presentation using the OpenAI service.

        Args:
             openai_api (OpenAIAPI): An instance of the OpenAIAPI class.
             slide_text (str): The text content of the slide.

        Returns:
             str or None: The response from the OpenAI service, or None if the slide is empty.
        """
        if not slide_text.strip():  # Check if the slide text is empty or contains only whitespace
            print("Empty slide text:", slide_text)
            return None

        prompt = slide_text + " Give me more explanation"
        chat_response = await openai_api.create_completion(prompt)
        return chat_response

    async def analyze_presentation(self):
        """
        Analyzes the presentation file using the OpenAI service.
        """
        powerpoint = powerPointProcessor.PowerPointProcessor(self.file_name)
        powerpoint.load_presentation()
        slides = powerpoint.process_slides()

        openai_api = OpenAIAPI(self.api_key)

        storage_list = []
        tasks = [self.analyze_slide(openai_api, slide_text) for slide_text in slides]
        slide_response = await asyncio.gather(*tasks)

        for response in slide_response:
            if response is not None:
                storage_list.append(f'ChatGPT: {response}')
                print(f'ChatGPT: {response}')
            else:
                print("Slide analysis skipped.")

        # Write the JSON string to a file
        with open('outputs/' + str(self.file_name.name.split("_")[-1]) + '.json', 'w') as file:
            json.dump(storage_list, file, indent=4)
