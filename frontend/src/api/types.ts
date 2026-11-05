export type ValidationStatus = 'passed' | 'failed' | 'not_run' | 'unavailable';

export interface WorkbenchMeta {
  snapshotId: string;
  ontologyVersion: string;
  validation: ValidationStatus;
  tripleCount: number;
  classCount: number;
  propertyCount: number;
  dataSource: 'bundled-example-fixture';
}

export interface Workspace {
  workspaceId: string;
  name: string;
  createdAt: string;
  status: 'empty';
  activeSnapshotId: null;
}

export interface EmptyWorkspaceSummary extends Workspace {}

export interface CorruptWorkspaceSummary {
  workspaceId: string;
  name: null;
  createdAt: null;
  status: 'corrupt';
  issueCode: 'workspace_manifest_unavailable';
}

export type WorkspaceSummary = EmptyWorkspaceSummary | CorruptWorkspaceSummary;
