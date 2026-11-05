import { useEffect, useState, type FormEvent } from 'react';
import { Button, Input, Typography } from '@arco-design/web-react';
import { Link, useNavigate } from 'react-router-dom';
import { createWorkspace, getWorkspace, listWorkspaces, WorkspaceApiError } from '../api/workspaces';
import type { Workspace, WorkspaceSummary } from '../api/types';
import type { Messages } from '../i18n';

const { Title, Paragraph, Text } = Typography;

export function WorkspacesPage({ copy }: { copy: Messages }) {
  const navigate = useNavigate();
  const [workspaces, setWorkspaces] = useState<WorkspaceSummary[]>([]);
  const [name, setName] = useState('');
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    listWorkspaces()
      .then((items) => {
        if (active) setWorkspaces(items);
      })
      .catch((reason: unknown) => {
        if (active) setLoadError(errorMessage(reason, copy));
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => { active = false; };
  }, [copy]);

  async function handleCreate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setCreating(true);
    setError(null);
    try {
      const workspace = await createWorkspace(name);
      navigate(`/workspaces/${encodeURIComponent(workspace.workspaceId)}`);
    } catch (reason) {
      setError(errorMessage(reason, copy));
    } finally {
      setCreating(false);
    }
  }

  return (
    <div className="page-wrap secondary-page workspaces-page">
      <div className="page-title-row">
        <div className="page-title-copy">
          <Title heading={1}>{copy.workspacesTitle}</Title>
          <Paragraph>{copy.workspacesDescription}</Paragraph>
        </div>
      </div>

      <section className="workspace-create-panel" aria-labelledby="workspace-create-heading">
        <Title heading={2} id="workspace-create-heading">{copy.createWorkspaceTitle}</Title>
        <form className="workspace-create-form" onSubmit={handleCreate}>
          <label className="workspace-name-field">
            <span>{copy.workspaceNameFieldLabel}</span>
            <Input
              value={name}
              onChange={setName}
              placeholder={copy.workspaceNamePlaceholder}
              autoComplete="off"
              aria-describedby="workspace-name-hint"
              required
            />
            <span className="workspace-name-hint" id="workspace-name-hint">{copy.workspaceNameHint}</span>
          </label>
          <Button className="primary-action" htmlType="submit" loading={creating} disabled={creating}>
            {copy.createWorkspaceAction}
          </Button>
        </form>
        {error && <p className="workspace-error" role="alert">{error}</p>}
      </section>

      <section className="workspace-list-section" aria-labelledby="workspace-list-heading">
        <div className="workspace-list-heading-row">
          <Title heading={2} id="workspace-list-heading">{copy.workspaceListTitle}</Title>
          {!loading && <Text>{copy.workspaceCount(workspaces.length)}</Text>}
        </div>
        {loading ? (
          <div className="workspace-list-state" role="status">{copy.workspaceLoading}</div>
        ) : loadError ? (
          <div className="workspace-list-state" role="alert">{loadError}</div>
        ) : workspaces.length === 0 ? (
          <div className="workspace-list-state">
            <strong>{copy.noWorkspacesTitle}</strong>
            <span>{copy.noWorkspacesDescription}</span>
          </div>
        ) : (
          <ul className="workspace-list">
            {workspaces.map((workspace) => <WorkspaceListItem key={workspace.workspaceId} workspace={workspace} copy={copy} />)}
          </ul>
        )}
      </section>
    </div>
  );
}

function WorkspaceListItem({ workspace, copy }: { workspace: WorkspaceSummary; copy: Messages }) {
  const isCorrupt = workspace.status === 'corrupt';
  const content = (
    <>
      <span className="workspace-list-copy">
        <strong>{isCorrupt ? copy.corruptWorkspaceName : workspace.name}</strong>
        <span>{isCorrupt ? copy.corruptWorkspaceDescription : copy.emptyWorkspaceStatus}</span>
      </span>
      <span className="workspace-list-date">
        {workspace.createdAt ? new Date(workspace.createdAt).toLocaleString() : copy.dateUnavailable}
      </span>
      {!isCorrupt && <span className="workspace-list-arrow" aria-hidden="true">↗</span>}
    </>
  );

  return (
    <li className={isCorrupt ? 'workspace-list-item is-corrupt' : 'workspace-list-item'}>
      {isCorrupt ? (
        <div className="workspace-list-entry" aria-label={copy.corruptWorkspaceDescription}>
          {content}
        </div>
      ) : (
        <Link className="workspace-list-entry" to={`/workspaces/${encodeURIComponent(workspace.workspaceId)}`}>
          {content}
        </Link>
      )}
    </li>
  );
}

export function WorkspaceDetailPage({ workspaceId, copy }: { workspaceId: string; copy: Messages }) {
  const [workspace, setWorkspace] = useState<Workspace | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError(null);
    getWorkspace(workspaceId)
      .then((item) => {
        if (active) setWorkspace(item);
      })
      .catch((reason: unknown) => {
        if (active) setError(errorMessage(reason, copy));
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => { active = false; };
  }, [workspaceId, copy]);

  return (
    <div className="page-wrap secondary-page workspace-detail-page">
      <Link to="/workspaces" className="workspace-back-link">← {copy.backToWorkspaces}</Link>
      {loading ? (
        <div className="workspace-list-state" role="status">{copy.workspaceLoading}</div>
      ) : error ? (
        <section className="workspace-detail-state" role="alert">
          <span className="workspace-status-kicker">{copy.workspaceUnavailableLabel}</span>
          <Title heading={1}>{error}</Title>
          <Paragraph>{copy.workspaceUnavailableDescription}</Paragraph>
        </section>
      ) : workspace ? (
        <>
          <div className="page-title-row workspace-detail-heading">
            <div className="page-title-copy">
              <span className="workspace-status-kicker">{copy.workspaceDetailKicker}</span>
              <Title heading={1}>{workspace.name}</Title>
              <Paragraph>{copy.workspaceDetailDescription}</Paragraph>
            </div>
          </div>
          <section className="workspace-detail-panel" aria-label={copy.workspaceStateTitle}>
            <div className="workspace-state-card">
              <span>{copy.workspaceDataStatus}</span>
              <strong>{copy.noImportedData}</strong>
            </div>
            <div className="workspace-state-card">
              <span>{copy.activeSnapshotLabel}</span>
              <strong>{copy.noActiveSnapshot}</strong>
            </div>
            <div className="workspace-state-card">
              <span>{copy.workspaceAccessLabel}</span>
              <strong>{copy.workspaceReadonly}</strong>
            </div>
          </section>
          <div className="workspace-detail-meta">
            <span>{copy.workspaceCreatedLabel}</span>
            <time dateTime={workspace.createdAt}>{new Date(workspace.createdAt).toLocaleString()}</time>
          </div>
        </>
      ) : null}
    </div>
  );
}

function errorMessage(reason: unknown, copy: Messages): string {
  if (!(reason instanceof WorkspaceApiError)) return copy.workspaceGenericError;
  switch (reason.code) {
    case 'workspace_name_invalid': return copy.workspaceNameInvalidError;
    case 'workspace_not_found': return copy.workspaceNotFoundError;
    case 'workspace_manifest_unavailable': return copy.workspaceManifestError;
    case 'workspace_storage_unavailable': return copy.workspaceStorageError;
    default: return copy.workspaceGenericError;
  }
}
