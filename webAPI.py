from flask import Flask, request, jsonify
from pathlib import Path
import datetime
import uuid

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
        if email:
            user = session.query(User).filter_by(email=email).first()
            if not user:
                user = User(email=email)
                session.add(user)

        upload = Upload(
            uid=uid,
            filename=filename,
            upload_time=datetime.datetime.now(),
            status='pending',
            user=user
        )
        session.add(upload)
        session.commit()

        session.close()

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
                    :param uid_or_filename:

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
        # upload_files = app.config['UPLOAD_FOLDER'].glob('*')

        # for path in upload_files:
        #     if uid_or_filename in path.name:
        #         original_filename, timestamp, _ = path.name.rsplit('_', 2)
        #         output_file = f"output_{original_filename}_{timestamp}_{uid_or_filename}"
        #         if (app.config['UPLOAD_FOLDER'] / output_file).exists():

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

        # return jsonify({'status': 'not found', 'filename': None, 'timestamp': None, 'explanation': None})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
