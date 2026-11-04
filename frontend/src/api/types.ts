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
