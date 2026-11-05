import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { defineConfig, devices } from '@playwright/test';

const frontendDirectory = path.dirname(fileURLToPath(import.meta.url));
const repositoryRoot = path.resolve(frontendDirectory, '..');
const python = path.join(repositoryRoot, '.venv/bin/python');
const e2eDataRoot = process.env.SDLC_QE_E2E_DATA_ROOT;
if (!e2eDataRoot || process.env.SDLC_QE_DATA_DIR !== e2eDataRoot) {
  throw new Error('Run Playwright through make e2e or npm --workspace frontend run e2e to isolate local data');
}
const frontendPortValue = process.env.E2E_FRONTEND_PORT ?? '5174';
const frontendPort = Number(frontendPortValue);
if (
  !/^[1-9]\d{0,4}$/.test(frontendPortValue) ||
  frontendPort > 65535 ||
  !Number.isInteger(frontendPort)
) {
  throw new Error('E2E_FRONTEND_PORT must be an integer from 1 to 65535');
}
const frontendOrigin = `http://127.0.0.1:${frontendPort}`;

export default defineConfig({
  testDir: path.join(repositoryRoot, 'e2e/tests'),
  fullyParallel: true,
  reporter: 'list',
  use: {
    baseURL: frontendOrigin,
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
      command: `npm run dev -- --host 127.0.0.1 --port ${frontendPort} --strictPort`,
      cwd: frontendDirectory,
      url: frontendOrigin,
      reuseExistingServer: false,
      timeout: 30_000,
    },
  ],
});
