## Deploy a Flask App on Google Cloud Run with Image Upload & Metadata Storage
#### This is a Flask web application that allows users to:
#### ✅ Upload images to Google Cloud Storage (GCS)
#### ✅ Store metadata (filename, URL, timestamp) in Google Cloud Datastore 
#### ✅ View previously uploaded images via Flask UI 
#### ✅ Deploy the app serverlessly on Google Cloud Run


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
│── .gitignore        # Ignore unnecessary files
│── README.md            # Documentation

```

## 🚀 Setup on Google Cloud Shell
#### 1️⃣ Clone the Repository from GitHub
``` bash
git clone https://github.com/techgalary/flask-app-engine.git
cd flask-app-engine/

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

### Create a Service Account for Deployment

#### 1️⃣ Create the Service Account
```
export SERVICE_ACCOUNT=flask-deploy-sa
gcloud iam service-accounts create $SERVICE_ACCOUNT \
    --description="Service Account for Deployment" \
    --display-name="Flask Deployment Service Account"
```

#### 2️⃣ Grant Permissions to the Service Account
##### Storage Access
```
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role=roles/storage.admin
```
##### Cloud Build Permissions
```
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role=roles/cloudbuild.builds.editor
```
##### Cloud Run Deployment Permissions
```
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role=roles/run.admin
```
##### Datastore Permissions
```
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role=roles/datastore.user
```
### Setting Up Google Cloud Datastore
#### Google Cloud Datastore is used to store metadata for each uploaded image.

#### 1️⃣ Enable Datastore API
```
gcloud services enable datastore.googleapis.com
```

#### 2️⃣ Initialize Datastore
```
gcloud firestore databases create --location=us-central1 --type=datastore-mode
```
#### 3️⃣ Verify Metadata Storage
##### After uploading images, you can check stored metadata using:
```
gcloud datastore indexes list
```
### Deploy to Google Cloud Run
#### 1️⃣ Enable Required Services
```
gcloud services enable run.googleapis.com storage.googleapis.com datastore.googleapis.com
```
#### 2️⃣ Authenticate as the Service Account
```
gcloud auth activate-service-account ${SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com --key-file=service-account-key.json
```
#### 3️⃣ Build and Push Docker Image
```
gcloud builds submit --tag gcr.io/${PROJECT_ID}/flask-app
```
#### 4️⃣ Deploy to Cloud Run
```
gcloud run deploy flask-app \
  --image gcr.io/${PROJECT_ID}/flask-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --service-account=${SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com \
  --set-env-vars CLOUD_STORAGE_BUCKET=${BUCKET_NAME}
```
#### 5️⃣ Get the URL of the Deployed Application
```
gcloud run services describe flask-app --region us-central1 --format='value(status.url)'
```
## Cleanup - Remove Resources After Lab Completion
### To avoid unnecessary charges, remove all created resources when done.

#### 1️⃣ Delete the Cloud Run Service
```
gcloud run services delete flask-app --region us-central1
```
#### 2️⃣ Delete the Container Image from Artifact Registry
```
gcloud artifacts docker images delete gcr.io/${PROJECT_ID}/flask-app --delete-tags
```
#### 3️⃣ Delete the Cloud Storage Bucket
```
gcloud storage rm -r buckets delete gs://${PROJECT_ID}-image-uploads
gcloud storage buckets delete gs://${BUCKET_NAME}
```
#### 4️⃣ Delete Firestore (Datastore)
```
gcloud firestore databases delete --location=us-central1
```
#### 5️⃣ Delete the IAM Service Account
```
gcloud iam service-accounts delete $SERVICE_ACCOUNT@${PROJECT_ID}.iam.gserviceaccount.com
```
