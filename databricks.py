from flask import Flask, request
from databricks.sdk import WorkspaceClient
import io

app = Flask(__name__)
w = WorkspaceClient()

@app.route('/upload', methods=['POST'])
def upload_to_volume():
    # Get file and volume details from form
    uploaded_file = request.files['file']
    catalog = request.form.get('catalog')
    schema = request.form.get('schema')
    volume_name = request.form.get('volume_name')
    target_path = request.form.get('target_path', '')
    
    # Construct full volume path
    volume_base = f"/Volumes/{catalog}/{schema}/{volume_name}"
    full_path = f"{volume_base}/{target_path}/{uploaded_file.filename}" if target_path else f"{volume_base}/{uploaded_file.filename}"

    # Convert file to binary stream
    file_bytes = uploaded_file.read()
    binary_data = io.BytesIO(file_bytes)

    # Execute upload
    w.files.upload(full_path, binary_data, overwrite=True)
    
    return f"File uploaded to {full_path}", 200
