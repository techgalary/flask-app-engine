### Flask Image Upload App (Google Cloud Storage + Cloud Datastore)
#### This is a Flask web application that allows users to:
#### ✅ Upload images 📤
#### ✅ Store images in Google Cloud Storage 🗂️
#### ✅ Save metadata in Google Cloud Datastore 📊
#### ✅ View previously uploaded images 👀


### 📂 Project Structure
``` bash
flask-app-gcp/
│── templates/
│   └── homepage.html    # UI for image upload & display
│── tests/               # Unit & integration tests
│   ├── test.py          # Flask app tests
│── main.py              # Flask application
│── Dockerfile           # Defines Cloud Run container
│── requirements.txt     # Python dependencies
│── .gcloudignore        # Ignore unnecessary files
│── README.md            # Documentation

```

### 🚀 Setup on Google Cloud Shell
#### 1️⃣ Clone the Repository from GitHub
``` bash
git clone https://github.com/<your-github-username>/flask-app-gcp.git
cd flask-app-gcp
```

#### 2️⃣ Install Dependencies
``` bash
pip install -r requirements.txt
```

#### 3️⃣ Authenticate Google Cloud Account
``` bash
gcloud auth login
gcloud config set project <your-project-id>

```
### Setting Up Google Cloud Storage
#### 1️⃣ Create a Storage Bucket
``` bash
export PROJECT_ID=$(gcloud config get-value project)
export BUCKET_NAME=${PROJECT_ID}-image-uploads
```
```
gcloud storage buckets create gs://${BUCKET_NAME} --location=us-central1
```

### 2️⃣ Grant Permissions
``` bash
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member=allUsers \
    --role=roles/storage.objectViewer
```

### 3️⃣ Run the Flask App Locally
```
python main.py
Open http://127.0.0.1:8080/ in your browser.
```
### Deploy to Google Cloud Run

#### 1️⃣ Enable Required Services
``` bash
gcloud services enable run.googleapis.com
```
#### 2️⃣ Build and Push Docker Image
```
gcloud builds submit --tag gcr.io/$(gcloud config get-value project)/flask-app
```

### Deploy to Google Cloud Run
#### 1️⃣ Enable Required Services
``` bash
gcloud services enable run.googleapis.com storage.googleapis.com datastore.googleapis.com
```

#### 2️⃣ Build and Push Docker Image
``` bash
gcloud builds submit --tag gcr.io/${PROJECT_ID}/flask-app
```
#### 3️⃣ Deploy to Cloud Run
``` bash
gcloud run deploy flask-app \
  --image gcr.io/${PROJECT_ID}/flask-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars CLOUD_STORAGE_BUCKET=${BUCKET_NAME}
```
#### 4️⃣ Access the Application
```
gcloud run services describe flask-app --region us-central1 --format='value(status.url)'
```
