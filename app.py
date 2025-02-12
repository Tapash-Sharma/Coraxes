from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'eml', 'html', ''])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Check allowed file type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        # Run Phishector.py
        try:
            subprocess.check_call(['python', 'coraxes.py'])
        except subprocess.CalledProcessError as e:
            return jsonify({'error': 'Error running Phishector.py: {}'.format(str(e))}), 500

        # Read features_list.txt
        try:
            with open('features_list.txt', 'r') as f:
                features_data = f.read()
        except IOError:
            return jsonify({'error': 'features_list.txt not found'}), 500

        # Read model_predictions.txt
        try:
            with open('model_predictions.txt', 'r') as f:
                predictions_data = f.readlines()
        except IOError:
            return jsonify({'error': 'model_predictions.txt not found'}), 500

        # Parse Predictions
        spam_count = sum(1 for line in predictions_data if "['S']" in line)
        healthy_count = sum(1 for line in predictions_data if "['H']" in line)
        
        final_decision = 'Malicious' if spam_count > healthy_count else 'Healthy'

        response = {
            'features': features_data,
            'predictions': [line.strip() for line in predictions_data],
            'final_result': final_decision
        }
        os.remove(file_path)


        return jsonify(response), 200
    
    return jsonify({'error': 'File type not allowed'}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
