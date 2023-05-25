# import pptx
# import openai
# import OpenApi
# import json
# import time
#
# openai.api_key = "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"
#
# # Define your completion prompt
# prompt = "Give me more explanation"
#
# # Set the timeout duration in seconds
# timeout_duration = 15
# file_name = "data structures and relavant packages"
# # Load the PowerPoint file
# all_slides = pptx.Presentation(file_name + '.pptx')
#
# storage_list = []
#
# # Loop through each slide in the PowerPoint file
# for slide in all_slides.slides:
#     string_of_slide = ""
#     # Loop through each shape in the slide
#     for shape in slide.shapes:
#         # Check if the shape is a text box
#         if hasattr(shape, 'text'):
#             # Print the text in the text box
#             # print(shape.text)
#             string_of_slide += shape.text
#             string_of_slide += " "
#
#     try:
#         # Start the timer
#         start_time = time.time()
#
#         completion = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "user", "content": string_of_slide + prompt}
#             ],
#             timeout=timeout_duration
#         )
#
#         # Calculate the elapsed time
#         elapsed_time = time.time() - start_time
#
#         # Check if the request timed out
#         if elapsed_time >= timeout_duration:
#             print("Request timed out.")
#         else:
#             # Handle the response
#             print(completion)
#
#     except openai.error.OpenAIError as e:
#         # Handle any errors from the API
#         print("Error:", e)
#
#     chat_response = completion.choices[0].message.content
#     print(f'ChatGPT: {chat_response}')
#     # Wait for 20 seconds before making the next request
#     time.sleep(20)
#     storage_list += [chat_response]
#     print(storage_list)
#
#
# # Write the JSON string to a file
# with open(file_name + '.json', 'w') as file:
#     json.dump(storage_list, file, indent=4)
#     # file.write(json_data)
#     file.close()
#
#
from presentationAnalyzer import PresentationAnalyzer

if __name__ == '__main__':
    file_name = "data structures and relavant packages"
    api_key = "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"

    presentation_analyzer = PresentationAnalyzer(file_name, api_key)
    presentation_analyzer.analyze_presentation()
