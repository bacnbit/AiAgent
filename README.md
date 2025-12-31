# AI Agent - ERP Configuration Validator

An AI-powered agent that validates ERP system configurations against customer contracts, identifies discrepancies, and recommends corrective actions.

## Overview

This application uses LlamaIndex and MCP (Model Context Protocol) servers to:
- Load customer contracts from various sources (Salesforce, file uploads)
- Query ERP system configurations
- Compare contract terms against ERP settings
- Identify misconfigurations (pricing, payment terms, POD, Incoterms, etc.)
- Recommend and execute corrective actions (with human approval)

## Architecture

- **Backend**: Python + FastAPI + LlamaIndex
- **Frontend**: React + Vite
- **Database**: SQLite (with Persistent Volume in K8s)
- **Deployment**: Docker + Kubernetes + Helm + ArgoCD
- **Domain**: `aiagent.gillsonhome.com`

## Project Structure

```
AiAgent/
├── backend/          # Python FastAPI application
├── frontend/         # React application
├── docker/           # Dockerfile and nginx config
├── helm/             # Kubernetes Helm chart
├── docker-compose.yml
├── CONSTITUTION.md   # Project principles and architecture decisions
└── README.md
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Node.js 18+
- (For deployment) Kubernetes cluster with ArgoCD

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd AiAgent
   ```

2. **Start with Docker Compose**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Development without Docker

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Deployment

### Build and Push Docker Image

```bash
# Build the image
docker build -f docker/Dockerfile -t <your-registry>/aiagent:latest .

# Push to registry
docker push <your-registry>/aiagent:latest
```

### Deploy to Kubernetes with Helm

```bash
# Install or upgrade
helm upgrade --install aiagent ./helm \
  --namespace aiagent \
  --create-namespace \
  -f helm/values.yaml

# Check deployment
kubectl get pods -n aiagent
kubectl logs -f deployment/aiagent -n aiagent
```

### ArgoCD Deployment

ArgoCD will automatically sync from the git repository. Ensure your ArgoCD application points to this repo's `helm/` directory.

## Configuration

### Environment Variables

Configure via Kubernetes ConfigMap and Secrets:

**ConfigMap** (`LOG_LEVEL`, `MCP_ENDPOINTS`, etc.)
**Secrets** (`ERP_API_KEY`, `SALESFORCE_API_KEY`, etc.)

See `helm/templates/configmap.yaml` and `helm/templates/secret.yaml` for details.

## Key Features

- **Real-time Progress**: WebSocket updates during analysis
- **Human-in-the-Loop**: All configuration changes require approval
- **Partial Approvals**: Approve/reject individual recommendations
- **Event-Driven**: Can be triggered by external events (e.g., new contract in Salesforce)
- **MCP Integration**: Extensible via Model Context Protocol servers

## Development Principles

See [CONSTITUTION.md](./CONSTITUTION.md) for detailed coding principles and architectural decisions.

Key highlights:
- Simplicity over cleverness
- Minimal dependencies
- Separation of concerns
- Container-first development
- GitOps with ArgoCD

## Contributing

1. Follow the principles in `CONSTITUTION.md`
2. Prefix temporary/test files with `temp_`
3. Use CSS classes only (no inline styles)
4. Keep Python files focused and small (< 300 lines)
5. Real-time user feedback is a must

## License

[TBD]

## Support

For issues or questions, please open a GitHub issue.
