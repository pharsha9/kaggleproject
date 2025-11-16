# 🚀 Deployment Guide

This guide provides comprehensive instructions for deploying the BI Intelligence Agent System to production environments.

---

## Table of Contents

1. [Local Deployment](#local-deployment)
2. [Docker Deployment](#docker-deployment)
3. [Google Cloud Run Deployment](#google-cloud-run-deployment)
4. [Vertex AI Agent Engine Deployment](#vertex-ai-agent-engine-deployment)
5. [Environment Configuration](#environment-configuration)
6. [Monitoring & Logging](#monitoring--logging)
7. [Scaling Considerations](#scaling-considerations)

---

## Local Deployment

### Prerequisites
- Python 3.9+
- pip package manager
- Google AI API key

### Steps

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your API key
```

3. **Run the system**
```bash
python main.py analyze data/examples/sales_data.csv
```

---

## Docker Deployment

### Create Dockerfile

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/data /app/outputs /app/reports /app/memory

# Set environment variable
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["python", "main.py", "analyze", "data/examples/sales_data.csv"]
```

### Build and Run

```bash
# Build Docker image
docker build -t bi-agent-system .

# Run container
docker run -it \
  -e GOOGLE_API_KEY=your_api_key \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/outputs:/app/outputs \
  -v $(pwd)/reports:/app/reports \
  bi-agent-system

# Or run with custom data
docker run -it \
  -e GOOGLE_API_KEY=your_api_key \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/outputs:/app/outputs \
  -v $(pwd)/reports:/app/reports \
  bi-agent-system \
  python main.py analyze /app/data/your_data.csv
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  bi-agent:
    build: .
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - DEFAULT_MODEL=gemini-2.0-flash-exp
      - TEMPERATURE=0.7
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/app/data
      - ./outputs:/app/outputs
      - ./reports:/app/reports
      - ./memory:/app/memory
    command: python demo.py
```

Run with:
```bash
docker-compose up
```

---

## Google Cloud Run Deployment

### Prerequisites
- Google Cloud account
- gcloud CLI installed and configured
- Project with billing enabled

### Deployment Steps

1. **Enable required APIs**
```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

2. **Create app.yaml for Cloud Run**

```yaml
# app.yaml
runtime: python311

env_variables:
  GOOGLE_API_KEY: "your_api_key_here"
  DEFAULT_MODEL: "gemini-2.0-flash-exp"
  TEMPERATURE: "0.7"

automatic_scaling:
  min_instances: 0
  max_instances: 10
  
resources:
  cpu: 2
  memory: 4Gi
```

3. **Create Procfile**

```
# Procfile
web: python main.py analyze data/examples/sales_data.csv
```

4. **Deploy to Cloud Run**

```bash
# Set your project ID
export PROJECT_ID=your-gcp-project-id
gcloud config set project $PROJECT_ID

# Deploy
gcloud run deploy bi-agent-system \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 4Gi \
  --cpu 2 \
  --timeout 900 \
  --set-env-vars GOOGLE_API_KEY=your_api_key
```

5. **Access your deployment**
```bash
# Get the service URL
gcloud run services describe bi-agent-system \
  --region us-central1 \
  --format 'value(status.url)'
```

### Cloud Run with Container

1. **Build and push container**
```bash
# Build container
gcloud builds submit --tag gcr.io/$PROJECT_ID/bi-agent-system

# Deploy container
gcloud run deploy bi-agent-system \
  --image gcr.io/$PROJECT_ID/bi-agent-system \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 4Gi \
  --set-env-vars GOOGLE_API_KEY=your_api_key
```

### Using Cloud Storage for Data

```python
# Modified config.py for Cloud Storage
from google.cloud import storage

class Config:
    # ... existing config ...
    
    # Cloud Storage configuration
    USE_CLOUD_STORAGE = os.getenv("USE_CLOUD_STORAGE", "false").lower() == "true"
    GCS_BUCKET = os.getenv("GCS_BUCKET", "")
    
    @classmethod
    def get_data_path(cls, filename):
        if cls.USE_CLOUD_STORAGE:
            # Download from GCS
            storage_client = storage.Client()
            bucket = storage_client.bucket(cls.GCS_BUCKET)
            blob = bucket.blob(filename)
            local_path = f"/tmp/{filename}"
            blob.download_to_filename(local_path)
            return local_path
        else:
            return cls.DATA_DIR / filename
```

---

## Vertex AI Agent Engine Deployment

### Prerequisites
- Google Cloud project with Vertex AI enabled
- Appropriate IAM permissions

### Steps

1. **Enable Vertex AI API**
```bash
gcloud services enable aiplatform.googleapis.com
```

2. **Create agent configuration**

```python
# vertex_agent_config.py
from google.cloud import aiplatform

def deploy_to_vertex_ai():
    """Deploy BI Agent to Vertex AI Agent Engine."""
    
    aiplatform.init(
        project='your-project-id',
        location='us-central1'
    )
    
    # Define agent configuration
    agent_config = {
        "display_name": "BI Intelligence Agent",
        "description": "Multi-agent business intelligence analyzer",
        "agent_type": "CONVERSATIONAL",
        "tools": [
            {
                "name": "data_ingestion",
                "description": "Load and process data files"
            },
            {
                "name": "statistical_analysis",
                "description": "Perform statistical analysis"
            },
            {
                "name": "visualization",
                "description": "Create data visualizations"
            }
        ]
    }
    
    # Deploy agent
    agent = aiplatform.Agent.create(**agent_config)
    
    print(f"Agent deployed: {agent.resource_name}")
    return agent

if __name__ == "__main__":
    deploy_to_vertex_ai()
```

3. **Deploy**
```bash
python vertex_agent_config.py
```

---

## Environment Configuration

### Production Environment Variables

Create a `.env.production` file:

```bash
# API Configuration
GOOGLE_API_KEY=your_production_api_key

# Model Configuration
DEFAULT_MODEL=gemini-2.0-flash-exp
TEMPERATURE=0.7

# Logging
LOG_LEVEL=INFO
ENABLE_TRACING=true

# Cloud Storage (if using)
USE_CLOUD_STORAGE=true
GCS_BUCKET=your-bucket-name

# Performance
MAX_WORKERS=4
TIMEOUT_SECONDS=300

# Security
ENABLE_API_KEY_ROTATION=true
```

### Secret Management

#### Google Secret Manager

```bash
# Store API key in Secret Manager
echo -n "your_api_key" | gcloud secrets create google-api-key \
  --data-file=- \
  --replication-policy="automatic"

# Grant access to Cloud Run
gcloud secrets add-iam-policy-binding google-api-key \
  --member="serviceAccount:YOUR_SERVICE_ACCOUNT" \
  --role="roles/secretmanager.secretAccessor"
```

Update your Cloud Run deployment:
```bash
gcloud run deploy bi-agent-system \
  --source . \
  --set-secrets GOOGLE_API_KEY=google-api-key:latest
```

---

## Monitoring & Logging

### Cloud Logging Setup

```python
# Enhanced observability.py for Cloud Logging
import google.cloud.logging

class CloudObservabilityManager(ObservabilityManager):
    def __init__(self):
        super().__init__()
        
        # Initialize Cloud Logging
        if Config.USE_CLOUD_LOGGING:
            client = google.cloud.logging.Client()
            client.setup_logging()
    
    def log_to_cloud(self, severity, message, **kwargs):
        """Log to Google Cloud Logging."""
        logger = google.cloud.logging.Logger("bi-agent-system")
        logger.log_struct({
            "message": message,
            "severity": severity,
            **kwargs
        })
```

### Metrics Dashboard

Create a Cloud Monitoring dashboard:

```bash
# metrics_dashboard.json
{
  "displayName": "BI Agent Metrics",
  "dashboardFilters": [],
  "gridLayout": {
    "widgets": [
      {
        "title": "Agent Calls",
        "xyChart": {
          "dataSets": [{
            "timeSeriesQuery": {
              "timeSeriesFilter": {
                "filter": "resource.type=\"cloud_run_revision\" AND metric.type=\"custom.googleapis.com/agent_calls\""
              }
            }
          }]
        }
      },
      {
        "title": "Processing Time",
        "xyChart": {
          "dataSets": [{
            "timeSeriesQuery": {
              "timeSeriesFilter": {
                "filter": "resource.type=\"cloud_run_revision\" AND metric.type=\"custom.googleapis.com/processing_time\""
              }
            }
          }]
        }
      }
    ]
  }
}
```

Deploy dashboard:
```bash
gcloud monitoring dashboards create --config-from-file=metrics_dashboard.json
```

---

## Scaling Considerations

### Horizontal Scaling

**Cloud Run Auto-scaling:**
```bash
gcloud run services update bi-agent-system \
  --min-instances=2 \
  --max-instances=100 \
  --concurrency=10
```

### Vertical Scaling

**Increase resources:**
```bash
gcloud run services update bi-agent-system \
  --memory=8Gi \
  --cpu=4
```

### Performance Optimization

1. **Enable Caching**
```python
# Add to config.py
ENABLE_RESULT_CACHE = True
CACHE_TTL_SECONDS = 3600
```

2. **Async Processing**
```python
# Use asyncio for parallel operations
import asyncio

async def parallel_analysis(df):
    tasks = [
        analyze_correlations(df),
        detect_outliers(df),
        create_visualizations(df)
    ]
    results = await asyncio.gather(*tasks)
    return results
```

3. **Database Connection Pooling**
```python
# For database sources
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=40
)
```

### Cost Optimization

1. **Use preemptible instances** for non-critical workloads
2. **Implement request batching** to reduce API calls
3. **Cache frequently analyzed datasets**
4. **Use Cloud Storage lifecycle policies** for old reports

---

## Health Checks

### Create health check endpoint

```python
# health.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "bi-agent-system",
        "version": "1.0.0"
    })

@app.route('/ready')
def ready():
    """Readiness check."""
    # Check if system is ready
    try:
        Config.validate()
        return jsonify({"status": "ready"})
    except Exception as e:
        return jsonify({"status": "not ready", "error": str(e)}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

---

## Troubleshooting

### Common Issues

**Issue: API key not found**
```bash
# Solution: Verify environment variable
echo $GOOGLE_API_KEY

# Or check Secret Manager
gcloud secrets versions access latest --secret="google-api-key"
```

**Issue: Memory errors**
```bash
# Solution: Increase Cloud Run memory
gcloud run services update bi-agent-system --memory=8Gi
```

**Issue: Timeout errors**
```bash
# Solution: Increase timeout
gcloud run services update bi-agent-system --timeout=15m
```

---

## Security Best Practices

1. **Never commit API keys** to version control
2. **Use Secret Manager** for sensitive data
3. **Enable IAM authentication** for production
4. **Implement rate limiting** on API endpoints
5. **Regular security audits** of dependencies
6. **Use least privilege** for service accounts

---

## Production Checklist

- [ ] API keys stored in Secret Manager
- [ ] Monitoring dashboard configured
- [ ] Logging enabled and configured
- [ ] Health checks implemented
- [ ] Auto-scaling configured
- [ ] Backup strategy for memory/sessions
- [ ] Error alerting configured
- [ ] Load testing completed
- [ ] Security audit passed
- [ ] Documentation updated

---

## Support & Maintenance

### Logs Access
```bash
# View Cloud Run logs
gcloud run logs tail bi-agent-system --region=us-central1

# Filter by severity
gcloud run logs tail bi-agent-system --region=us-central1 --log-filter="severity>=ERROR"
```

### Updating Deployment
```bash
# Deploy new version
gcloud run deploy bi-agent-system \
  --source . \
  --region us-central1

# Rollback if needed
gcloud run services update-traffic bi-agent-system \
  --to-revisions=PREVIOUS_REVISION=100
```

---

**For additional support, consult the [README.md](README.md) or Google Cloud documentation.**

