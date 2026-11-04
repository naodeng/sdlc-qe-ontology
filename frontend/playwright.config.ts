import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { defineConfig, devices } from '@playwright/test';

const frontendDirectory = path.dirname(fileURLToPath(import.meta.url));
const repositoryRoot = path.resolve(frontendDirectory, '..');
const python = path.join(repositoryRoot, '.venv/bin/python');

export default defineConfig({
  testDir: path.join(repositoryRoot, 'e2e/tests'),
  fullyParallel: true,
  reporter: 'list',
  use: {
    baseURL: 'http://127.0.0.1:5174',
    trace: 'retain-on-failure',
    ...devices['Desktop Chrome'],
  },
  webServer: [
    {
      command: `${python} -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000`,
      cwd: repositoryRoot,
      url: 'http://127.0.0.1:8000/api/v1/health',
      reuseExistingServer: false,
      timeout: 30_000,
    },
    {
      command: 'npm run dev -- --host 127.0.0.1',
      cwd: frontendDirectory,
      url: 'http://127.0.0.1:5174',
      reuseExistingServer: false,
      timeout: 30_000,
    },
  ],
});
