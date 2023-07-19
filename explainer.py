import asyncio
import datetime
from pathlib import Path

from db.database import Session
from db.orm import Upload
from presentationAnalyzer import PresentationAnalyzer
import os
from flask import Flask

app = Flask(__name__)

UPLOAD_FOLDER = Path('db/uploads')
OUTPUT_FOLDER = Path('outputs')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER


async def process_file(session, upload_id, file_name):
    """
    Processes a file by analyzing its presentation content and saving the explanation.

    Args:
        session: SQLAlchemy session object.
        upload_id (int): The ID of the upload in the database.
        file_name (str): The name of the file to process.

    Returns:
        None

    Raises:
        FileNotFoundError: If the file does not exist.
        Exception: If an error occurs during presentation analysis.

    """
    api_key = os.getenv("OPENAI_API_KEY")

    presentation_analyzer = PresentationAnalyzer(file_name, api_key)
    explanation = await presentation_analyzer.analyze_presentation()

    # Save the explanation to the database
    upload = session.query(Upload).filter_by(id=upload_id).first()
    upload.explanation = explanation
    upload.finish_time = datetime.datetime.now()
    upload.status = 'done'
    session.commit()

    print(f"Explanation saved for file: {file_name}")

    # Remove the processed file from the uploads folder
    file_name.unlink()


async def process_new_files():
    """
    Processes newly uploaded files by analyzing their presentation content and saving the explanation.

    This function queries the database for pending uploads and processes each upload that doesn't have an output
    file yet. It calls the `process_file` function to analyze the presentation and save the explanation.

    Args:
        None

    Returns:
        None

    """
    session = Session()

    # Find pending uploads in the database
    pending_uploads = session.query(Upload).filter_by(status='pending').all()

    for upload in pending_uploads:
        file_name = app.config['UPLOAD_FOLDER'] / upload.uid

        # for file_name in uploaded_files:
        output_filename = f"output_{upload.uid}.json"
        output_path = app.config['OUTPUT_FOLDER'] / output_filename

        if not output_path.exists():
            print(f"Processing file: {file_name}")
            try:
                await process_file(session, upload.id, file_name)
            except Exception as e:
                # Handle any errors during presentation analysis
                print(f"Error processing file: {file_name}. Error: {e}")
                upload.status = 'failed'
                session.commit()

    session.close()


async def main():
    while True:
        await process_new_files()
        await asyncio.sleep(10)


if __name__ == '__main__':
    asyncio.run(main())
