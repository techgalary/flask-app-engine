Flask Image Upload App (Google Cloud Storage + Cloud Datastore)
This is a Flask web application that allows users to:
✅ Upload images 📤
✅ Store images in Google Cloud Storage 🗂️
✅ Save metadata in Google Cloud Datastore 📊
✅ View previously uploaded images 👀

Deployed using Google Cloud Run for cost-efficient, serverless hosting.

📂 Project Structure
php
Copy
Edit
flask-app-gcp/
│── templates/
│   └── homepage.html    # UI for image upload & display
│── static/              # (Optional) Static assets (CSS, JS)
│── tests/               # Unit & integration tests
│   ├── test_main.py     # Flask app tests
│── main.py              # Flask application
│── Dockerfile           # Defines Cloud Run container
│── requirements.txt     # Python dependencies
│── .gcloudignore        # Ignore unnecessary files
│── README.md            # Documentation
🚀 Setup on Google Cloud Shell
1️⃣ Clone the Repository from GitHub
sh
Copy
Edit
git clone https://github.com/<your-github-username>/flask-app-gcp.git
cd flask-app-gcp
2️⃣ Install Dependencies
sh
Copy
Edit
pip install -r requirements.txt
3️⃣ Set Up Google Cloud Credentials
Replace <your-cloud-storage-bucket> with your actual bucket name:

sh
Copy
Edit
export CLOUD_STORAGE_BUCKET="<your-cloud-storage-bucket>"
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/key.json"
(Ensure you've uploaded your service account key key.json to Cloud Shell.)

4️⃣ Run the Flask App Locally
sh
Copy
Edit
python main.py
Open http://127.0.0.1:8080/ in your browser. 🎉

📦 Deploy to Google Cloud Run
1️⃣ Enable Required Services
sh
Copy
Edit
gcloud services enable run.googleapis.com
2️⃣ Build and Push Docker Image
sh
Copy
Edit
gcloud builds submit --tag gcr.io/$(gcloud config get-value project)/flask-app
3️⃣ Deploy to Cloud Run
sh
Copy
Edit
gcloud run deploy flask-app \
  --image gcr.io/$(gcloud config get-value project)/flask-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
4️⃣ Open the Application
sh
Copy
Edit
gcloud run services describe flask-app --region us-central1 --format='value(status.url)'
This will return the public URL where your app is hosted! 🌍

🧪 Running Tests
1️⃣ Install pytest
sh
Copy
Edit
pip install pytest
2️⃣ Run Tests
sh
Copy
Edit
pytest tests/