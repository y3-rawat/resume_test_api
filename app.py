from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit():
    # Extract data from the request
    file_name = request.form.get('fileName', '')
    file_type = request.form.get('fileType', '')
    job_description = request.form.get('job_description', '')
    additional_information = request.form.get('additional_information', '')
    experience = request.form.get('experience', '')

    # Handle the file upload if present
    if 'file' in request.files:
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_name = uploaded_file.filename
            # Save the file or process it as needed
            uploaded_file.save(f"/tmp/{file_name}")

    # Create a response dictionary
    response = {
        'fileName': file_name,
        'fileType': file_type,
        'job_description': job_description,
        'additional_information': additional_information,
        'experience': experience
    }

    # Return a JSON response
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
