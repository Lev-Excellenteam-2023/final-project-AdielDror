from flask import Flask, request, jsonify
from pathlib import Path
import datetime
import uuid
from email_validator import validate_email, EmailNotValidError
from sqlalchemy import desc
from werkzeug.utils import secure_filename

from db.database import Session
from db.orm import User, Upload

app = Flask(__name__)

UPLOAD_FOLDER = Path('db/uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class WebAPI:

    @staticmethod
    @app.route('/upload', methods=['POST'])
    def upload():
        """
        Handles the file upload request.

        This method expects a file to be attached to the request with the key 'file'.
        It saves the uploaded file to the specified upload folder, generating a unique filename
        based on the original filename, timestamp, and a UUID.

        If an email parameter is provided in the request, it associates the upload with an existing user
        or creates a new user.

        Returns:
            jsonify: A JSON response containing the unique identifier (UID) of the uploaded file.

        """
        if 'file' not in request.files:
            return jsonify({'error': 'No file attached'})

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'})

        uid = str(uuid.uuid4())
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        filename = secure_filename(file.filename)
        new_filename = f"{filename}_{timestamp}_{uid}"
        file.save(app.config['UPLOAD_FOLDER'] / new_filename)

        email = request.form.get('email')
        session = Session()

        user = None
        try:
            if email:
                valid_email = validate_email(email)
                email = valid_email.email

            user = session.query(User).filter_by(email=email).first()
            if not user:
                user = User(email=email)
                session.add(user)

            upload = Upload(
                uid=uid,
                filename=filename,
                upload_time=datetime.datetime.now(),
                finish_time=None,
                status='pending',
                user=user
            )
            session.add(upload)
            session.commit()

            session.close()

        except EmailNotValidError as e:
            return jsonify({'error': str(e)})

        return jsonify({'uid': uid})

    @staticmethod
    @app.route('/status/<uid_or_filename>', methods=['GET'])
    def status(uid_or_filename):
        """
        Retrieves the status of a file upload based on its unique identifier (UID) or filename and email.

        If a UID is provided, it fetches the upload from the database using the UID.
        If a filename and email are provided, it fetches the latest upload with that filename for the given email.

        Returns:
            jsonify: A JSON response containing the status information of the file upload.
                - If the processed output file exists, returns:
                    {
                        'status': 'done',
                        'filename': filename,
                        'timestamp': timestamp,
                        'explanation': 'Processed output for the upload'
                    }
                - If the processed output file does not exist, returns:
                    {
                        'status': 'pending',
                        'filename': filename,
                        'timestamp': timestamp,
                        'explanation': None
                    }
                - If the file with the specified UID or filename is not found, returns:
                    {
                        'status': 'not found',
                        'filename': None,
                        'timestamp': None,
                        'explanation': None
                    }

        """
        session = Session()

        upload = session.query(Upload).filter_by(uid=uid_or_filename).first()

        if not upload:
            # If not found by UID, try to find the latest upload with the specified filename for the given email
            email = request.args.get('email')
            user = session.query(User).filter_by(email=email).first()
            if user:
                upload = (
                    session.query(Upload)
                    .filter_by(filename=uid_or_filename, user=user)
                    .order_by(Upload.upload_time.desc())
                    .first()
                )
        if not upload:
            session.close()  # Close the session before returning the response
            return jsonify({'status': 'not found', 'filename': None, 'timestamp': None, 'explanation': None})

        filename = upload.filename
        timestamp = upload.upload_time.strftime('%Y%m%d%H%M%S')
        output_file = app.config['UPLOAD_FOLDER'] / f"output_{upload.uid}"

        if output_file.exists():
            response = jsonify({
                'status': 'done',
                'filename': filename,
                'timestamp': timestamp,
                'explanation': 'Processed output for the upload'
            })
        else:
            response = jsonify({
                'status': 'pending',
                'filename': filename,
                'timestamp': timestamp,
                'explanation': None
            })

        session.close()  # Close the session before returning the response
        return response

    @staticmethod
    @app.route('/history', methods=['GET'])
    def history():
        """
        Retrieves a JSON summary of past uploads for a user based on their email.

        The email is provided as a URL parameter.

        Returns:
            jsonify: A JSON response containing a list of upload summaries.

        """
        email = request.args.get('email')

        if not email:
            return jsonify({'error:' 'Email parameter is missing'}), 400

        try:
            valid_email = validate_email(email)
            email = valid_email.ascii_email
        except EmailNotValidError as e:
            return jsonify({'error': str(e)}), 400

        session = Session()

        user = session.query(User).filter_by(email=email).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        uploads = (
            session.query(Upload)
                .filter_by(user=user)
                .order_by(desc(Upload.upload_time))
                .all()
        )

        upload_summaries = []
        for upload in uploads:
            summary = {
                'uid': upload.uid,
                'filename': upload.filename,
                'upload_time': upload.upload_time.strftime('%Y-%m-%d %H:%M:%S'),
                'status': upload.status
            }
            upload_summaries.append(summary)

        return jsonify(upload_summaries)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
