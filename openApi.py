# import os
import openai
import time


#
# # openai.api_key = os.getenv("OPENAI_API_KEY")
#
#
# openai.api_key = "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"
# messages = [
#     {"role": "system", "content": "You’re a kind helpful assistant"}
# ]
#
# while True:
#     content = input("User: ")
#     messages.append({"role": "user", "content": content})
#     completion = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=messages
#     )
#     chat_response = completion.choices[0].message.content
#     print(f'ChatGPT: {chat_response}')
#     messages.append({"role": "assistant", "content": chat_response})

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
