from flask import Flask, request, jsonify
from pathlib import Path
import datetime
import uuid

from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = Path('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class WebAPI:

    @staticmethod
    @app.route('/upload', methods=['POST'])
    def upload():
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

        return jsonify({'uid': uid})

    @staticmethod
    @app.route('/status/<uid>', methods=['GET'])
    def status(uid):
        upload_files = app.config['UPLOAD_FOLDER'].glob('*')

        for path in upload_files:
            if uid in path.name:
                original_filename, timestamp, _ = path.name.rsplit('_', 2)
                output_file = f"output_{original_filename}_{timestamp}_{uid}"
                if (app.config['UPLOAD_FOLDER'] / output_file).exists():
                    return jsonify({
                        'status': 'done',
                        'filename': original_filename,
                        'timestamp': timestamp,
                        'explanation': 'Processed output for the upload'
                    })
                else:
                    return jsonify({
                        'status': 'pending',
                        'filename': original_filename,
                        'timestamp': timestamp,
                        'explanation': None
                    })

        return jsonify({'status': 'not found', 'filename': None, 'timestamp': None, 'explanation': None})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
