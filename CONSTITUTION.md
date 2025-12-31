# AI Agent Project - Coding Constitution

This document defines the principles, architecture, and technical decisions for the AI Agent ERP Configuration Validator project.

---

## Project Overview

**Goal**: Build an AI Agent that validates ERP system configurations against customer contracts, identifies discrepancies, and recommends corrective actions.

**Tech Stack**:
- Backend: Python + FastAPI + LlamaIndex
- Frontend: React + Vite
- Deployment: Docker + Kubernetes + Helm + ArgoCD
- Database: SQLite (with PVC for persistence)

**Domain**: `aiagent.gillsonhome.com`

---

## Core Principles

### 1. Simplicity Over Cleverness
- No premature abstractions or over-engineering
- If it can be done in 10 lines instead of a framework, do it in 10 lines
- Prefer explicit code over "magic"

### 2. Minimal Dependencies
- Only use well-maintained, popular packages with large communities
- Avoid packages with heavy dependency trees
- When in doubt, implement it ourselves if it's simple

### 3. Interactive & Responsive UX
- Always provide real-time feedback to users
- Never leave users wondering what's happening
- Default to helpful states (checkboxes pre-checked, smart defaults)

### 4. Safety First
- Human approval required before any write operations
- Clear, explicit action descriptions (no ambiguous changes)
- Manual retry only - no automatic retries on failures

### 5. Logging Philosophy
- Info by default (what happened)
- Verbose available (how it happened)
- No debug logs in production unless explicitly enabled
- Configure via environment variable: `LOG_LEVEL=info|verbose`

### 6. Code Style
- Self-documenting code (good names > comments)
- Comments only for "why", not "what"
- Keep functions small and focused

### 7. State Management
- Prefer simple state (React useState/useContext)
- Backend is source of truth
- Frontend reflects backend state

### 8. Error Handling
- Fail gracefully with clear error messages
- User-facing errors should suggest next steps
- Log technical details, show friendly messages

### 9. API Design
- RESTful for CRUD operations
- WebSockets for real-time updates
- Clear, consistent endpoint naming

### 10. Future-Proofing
- Build for today's requirements
- Make it easy to extend, not pre-emptively extensible
- YAGNI (You Aren't Gonna Need It) - don't build features we might need later

---

## File & Code Organization

### 11. CSS Classes Only
- Always use CSS classes for visual styling
- No inline styles
- Keep styles separate from component logic

### 12. Temporary File Convention
- All testing, scratch, or temporary files MUST be prefixed with `temp_`
- Makes cleanup easy and prevents clutter
- Add `temp_*` to `.gitignore`

### 13. Separation of Concerns
- No monolithic Python files
- Prefer many small, focused files over large code blocks
- Each file should have a single, clear responsibility
- Use descriptive, explicit file names (e.g., `contract_parser.py`, `erp_config_comparator.py`)
- If a file grows beyond ~200-300 lines, consider splitting it

---

## Deployment & Infrastructure

### 14. Container-First Architecture
- Everything runs in Docker containers
- Development environment should match production (docker-compose for local dev)
- No "works on my machine" - if it works in Docker, it works everywhere

### 15. Kubernetes Native
- Design for K8s from the start (health checks, graceful shutdown, 12-factor principles)
- Stateless where possible (easier scaling and restarts)
- Configuration via ConfigMaps/Secrets (no hardcoded values)

### 16. GitOps with ArgoCD
- Helm chart defines all K8s resources
- Environment-specific values files (dev, staging, prod)
- Automated deployment on git push

### 17. Deployment Configuration
- Single container deployment (Frontend + Backend in one container)
- SQLite + PersistentVolumeClaim for data persistence
- Kubernetes native Secrets for sensitive data
- Helm chart for all infrastructure as code
- ArgoCD for GitOps deployments

---

## Technology Choices

### Backend (Python)
- **FastAPI**: Lightweight, modern, excellent WebSocket support
- **LlamaIndex**: Agent orchestration and tool management
- **SQLite**: Simple, file-based database (sufficient for POC)
- **Pydantic**: Data validation and settings management
- **Python logging module**: Built-in, configurable logging

### Frontend (React)
- **Vite**: Fast, simple build tool
- **Vanilla React**: No Next.js complexity
- **WebSockets**: Real-time updates (Socket.io-client or native)
- **Minimal state management**: Context API if needed
- **CSS**: Tailwind CSS or plain CSS (no heavy component libraries)

### DevOps
- **Docker**: Single container for frontend + backend
- **Kubernetes**: Deployment target (homelab cluster)
- **Helm**: Infrastructure as code
- **ArgoCD**: GitOps continuous deployment
- **NGINX Ingress Controller**: Traffic routing
- **Image Registry**: Docker Hub or GitHub Container Registry (for POC)

### Development Tools
- **Type hints** in Python (for clarity and IDE support)
- **ESLint + Prettier**: Code consistency in frontend
- **Simple project structure**: No over-organization

---

## Data Flow Architecture

### Manual Trigger (User-Initiated)
```
User clicks "Analyze Contract"
    ↓
Frontend sends request to Backend API
    ↓
Backend creates Agent Task (status: "running")
    ↓
WebSocket emits real-time progress:
    - "loading_contract"
    - "querying_erp_pricing"
    - "querying_erp_payment_terms"
    - "analyzing_discrepancies"
    - "generating_recommendations"
    ↓
Agent completes → Backend saves results (status: "pending_approval")
    ↓
Frontend displays approval interface:
    - All recommendations listed
    - All checkboxes CHECKED by default
    - User unchecks unwanted actions
    - "Execute Selected" button
    ↓
User clicks execute → Backend processes only checked items
    ↓
Backend emits progress per action:
    - "executing_action_1" → "action_1_success"
    - "executing_action_2" → "action_2_failed"
    ↓
User can manually retry failed actions
    ↓
Task status updated to "completed"
```

### Event-Driven Trigger (Automated)
```
Salesforce: New contract uploaded
    ↓
Event Listener API receives webhook:
POST /api/events/contract-uploaded
{
  "source": "salesforce",
  "contract_id": "xxx",
  "event_type": "new_contract"
}
    ↓
Backend validates → Creates task → Agent runs
    ↓
[Same flow as manual trigger]
    ↓
Notification sent to user (email/in-app)
    ↓
User logs in, sees pending review in dashboard
    ↓
User approves/rejects recommended actions
```

---

## Key Components

### Backend Components
- **Task Manager**: Create, track, update task status
- **Agent Orchestrator**: LlamaIndex agent coordinating MCP calls
- **MCP Client**: Connects to various MCP servers (ERP, Salesforce, etc.)
- **Event Listener**: Webhook endpoint for external events
- **API Endpoints**: Trigger analysis, get results, submit approvals
- **WebSocket Manager**: Real-time progress updates

### Frontend Components
- **Analysis Dashboard**: Show pending/completed analyses
- **Approval Interface**: Review discrepancies + recommended actions
- **Manual Trigger UI**: Button + context selection
- **Real-time Progress Display**: Live updates via WebSocket

### Database Schema (Minimal)
- **Tasks table**: id, status, contract_id, created_at, results_json
- **Actions table**: id, task_id, description, status (pending/approved/rejected/executed)

---

## MCP Server Strategy

### Read vs Write Permissions
- **Read-only MCPs**: Query ERP configuration, load contracts
- **Write MCPs**: Update/create ERP configuration (requires approval)

### Authentication
- Credentials stored in Kubernetes Secrets
- Injected as environment variables
- MCP clients authenticate per-request

### Discovery
- Fixed configuration for POC (defined in ConfigMap)
- Can be extended to dynamic discovery later

---

## Security & Safety

### Approval Workflow
- All write operations require explicit human approval
- Default: all actions pre-checked, user unchecks unwanted items
- Partial approvals supported (approve some, reject others)

### Audit Trail
- All task executions logged (info level)
- MCP calls logged at verbose level (optional)
- Action outcomes stored in database

### Error Handling
- Failed actions do not block other actions
- Manual retry mechanism for failures
- Clear error messages to users

---

## Deployment Details

### Container Structure
```
Single Container:
├── NGINX (port 80)
│   ├── Serve React static files
│   └── Proxy /api/* to FastAPI
└── FastAPI (port 8000)
    ├── REST API endpoints
    ├── WebSocket endpoint
    └── LlamaIndex Agent
```

### Persistent Storage
- SQLite database at `/data/agent.db`
- Mounted to PersistentVolumeClaim
- Single replica deployment (SQLite limitation)

### Environment Configuration
- **ConfigMap**: Log level, MCP endpoints, feature flags
- **Secret**: API keys, credentials
- **Ingress**: `aiagent.gillsonhome.com` → NGINX Ingress Controller

---

## Project Structure

```
AiAgent/
├── backend/
│   ├── main.py
│   ├── api/
│   │   ├── routes.py
│   │   └── websocket.py
│   ├── agent/
│   │   ├── orchestrator.py
│   │   └── mcp_client.py
│   ├── models/
│   │   ├── task.py
│   │   └── action.py
│   ├── services/
│   │   ├── contract_parser.py
│   │   ├── erp_comparator.py
│   │   └── task_manager.py
│   ├── requirements.txt
│   └── config.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.jsx
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── docker/
│   ├── Dockerfile
│   └── nginx.conf
├── helm/
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── values-dev.yaml
│   └── templates/
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── ingress.yaml
│       ├── pvc.yaml
│       ├── configmap.yaml
│       └── secret.yaml
├── docker-compose.yml
├── .gitignore
├── README.md
└── CONSTITUTION.md
```

---

## MVP Scope

The Minimum Viable Product should include:

1. **Manual Trigger**: User can start an analysis via button click
2. **Contract Loading**: Agent loads a contract (via upload or Salesforce MCP)
3. **ERP Query**: Agent queries ERP configuration via MCP
4. **Comparison**: Agent identifies discrepancies
5. **Recommendations**: Agent suggests corrective actions
6. **Approval UI**: User sees recommendations with pre-checked checkboxes
7. **Execution**: Backend executes approved actions
8. **Real-time Updates**: WebSocket shows progress throughout

**Not in MVP**:
- Event-driven triggers (add later)
- Multiple ERP support (start with one)
- Advanced retry logic
- Email notifications
- Historical analysis tracking

---

## Development Workflow

1. **Local Development**: Use docker-compose to run full stack locally
2. **Build**: Docker build creates single container image
3. **Push**: Push image to Docker Hub / GitHub Container Registry
4. **Deploy**: ArgoCD watches git repo, applies Helm chart
5. **Monitor**: Check logs via `kubectl logs`, access via `aiagent.gillsonhome.com`

---

## Future Considerations (Not Now)

- Multi-container architecture (if scaling needed)
- PostgreSQL migration (if SQLite limitations hit)
- Multiple replica support
- Advanced secret management (Sealed Secrets, External Secrets Operator)
- Self-hosted image registry (Harbor)
- Prometheus + Grafana monitoring
- Automated testing CI/CD pipeline

---

**Last Updated**: 2025-12-30
**Status**: Initial Draft - POC Phase
