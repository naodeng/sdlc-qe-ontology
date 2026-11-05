import type { Workspace, WorkspaceSummary } from './types';

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, '') ?? '';

interface WorkspaceListResponse {
  workspaces: WorkspaceSummary[];
}

interface WorkspaceErrorResponse {
  detail?: { code?: string };
}

export class WorkspaceApiError extends Error {
  constructor(readonly code: string) {
    super(code);
    this.name = 'WorkspaceApiError';
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`, {
    ...init,
    headers: {
      Accept: 'application/json',
      ...(init?.headers ?? {}),
    },
  });

  if (!response.ok) {
    let code = 'workspace_request_failed';
    try {
      const payload = (await response.json()) as WorkspaceErrorResponse;
      code = payload.detail?.code ?? code;
    } catch {
      // Keep the UI error stable when the local service returns a non-JSON response.
    }
    throw new WorkspaceApiError(code);
  }

  return (await response.json()) as T;
}

export async function listWorkspaces(): Promise<WorkspaceSummary[]> {
  const response = await request<WorkspaceListResponse>('/api/v1/workspaces');
  return response.workspaces;
}

export function createWorkspace(name: string): Promise<Workspace> {
  return request<Workspace>('/api/v1/workspaces', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name }),
  });
}

export function getWorkspace(workspaceId: string): Promise<Workspace> {
  return request<Workspace>(`/api/v1/workspaces/${encodeURIComponent(workspaceId)}`);
}
