import asyncio
import functools
import openai
import time


class OpenAIAPI:
    """
    Class for interacting with the OpenAI API.
    """
    def __init__(self, api_key, timeout_duration=180):
        """
        Initializes the OpenAIAPI object.

        Args:
            api_key (str): The API key for the OpenAI service.
            timeout_duration (int, optional): The maximum duration (in seconds) to wait for a response from the API.
                                              Defaults to 180 seconds.
        """
        self.api_key = api_key
        self.timeout_duration = timeout_duration

    async def create_completion(self, prompt):
        """
        Creates a chat-based completion using the OpenAI API.

        Args:
            prompt (str): The input prompt for the completion.

        Returns:
            str: The completion response from the OpenAI API.
        """
        openai.api_key = self.api_key
        try:
            start_time = time.time()
            loop = asyncio.get_event_loop()
            partial_function = functools.partial(openai.ChatCompletion.create,
                                                 model="gpt-3.5-turbo",
                                                 messages=[{"role": "user", "content": prompt}],
                                                 timeout=self.timeout_duration)

            completion = await loop.run_in_executor(None, partial_function)
            elapsed_time = time.time() - start_time

            if elapsed_time >= self.timeout_duration:
                print("Request timed out.")
            else:
                return completion.choices[0].message.content

        except openai.error.RateLimitError:
            print("Rate limit reached. Waiting for 20 seconds.")
            time.sleep(20)
            return await self.create_completion(prompt)

        except openai.error.OpenAIError as e:
            print("Error:", e)

