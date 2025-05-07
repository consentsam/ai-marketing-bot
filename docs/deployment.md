# Deployment Guide

This guide covers how to deploy the YieldFi AI Agent application.

## Docker Deployment (Local)

1. Ensure Docker is installed and running on your machine.
2. Build the Docker image:
   ```bash
   docker build -t yieldfi-ai-agent .
   ```
3. Run the Docker container:
   ```bash
   docker run -d --name yieldfi-ai-agent -p 8501:8501 --env-file .env yieldfi-ai-agent:latest
   ```
4. Open your browser at `http://localhost:8501` to verify the application.

## Docker Compose

You can also use Docker Compose for local orchestration:

```bash
docker-compose up --build
```

This will:
- Build the Docker image.
- Start the `ai-agent` service defined in `docker-compose.yml` on port 8501.

## Vercel Deployment

Detailed steps are provided in `docs/usage.md` under **Vercel Deployment**, including the required `vercel.json` configuration and Vercel dashboard setup.

## Continuous Deployment (CI/CD)

For automated builds and deployments, you can integrate with GitHub Actions:

- **On Push to `main`**:
  1. Build the Docker image.
  2. Push the image to your container registry (e.g., Docker Hub, GitHub Container Registry).
  3. Deploy to your production environment (e.g., using a deployment action or script).

Example snippet for `.github/workflows/deploy.yml`:

```yaml
name: CI/CD
on:
  push:
    branches: [ main ]
jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up QEMU
        uses: docker/setup-qemu-action@v2
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ secrets.DOCKER_USERNAME }}/yieldfi-ai-agent:latest
```

Ensure you store your Docker credentials as repository secrets in GitHub. 