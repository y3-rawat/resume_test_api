from flask import Flask, request, jsonify, render_template
from flask_cors import CORS



app = Flask(__name__)
# Configure CORS with specific options
cors = CORS(app, resources={
    r"/submit": {"origins": "*"}  # Allow all origins for the /submit endpoint
})

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/submit', methods=['GET'])
def submit():
    # Extract data from the URL parameters
    file_name = request.args.get('fileName', '')
    file_type = request.args.get('fileType', '')
    job_description = request.args.get('job_description', '')
    additional_information = request.args.get('additional_information', '')
    experience = request.args.get('experience', '')

    # Create a response dictionary
    response ={"res": {
       """ 'fileName': file_name,
        'fileType': file_type,
        'job_description': job_description,
        'additional_information': additional_information,
        'experience': experience"""
    }}

    # Return a JSON response
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
