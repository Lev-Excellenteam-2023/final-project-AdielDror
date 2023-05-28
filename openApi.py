import openai
import time


class OpenAIAPI:
    def __init__(self, api_key, timeout_duration=15):
        self.api_key = api_key
        self.timeout_duration = timeout_duration

    def create_completion(self, prompt):
        openai.api_key = self.api_key
        try:
            start_time = time.time()
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                timeout=self.timeout_duration
            )
            elapsed_time = time.time() - start_time

            if elapsed_time >= self.timeout_duration:
                print("Request timed out.")
            else:
                return completion.choices[0].message.content

        except openai.error.OpenAIError as e:
            print("Error:", e)
