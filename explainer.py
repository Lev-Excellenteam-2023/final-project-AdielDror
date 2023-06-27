import asyncio
from pathlib import Path

from presentationAnalyzer import PresentationAnalyzer
import os
from flask import Flask

app = Flask(__name__)

UPLOAD_FOLDER = Path('uploads')
OUTPUT_FOLDER = Path('outputs')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER


async def process_file(file_name):
    """
    Processes a file by analyzing its presentation content and saving the explanation.

    Args:
        file_name (str): The name of the file to process.

    Returns:
        None

    Raises:
        FileNotFoundError: If the file does not exist.
        Exception: If an error occurs during presentation analysis.

    """
    api_key = os.getenv("OPENAI_API_KEY")

    presentation_analyzer = PresentationAnalyzer(file_name, api_key)
    await presentation_analyzer.analyze_presentation()
    print(f"Explanation saved for file: {file_name}")

    # Remove the processed file from the uploads folder
    file_name.unlink()


async def process_new_files():
    """
    Processes newly uploaded files by analyzing their presentation content and saving the explanation.

    This function iterates over the files in the upload folder and checks if their corresponding output files exist
    in the output folder. If an output file doesn't exist, it means the corresponding presentation file hasn't been
    processed yet. In that case, the function calls the `process_file` function to analyze the presentation.

    Args:
        None

    Returns:
        None

    """
    uploaded_files = app.config['UPLOAD_FOLDER'].glob('*')

    for file_name in uploaded_files:
        output_filename = f"output_{file_name.name}"
        output_path = app.config['OUTPUT_FOLDER'] / output_filename

        if not output_path.exists():
            print(f"Processing file: {file_name}")
            await process_file(file_name)


async def main():
    while True:
        await process_new_files()
        await asyncio.sleep(10)


if __name__ == '__main__':
    asyncio.run(main())
