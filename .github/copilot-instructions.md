# GitHub Copilot Instructions for AiAgent Project

**IMPORTANT**: This project has a detailed coding constitution in `CONSTITUTION.md`. All code suggestions must align with these principles.

## Core Principles (Quick Reference)

1. **Simplicity First**: No over-engineering, prefer explicit code
2. **Minimal Dependencies**: Only mainstream, well-supported packages
3. **No Monolithic Files**: Keep Python files under 200-300 lines, use separation of concerns
4. **CSS Classes Only**: Never suggest inline styles in React
5. **Temp File Prefix**: All temporary files must start with `temp_`
6. **Type Hints Required**: All Python functions need type hints
7. **No Premature Abstractions**: Build for today's requirements, not hypothetical future

## Project Tech Stack
- Backend: FastAPI + LlamaIndex + SQLite
- Frontend: React + Vite (vanilla, no Next.js)
- Deployment: Docker + Kubernetes + Helm

## Code Style
- Python: Type hints, max 100 chars/line, use black formatter
- JavaScript/React: ESLint, Prettier, single quotes
- CSS: Always use classes (separate .css files)

## File Organization
- Backend: Separate files for routes, services, models, agent logic
- Frontend: Components in `components/`, services in `services/`
- Use descriptive file names (e.g., `contract_parser.py` not `utils.py`)

Read `CONSTITUTION.md` for complete guidelines.
