import type { WorkbenchMeta } from './types';

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, '') ?? '';

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`, {
    headers: { Accept: 'application/json' },
  });
  if (!response.ok) {
    throw new Error(`Workbench API returned ${response.status}`);
  }
  return (await response.json()) as T;
}

export function getWorkbenchMeta(): Promise<WorkbenchMeta> {
  return getJson<WorkbenchMeta>('/api/v1/meta');
}
