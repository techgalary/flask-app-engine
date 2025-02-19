import os
from flask import Flask, request, render_template, redirect, url_for
from google.cloud import storage, datastore
import datetime

app = Flask(__name__)
CLOUD_STORAGE_BUCKET = os.environ.get("CLOUD_STORAGE_BUCKET")

storage_client = storage.Client()
datastore_client = datastore.Client()

@app.route('/')
def homepage():
    query = datastore_client.query(kind="Images")
    images = list(query.fetch())
    return render_template("homepage.html", images=images)

@app.route('/upload', methods=['POST'])
def upload_image():
    image = request.files['file']
    if not image:
        return "No file uploaded", 400
    
    bucket = storage_client.bucket(CLOUD_STORAGE_BUCKET)
    blob = bucket.blob(image.filename)
    blob.upload_from_file(image)
    blob.make_public()
    
    entity = datastore.Entity(datastore_client.key("Images"))
    entity.update({
        "filename": image.filename,
        "url": blob.public_url,
        "uploaded_at": datetime.datetime.utcnow()
    })
    datastore_client.put(entity)

    return redirect(url_for('homepage'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
