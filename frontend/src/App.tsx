import { useEffect, useState, type ReactNode } from 'react';
import { Button, Layout, Menu, Tag, Typography } from '@arco-design/web-react';
import { BrowserRouter, Link, NavLink, Route, Routes, useLocation, useNavigate, useParams } from 'react-router-dom';
import { getWorkbenchMeta } from './api/client';
import type { WorkbenchMeta } from './api/types';
import { messages, type Locale, type Messages } from './i18n';
import { WorkspaceDetailPage, WorkspacesPage } from './pages/WorkspacesPage';

const { Header, Sider, Content } = Layout;
const { Title, Text, Paragraph } = Typography;

function NavMark({ kind }: { kind: 'overview' | 'ontology' | 'import' | 'analysis' | 'workspaces' }) {
  const common = {
    width: 19,
    height: 19,
    viewBox: '0 0 20 20',
    fill: 'none',
    stroke: 'currentColor',
    strokeWidth: 1.5,
    strokeLinecap: 'round' as const,
    strokeLinejoin: 'round' as const,
    'aria-hidden': true as const,
  };

  if (kind === 'overview') {
    return <svg {...common}><rect x="2.5" y="2.5" width="6" height="6" rx="1.5" /><rect x="11.5" y="2.5" width="6" height="6" rx="1.5" /><rect x="2.5" y="11.5" width="6" height="6" rx="1.5" /><rect x="11.5" y="11.5" width="6" height="6" rx="1.5" /></svg>;
  }
  if (kind === 'ontology') {
    return <svg {...common}><circle cx="4" cy="5" r="2" /><circle cx="15.5" cy="4" r="2" /><circle cx="10" cy="15.5" r="2" /><path d="m5.8 5 7.7-.7M5 6.8l4 6.8m5.3-7.6-3.5 7.8" /></svg>;
  }
  if (kind === 'import') {
    return <svg {...common}><path d="M10 13V3.5m0 0L6.5 7M10 3.5 13.5 7M4 12.5v3.8h12v-3.8" /></svg>;
  }
  if (kind === 'workspaces') {
    return <svg {...common}><rect x="3" y="3" width="14" height="14" rx="2" /><path d="M7 7h6M7 10h6M7 13h3" /></svg>;
  }
  return <svg {...common}><path d="M3 16.5h14M5 13.5V9m5 4.5V5m5 8.5V7" /><circle cx="5" cy="7" r="1" /><circle cx="10" cy="3" r="1" /><circle cx="15" cy="5" r="1" /></svg>;
}

function LanguageSwitch({ locale, onChange, label }: { locale: Locale; onChange: (locale: Locale) => void; label: string }) {
  return (
    <div className="language-switch" role="group" aria-label={label}>
      <button type="button" aria-pressed={locale === 'zh'} onClick={() => onChange('zh')}>中文</button>
      <button type="button" aria-pressed={locale === 'en'} onClick={() => onChange('en')}>EN</button>
    </div>
  );
}

function AppFrame() {
  const location = useLocation();
  const navigate = useNavigate();
  const [locale, setLocale] = useState<Locale>('zh');
  const [meta, setMeta] = useState<WorkbenchMeta | null>(null);
  const [apiError, setApiError] = useState<string | null>(null);
  const copy = messages[locale];
  const activeKey = location.pathname.startsWith('/workspaces') ? '/workspaces' : location.pathname === '/' ? '/' : location.pathname;

  useEffect(() => {
    document.documentElement.lang = locale === 'zh' ? 'zh-CN' : 'en';
    document.title = locale === 'zh' ? 'SDLC-QE 质量证据工作台' : 'SDLC-QE Workbench';
  }, [locale]);

  useEffect(() => {
    getWorkbenchMeta()
      .then(setMeta)
      .catch((error: unknown) => {
        setApiError(error instanceof Error ? error.message : 'Could not reach the local API.');
      });
  }, []);

  return (
    <>
    <a className="skip-link" href="#main-content">{copy.skipToContent}</a>
    <Layout className="workbench-frame">
      <Sider className="workbench-sidebar" width={228} breakpoint="lg" collapsedWidth={0}>
        <Link to="/" className="brand-lockup" aria-label="SDLC-QE 质量证据工作台首页">
          <span className="brand-symbol" aria-hidden="true">
            <svg viewBox="0 0 32 32" fill="none">
              <path d="M8 10.5 23 8M9 12l6.5 10m6.5-12-6.2 12" />
              <circle cx="7" cy="10.5" r="2.3" />
              <circle cx="24.5" cy="7.8" r="2.3" />
              <circle cx="16" cy="23.5" r="2.3" />
            </svg>
          </span>
          <span className="brand-copy">
            <strong className="brand-name">SDLC·QE</strong>
            <span className="brand-caption">{copy.brandCaption}</span>
          </span>
        </Link>

        <div className="workspace-summary">
          <Text className="workspace-heading">{copy.workspaceLabel}</Text>
          <Text className="workspace-name">{copy.workspaceName}</Text>
          <Text className="workspace-meta"><span className="live-dot" />{copy.workspaceMeta}</Text>
        </div>

        <Menu className="workbench-menu" selectedKeys={[activeKey]} onClickMenuItem={(key) => navigate(key)} aria-label={copy.navLabel}>
          <Menu.Item key="/"><NavMark kind="overview" /><span>{copy.navOverview}</span></Menu.Item>
          <Menu.Item key="/ontology"><NavMark kind="ontology" /><span>{copy.navOntology}</span></Menu.Item>
          <Menu.Item key="/import"><NavMark kind="import" /><span>{copy.navImport}</span></Menu.Item>
          <Menu.Item key="/analysis"><NavMark kind="analysis" /><span>{copy.navAnalysis}</span></Menu.Item>
          <Menu.Item key="/workspaces"><NavMark kind="workspaces" /><span>{copy.navWorkspaces}</span></Menu.Item>
        </Menu>

        <div className="sidebar-note"><Text>{copy.sidebarNote}</Text></div>
      </Sider>

      <Layout className="workbench-main-layout">
        <Header className="workbench-header">
          <div className="header-context">
            <span className="header-product">SDLC·QE</span>
            <span className="header-separator" aria-hidden="true">/</span>
            <span>{pageTitle(location.pathname, copy)}</span>
          </div>
          <div className="header-right">
            <Tag className="local-pill"><span className="live-dot" />{copy.localMode}</Tag>
            <span className="header-snapshot">{copy.bundledLabel}</span>
            <LanguageSwitch locale={locale} onChange={setLocale} label={copy.languageLabel} />
          </div>
          <nav className="mobile-nav" aria-label={copy.navLabel}>
            <MobileNavLink to="/" label={copy.navOverview} />
            <MobileNavLink to="/ontology" label={copy.navOntology} />
            <MobileNavLink to="/import" label={copy.navImport} />
            <MobileNavLink to="/analysis" label={copy.navAnalysis} />
            <MobileNavLink to="/workspaces" label={copy.navWorkspaces} />
          </nav>
        </Header>

        <Content className="workbench-content" id="main-content" role="main" tabIndex={-1}>
          {apiError ? (
            <section className="service-error" role="alert">
              <span className="error-label">LOCAL SERVICE</span>
              <Title heading={1}>{copy.apiUnavailableTitle}</Title>
              <Paragraph>{copy.apiUnavailableDescription}</Paragraph>
              <code>{copy.startCommand}</code>
              <Text className="service-error-detail">{apiError}</Text>
            </section>
          ) : !meta ? (
            <div className="loading-state" role="status" aria-label={copy.loadingLabel}>
              <span className="loading-orbit" aria-hidden="true"><i /><i /><i /></span>
              <span>{copy.loadingLabel}</span>
            </div>
          ) : (
            <Routes>
              <Route path="/" element={<OverviewPage meta={meta} copy={copy} onNavigate={navigate} />} />
              <Route path="/ontology" element={<OntologyPage meta={meta} copy={copy} />} />
              <Route path="/import" element={<ImportPage copy={copy} />} />
              <Route path="/analysis" element={<AnalysisPage meta={meta} copy={copy} />} />
              <Route path="/workspaces" element={<WorkspacesPage copy={copy} />} />
              <Route path="/workspaces/:workspaceId" element={<WorkspaceDetailRoute copy={copy} />} />
              <Route path="*" element={<OverviewPage meta={meta} copy={copy} onNavigate={navigate} />} />
            </Routes>
          )}
        </Content>
      </Layout>
    </Layout>
    </>
  );
}

function WorkspaceDetailRoute({ copy }: { copy: Messages }) {
  const { workspaceId } = useParams();
  return workspaceId ? <WorkspaceDetailPage workspaceId={workspaceId} copy={copy} /> : <WorkspacesPage copy={copy} />;
}

function MobileNavLink({ to, label }: { to: string; label: string }) {
  return <NavLink to={to} end={to === '/'} className={({ isActive }) => isActive ? 'mobile-nav-link is-active' : 'mobile-nav-link'}>{label}</NavLink>;
}

function PageHeading({ title, description, action }: { title: string; description: string; action?: ReactNode }) {
  return (
    <div className="page-title-row">
      <div className="page-title-copy">
        <Title heading={1}>{title}</Title>
        <Paragraph>{description}</Paragraph>
      </div>
      {action}
    </div>
  );
}

function Metric({ label, value }: { label: string; value: number }) {
  return (
    <div className="metric-item">
      <span className="metric-label">{label}</span>
      <strong>{value.toLocaleString()}</strong>
    </div>
  );
}

function ModelPath({ copy }: { copy: Messages }) {
  const [selected, setSelected] = useState(0);
  const active = copy.modelPath[selected];

  return (
    <section className="trace-section" aria-labelledby="trace-heading">
      <div className="section-heading">
        <div>
          <Title heading={2} id="trace-heading">{copy.pathTitle}</Title>
          <Paragraph>{copy.pathDescription}</Paragraph>
        </div>
        <span className="section-hint">{copy.pathHint}</span>
      </div>
      <ol className="trace-flow" aria-label={copy.pathTitle}>
            {copy.modelPath.map((step, index) => (
          <li className="trace-flow-item" key={step.name}>
            <button
              className={'trace-node' + (selected === index ? ' is-active' : '')}
              type="button"
              aria-pressed={selected === index}
              onClick={() => setSelected(index)}
            >
              <span className="trace-node-name">{step.name}</span>
            </button>
            {index < copy.modelPath.length - 1 && <span className={'trace-connector' + (index < selected ? ' is-passed' : '')} aria-hidden="true" />}
          </li>
        ))}
      </ol>
      <div className="trace-detail" aria-live="polite">
        <span className="trace-detail-label">{copy.selectedConcept}</span>
        <p className="trace-detail-copy" key={active.name}><strong>{active.name}</strong><span>{active.detail}</span></p>
      </div>
    </section>
  );
}

function OverviewPage({ meta, copy, onNavigate }: { meta: WorkbenchMeta; copy: Messages; onNavigate: (path: string) => void }) {
  return (
    <div className="page-wrap overview-page">
      <PageHeading
        title={copy.overviewTitle}
        description={copy.overviewDescription}
        action={<Button className="primary-action" onClick={() => onNavigate('/import')}><span>{copy.importAction}</span><span aria-hidden="true">↗</span></Button>}
      />

      <div className="overview-summary">
        <section className="assessment-state" aria-labelledby="assessment-heading">
          <div className="assessment-copy">
            <span className="assessment-state-label">{copy.assessmentKicker}</span>
            <div className="assessment-title-line">
              <Title heading={2} id="assessment-heading">{copy.unknown}</Title>
              <Tag className="status-tag">{copy.notAssessed}</Tag>
            </div>
            <Paragraph>{copy.assessmentDescription}</Paragraph>
            <Button type="text" className="inline-action" onClick={() => onNavigate('/analysis')}>{copy.readAssessment}<span aria-hidden="true">↗</span></Button>
          </div>
        </section>

        <section className="metrics-panel" aria-label={copy.metricsTitle}>
          <div className="metrics-panel-heading">
            <span>{copy.metricsTitle}</span>
            <Tag className="demo-tag">{copy.bundledLabel}</Tag>
          </div>
          <div className="metric-grid">
            <Metric label={copy.metricClasses} value={meta.classCount} />
            <Metric label={copy.metricProperties} value={meta.propertyCount} />
            <Metric label={copy.metricTriples} value={meta.tripleCount} />
          </div>
        </section>
      </div>

      <ModelPath copy={copy} />

      <section className="metadata-section" aria-labelledby="metadata-heading">
        <div className="metadata-heading-row">
          <div>
            <Title heading={2} id="metadata-heading">{copy.dataTitle}</Title>
          </div>
          <span className="source-caption"><span className="live-dot" />{copy.dataSourceNote}</span>
        </div>
        <div className="metadata-grid">
          <div className="metadata-primary">
            <span className="metadata-label">{copy.dataSourceLabel}</span>
            <strong>{copy.dataSourceValue}</strong>
          </div>
          <div className="metadata-cell">
            <span className="metadata-label">{copy.ontologyVersionLabel}</span>
            <strong>{copy.ontologyVersionValue}</strong>
          </div>
          <div className="metadata-cell">
            <span className="metadata-label">{copy.validationLabel}</span>
            <strong className="validation-value">{displayValidation(meta.validation, copy)}</strong>
          </div>
        </div>
        <div className="fixture-row">
          <span>{copy.fixtureIdLabel}</span>
          <code title={meta.snapshotId}>{meta.snapshotId}</code>
        </div>
      </section>

      <div className="page-disclaimer">{copy.footerNote}</div>
    </div>
  );
}

function OntologyPage({ meta, copy }: { meta: WorkbenchMeta; copy: Messages }) {
  return (
    <div className="page-wrap secondary-page">
      <PageHeading title={copy.ontologyTitle} description={copy.ontologyDescription} />
      <div className="model-stats">
        <Metric label={copy.metricClasses} value={meta.classCount} />
        <Metric label={copy.metricProperties} value={meta.propertyCount} />
        <Metric label={copy.metricTriples} value={meta.tripleCount} />
        <Tag className="candidate-tag">{copy.candidateLabel}</Tag>
      </div>
      <ModelPath copy={copy} />
      <section className="reference-note">
        <div>
          <Title heading={2}>{copy.ontologyReviewTitle}</Title>
          <Paragraph>{copy.ontologyReviewDescription}</Paragraph>
        </div>
        <Button type="text" className="inline-action" href="/api/docs" target="_blank" rel="noreferrer">{copy.apiDocs}<span aria-hidden="true">↗</span></Button>
      </section>
    </div>
  );
}

function ImportPage({ copy }: { copy: Messages }) {
  return (
    <div className="page-wrap secondary-page">
      <PageHeading title={copy.importTitle} description={copy.importDescription} />
      <section className="import-note">
        <div className="import-note-heading">
          <div>
            <Title heading={2}>{copy.mappingTitle}</Title>
          </div>
          <Tag className="candidate-tag">{copy.plannedLabel}</Tag>
        </div>
        <Paragraph>{copy.mappingDescription}</Paragraph>
        <div className="import-plan-layout">
          <ol className="planned-steps">
            {copy.importSteps.map((step) => <li key={step}>{step}</li>)}
          </ol>
          <aside className="no-file-note">{copy.noFileNote}</aside>
        </div>
      </section>
    </div>
  );
}

function AnalysisPage({ meta, copy }: { meta: WorkbenchMeta; copy: Messages }) {
  return (
    <div className="page-wrap secondary-page">
      <PageHeading title={copy.analysisTitle} description={copy.analysisDescription} />
      <section className="assessment-report">
        <div className="report-main">
          <div className="report-summary">
            <div className="report-topline">
              <span className="report-status-label">{copy.assessmentStatusLabel}</span>
              <Tag className="status-tag">{copy.notAssessed}</Tag>
            </div>
            <div className="assessment-report-title">
              <div><Title heading={2}>{copy.unknown}</Title><Text className="report-caption">{copy.analysisExplanation}</Text></div>
            </div>
          </div>
          <dl className="report-facts">
            <div><dt>{copy.analysisFixtureStatements}</dt><dd>{meta.tripleCount.toLocaleString()}</dd></div>
            <div><dt>{copy.validationLabel}</dt><dd>{displayValidation(meta.validation, copy)}</dd></div>
            <div><dt>{copy.evidenceQualification}</dt><dd>{copy.notAvailable}</dd></div>
          </dl>
        </div>
        <p className="unknown-note">{copy.unknownExplanation}</p>
      </section>
    </div>
  );
}

function displayValidation(status: WorkbenchMeta['validation'], copy: Messages) {
  const labels: Record<WorkbenchMeta['validation'], string> = {
    passed: copy.validationPassed,
    failed: copy.validationFailed,
    not_run: copy.validationNotRun,
    unavailable: copy.validationUnavailable,
  };
  return labels[status];
}

function pageTitle(path: string, copy: Messages) {
  const pages: Record<string, string> = {
    '/': copy.navOverview,
    '/ontology': copy.navOntology,
    '/import': copy.navImport,
    '/analysis': copy.navAnalysis,
  };
  if (path.startsWith('/workspaces')) return copy.navWorkspaces;
  return pages[path] ?? copy.navOverview;
}

function App() {
  return <BrowserRouter><AppFrame /></BrowserRouter>;
}

export default App;
