# Docker Deployment Guide - Comment Analyzer

## 🐳 Docker Configuration Overview

### Bootstrap Contract
The application implements a **multi-stage bootstrap process** ensuring proper initialization:

1. **Environment Validation** - Checks for required API keys
2. **Directory Initialization** - Creates required directories
3. **Health Checks** - Validates system resources
4. **Application Startup** - Launches Streamlit server

### Files Created
```
Comment-Analyzer/
├── Dockerfile              # Multi-stage build configuration
├── docker-compose.yml      # Orchestration configuration
├── docker-bootstrap.sh     # Bootstrap script with contracts
└── .dockerignore          # Build exclusions
```

## 🚀 Quick Start

### 1. Basic Docker Run
```bash
# Build the image
docker build -t comment-analyzer .

# Run with environment file
docker run -d \
  --name comment-analyzer \
  -p 8501:8501 \
  -v $(pwd)/.env:/app/.env:ro \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/outputs:/app/outputs \
  comment-analyzer
```

### 2. Docker Compose (Recommended)
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📋 Bootstrap Contracts

### Environment Contract
The bootstrap script validates the following environment variables:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | - | OpenAI API key |
| `OPENAI_MODEL` | No | gpt-4 | Model to use |
| `APP_ENV` | No | production | Environment mode |
| `LOG_LEVEL` | No | INFO | Logging level |

### Directory Contract
Bootstrap ensures these directories exist:
- `/app/data/raw` - Raw input data
- `/app/data/processed` - Processed data
- `/app/outputs/exports` - Export files
- `/app/outputs/reports` - Generated reports
- `/app/client_input` - Client uploads
- `/app/logs` - Application logs

### Health Check Contract
- **Endpoint**: `http://localhost:8501/_stcore/health`
- **Interval**: 30 seconds
- **Timeout**: 10 seconds
- **Retries**: 3

## 🔧 Configuration Options

### Development Mode
```yaml
# docker-compose.override.yml
version: '3.8'
services:
  comment-analyzer:
    environment:
      - APP_ENV=development
      - DEBUG_MODE=True
      - LOG_LEVEL=DEBUG
    volumes:
      - ./src:/app/src  # Mount source for hot reload
```

### Production Mode
```bash
# Use production profile
docker-compose --profile production up -d
```

## 🔒 Security Considerations

### Non-Root User
- Container runs as `appuser` (UID 1000)
- No root privileges inside container
- Read-only mount for `.env` file

### Resource Limits
```yaml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 2G
```

### Network Isolation
- Custom bridge network
- No host network access
- Port exposure limited to 8501

## 📊 Monitoring

### View Logs
```bash
# Container logs
docker logs comment-analyzer

# Follow logs
docker logs -f comment-analyzer

# Bootstrap output
docker exec comment-analyzer cat /app/logs/bootstrap.log
```

### Check Health
```bash
# Health status
docker inspect comment-analyzer --format='{{.State.Health.Status}}'

# Manual health check
curl http://localhost:8501/_stcore/health
```

### Resource Usage
```bash
# CPU and Memory
docker stats comment-analyzer

# Disk usage
docker exec comment-analyzer df -h /app
```

## 🔄 Deployment Workflows

### Local Development
```bash
# Build and run
docker-compose up --build

# Hot reload (mount source)
docker-compose -f docker-compose.yml -f docker-compose.override.yml up
```

### CI/CD Pipeline
```bash
# Build
docker build -t comment-analyzer:$VERSION .

# Tag
docker tag comment-analyzer:$VERSION registry.example.com/comment-analyzer:$VERSION

# Push
docker push registry.example.com/comment-analyzer:$VERSION
```

### Cloud Deployment

#### AWS ECS
```bash
# Build and push to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin $ECR_URI
docker build -t comment-analyzer .
docker tag comment-analyzer:latest $ECR_URI/comment-analyzer:latest
docker push $ECR_URI/comment-analyzer:latest
```

#### Google Cloud Run
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/$PROJECT_ID/comment-analyzer
gcloud run deploy --image gcr.io/$PROJECT_ID/comment-analyzer --platform managed
```

#### Azure Container Instances
```bash
# Push to ACR
az acr build --registry $ACR_NAME --image comment-analyzer .
az container create --resource-group $RG --name comment-analyzer \
  --image $ACR_NAME.azurecr.io/comment-analyzer:latest
```

## 🐛 Troubleshooting

### Bootstrap Failures
```bash
# Check bootstrap output
docker run -it comment-analyzer /app/docker-bootstrap.sh

# Debug mode
docker run -it -e DEBUG_MODE=True comment-analyzer bash
```

### Missing API Key
```bash
# Pass via environment
docker run -e OPENAI_API_KEY="your_key" comment-analyzer

# Or mount .env file
docker run -v /path/to/.env:/app/.env:ro comment-analyzer
```

### Permission Issues
```bash
# Fix ownership
docker exec comment-analyzer chown -R appuser:appuser /app/data
```

### Port Already in Use
```bash
# Use different port
docker run -p 8502:8501 comment-analyzer
```

## 📦 Image Management

### Size Optimization
- Multi-stage build reduces image size
- Current size: ~500MB
- Base: python:3.12-slim

### Cleanup
```bash
# Remove container
docker rm -f comment-analyzer

# Remove image
docker rmi comment-analyzer

# Clean build cache
docker builder prune
```

## ✅ Validation Checklist

Before deployment, ensure:
- [ ] `.env` file created with API keys
- [ ] Docker installed (v20.10+)
- [ ] Docker Compose installed (v2.0+)
- [ ] Port 8501 available
- [ ] Minimum 2GB RAM available
- [ ] Bootstrap script executable

## 🎯 Summary

The Docker implementation provides:
- ✅ **Complete bootstrap contract** with validation
- ✅ **Multi-stage build** for optimization
- ✅ **Health checks** and monitoring
- ✅ **Security** with non-root user
- ✅ **Environment flexibility** (dev/staging/prod)
- ✅ **Volume persistence** for data
- ✅ **Resource limits** for stability

Run `docker-compose up` to start the application with full bootstrap validation!