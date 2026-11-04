# Frontend

React + TypeScript + Vite + Arco Design React shell for the local workbench. It reads the FastAPI API through Vite's same-origin /api proxy and does not read or mutate RDF files directly.

Install dependencies from the repository root. The root npm workspace keeps the browser tests at `e2e/` while sharing the frontend's Playwright dependency.

- npm ci
- npm --prefix frontend run build
- npm --prefix frontend run e2e:install (once per machine)
- npm --prefix frontend run e2e

Development binds to 127.0.0.1:5174. See the root DESIGN.md for the interface direction and current limitations.
