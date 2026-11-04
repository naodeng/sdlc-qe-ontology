export type Locale = 'zh' | 'en';

type MessageSet = {
  skipToContent: string;
  languageLabel: string;
  navLabel: string;
  navOverview: string;
  navOntology: string;
  navImport: string;
  navAnalysis: string;
  brandCaption: string;
  workspaceLabel: string;
  workspaceName: string;
  workspaceMeta: string;
  sidebarNote: string;
  localMode: string;
  bundledLabel: string;
  overviewKicker: string;
  overviewTitle: string;
  overviewDescription: string;
  importAction: string;
  assessmentKicker: string;
  assessmentTitle: string;
  unknown: string;
  notAssessed: string;
  assessmentDescription: string;
  readAssessment: string;
  metricsTitle: string;
  metricClasses: string;
  metricProperties: string;
  metricTriples: string;
  pathKicker: string;
  pathTitle: string;
  pathDescription: string;
  pathHint: string;
  sourceStatusKicker: string;
  ontologyMaterialsKicker: string;
  mappingKicker: string;
  modelPath: { name: string; detail: string }[];
  selectedConcept: string;
  dataTitle: string;
  dataSourceLabel: string;
  dataSourceValue: string;
  dataSourceNote: string;
  ontologyVersionLabel: string;
  ontologyVersionValue: string;
  validationLabel: string;
  validationNotRun: string;
  validationPassed: string;
  validationFailed: string;
  validationUnavailable: string;
  fixtureIdLabel: string;
  footerNote: string;
  ontologyTitle: string;
  ontologyDescription: string;
  candidateLabel: string;
  ontologyReviewTitle: string;
  ontologyReviewDescription: string;
  apiDocs: string;
  importTitle: string;
  importDescription: string;
  plannedLabel: string;
  mappingTitle: string;
  mappingDescription: string;
  importSteps: string[];
  noFileNote: string;
  analysisTitle: string;
  analysisDescription: string;
  assessmentStatusLabel: string;
  analysisExplanation: string;
  analysisFixtureStatements: string;
  evidenceQualification: string;
  notAvailable: string;
  unknownExplanation: string;
  loadingLabel: string;
  apiUnavailableTitle: string;
  apiUnavailableDescription: string;
  startCommand: string;
};

export type Messages = MessageSet;

export const messages: Record<Locale, MessageSet> = {
  zh: {
    skipToContent: '跳到主要内容',
    languageLabel: '界面语言',
    navLabel: '主导航',
    navOverview: '项目总览',
    navOntology: '本体模型',
    navImport: '数据导入',
    navAnalysis: '质量分析',
    brandCaption: '质量证据工作台',
    workspaceLabel: '当前工作区',
    workspaceName: '示例项目',
    workspaceMeta: '本地示例 · 只读',
    sidebarNote: '仅展示仓库自带的演示数据，不连接外部项目。',
    localMode: '本地工作区',
    bundledLabel: '示例数据',
    overviewKicker: '项目概览 / 质量追溯',
    overviewTitle: '质量证据总览',
    overviewDescription: '沿着需求、测试与证据的关系，快速看清当前数据能说明什么。',
    importAction: '导入项目数据',
    assessmentKicker: '当前质量结论',
    assessmentTitle: '评估状态',
    unknown: '未知',
    notAssessed: '尚未评估',
    assessmentDescription: '尚未接入真实项目或运行质量评估。此处只展示仓库示例，不能作为通过或失败的结论。',
    readAssessment: '查看评估说明',
    metricsTitle: '本体示例规模',
    metricClasses: '本体类',
    metricProperties: '本体属性',
    metricTriples: '示例三元组',
    pathKicker: '质量追溯',
    pathTitle: '从需求走到测试证据',
    pathDescription: '六个核心环节连接起需求、测试活动与结果来源。',
    pathHint: '选择一个环节查看说明',
    sourceStatusKicker: '来源与状态',
    ontologyMaterialsKicker: '本体资料',
    mappingKicker: '人工确认',
    modelPath: [
      { name: '需求', detail: '需要交付或解决的事项，是质量活动追溯的起点。' },
      { name: '验收标准', detail: '说明需求何时算完成，并可进一步转化为测试义务。' },
      { name: '测试义务', detail: '需要验证的质量要求，可由一个或多个测试用例覆盖。' },
      { name: '测试用例', detail: '定义在特定条件下执行的检查，并关联要覆盖的测试义务。' },
      { name: '测试执行', detail: '某次测试用例运行的记录，包含执行环境和结果。' },
      { name: '测试证据', detail: '支撑一次执行和质量判断的报告、结果或可追溯来源。' },
    ],
    selectedConcept: '环节说明',
    dataTitle: '数据来源与状态',
    dataSourceLabel: '数据来源',
    dataSourceValue: '仓库内置示例',
    dataSourceNote: '只读 · 不会上传或保存用户文件',
    ontologyVersionLabel: '本体版本',
    ontologyVersionValue: '候选模型 · 尚未发布',
    validationLabel: '验证状态',
    validationNotRun: '尚未运行',
    validationPassed: '已通过',
    validationFailed: '未通过',
    validationUnavailable: '不可用',
    fixtureIdLabel: '示例数据指纹',
    footerNote: '本地预览 · 候选本体 · 质量验证尚未运行',
    ontologyTitle: '本体模型',
    ontologyDescription: '当前模型是随仓库提供的候选版本；类、关系和约束仍需正式评审后才能成为稳定基线。',
    candidateLabel: '候选模型',
    ontologyReviewTitle: '模型材料',
    ontologyReviewDescription: '概念定义、能力问题、SHACL 约束和正反例均保存在仓库中，供后续评审与验证使用。',
    apiDocs: '查看本地 API 文档',
    importTitle: '导入项目数据',
    importDescription: '导入流程尚未实现。仓库已包含映射 Schema 与产品决策，当前页面不会模拟文件上传或验证进度。',
    plannedLabel: '计划中的 MVP 功能',
    mappingTitle: '字段含义由你确认',
    mappingDescription: '导入后先预览字段，再检查映射。只有人工明确确认后，映射才可进入数据校验。',
    importSteps: [
      '选择 CSV、JSON 或受控 RDF 数据源',
      '预览字段并配置映射模板',
      '检查映射并由人工明确确认',
      '完成数据校验后再创建项目快照',
    ],
    noFileNote: '此预览不会读取、上传或保存任何文件。',
    analysisTitle: '质量分析',
    analysisDescription: '分析结果应说明哪些测试义务有证据，以及哪些部分仍然未知。',
    assessmentStatusLabel: '评估状态',
    analysisExplanation: '当前没有针对真实项目运行评估。示例三元组数量仅用于说明模型数据规模，不构成质量结论。',
    analysisFixtureStatements: '示例三元组',
    evidenceQualification: '证据判定',
    notAvailable: '尚不可用',
    unknownExplanation: '未知是明确状态，既不代表通过，也不代表失败。',
    loadingLabel: '正在读取本地示例数据…',
    apiUnavailableTitle: '无法连接本地 API',
    apiUnavailableDescription: '请在项目目录启动服务：',
    startCommand: 'make setup && make dev',
  },
  en: {
    skipToContent: 'Skip to main content',
    languageLabel: 'Interface language',
    navLabel: 'Main navigation',
    navOverview: 'Overview',
    navOntology: 'Ontology model',
    navImport: 'Import data',
    navAnalysis: 'Quality analysis',
    brandCaption: 'QUALITY EVIDENCE WORKBENCH',
    workspaceLabel: 'CURRENT WORKSPACE',
    workspaceName: 'Example project',
    workspaceMeta: 'LOCAL EXAMPLE · READ ONLY',
    sidebarNote: 'Bundled demo data only. No external project is connected.',
    localMode: 'LOCAL WORKSPACE',
    bundledLabel: 'DEMO DATA',
    overviewKicker: 'PROJECT OVERVIEW / TRACEABILITY',
    overviewTitle: 'Quality evidence overview',
    overviewDescription: 'Follow requirements, tests, and evidence to see what the current data can tell you.',
    importAction: 'Import project data',
    assessmentKicker: 'CURRENT QUALITY CONCLUSION',
    assessmentTitle: 'Assessment status',
    unknown: 'Unknown',
    notAssessed: 'Not assessed',
    assessmentDescription: 'No real project is connected and no quality assessment has run. This bundled example is not a pass or fail result.',
    readAssessment: 'View assessment notes',
    metricsTitle: 'Bundled ontology size',
    metricClasses: 'Ontology classes',
    metricProperties: 'Ontology properties',
    metricTriples: 'Example triples',
    pathKicker: 'TRACEABILITY / QUALITY PATH',
    pathTitle: 'From requirement to test evidence',
    pathDescription: 'Six core concepts connect requirements, test activity, and evidence sources.',
    pathHint: 'Select a step to read its role',
    sourceStatusKicker: 'SOURCE / STATUS',
    ontologyMaterialsKicker: 'REPOSITORY MATERIALS',
    mappingKicker: 'HUMAN CONFIRMATION',
    modelPath: [
      { name: 'Requirement', detail: 'A need to deliver or resolve and the starting point for quality traceability.' },
      { name: 'Acceptance criterion', detail: 'Defines when a requirement is complete and can lead to test obligations.' },
      { name: 'Test obligation', detail: 'A quality expectation that one or more test cases should cover.' },
      { name: 'Test case', detail: 'A defined check run under specific conditions and linked to its obligations.' },
      { name: 'Test execution', detail: 'A record of running a test case, including its context and result.' },
      { name: 'Test evidence', detail: 'A report, result, or traceable source that supports an execution and decision.' },
    ],
    selectedConcept: 'STEP NOTES',
    dataTitle: 'Data source and status',
    dataSourceLabel: 'Data source',
    dataSourceValue: 'Bundled example fixture',
    dataSourceNote: 'Read only · no user files are uploaded or stored',
    ontologyVersionLabel: 'Ontology version',
    ontologyVersionValue: 'Candidate model · unpublished',
    validationLabel: 'Validation',
    validationNotRun: 'Not run',
    validationPassed: 'Passed',
    validationFailed: 'Failed',
    validationUnavailable: 'Unavailable',
    fixtureIdLabel: 'Example fingerprint',
    footerNote: 'Local preview · candidate ontology · validation has not run',
    ontologyTitle: 'Ontology model',
    ontologyDescription: 'This bundled model is a candidate. Its classes, relationships, and constraints still need formal review before becoming a stable baseline.',
    candidateLabel: 'CANDIDATE MODEL',
    ontologyReviewTitle: 'Model materials',
    ontologyReviewDescription: 'Concept definitions, competency questions, SHACL constraints, and positive/negative fixtures are kept in the repository for review and validation.',
    apiDocs: 'Open local API docs',
    importTitle: 'Import project data',
    importDescription: 'The import workflow is not implemented. The repository includes the mapping schema and product decisions; this page does not simulate uploads or validation progress.',
    plannedLabel: 'PLANNED FOR MVP',
    mappingTitle: 'You confirm field meaning',
    mappingDescription: 'Preview fields and review their mapping first. A mapping can enter validation only after an explicit human confirmation.',
    importSteps: [
      'Choose a CSV, JSON, or controlled RDF source',
      'Preview fields and configure a mapping template',
      'Review and explicitly confirm the mapping',
      'Validate the data before creating a project snapshot',
    ],
    noFileNote: 'This preview does not read, upload, or store any files.',
    analysisTitle: 'Quality analysis',
    analysisDescription: 'An assessment should show which test obligations have evidence and where the available data remains unknown.',
    assessmentStatusLabel: 'ASSESSMENT STATUS',
    analysisExplanation: 'No assessment has run against a real project. The example triple count describes model size and is not a quality conclusion.',
    analysisFixtureStatements: 'Example triples',
    evidenceQualification: 'Evidence qualification',
    notAvailable: 'Not available',
    unknownExplanation: 'Unknown is an explicit state. It does not mean passed or failed.',
    loadingLabel: 'Reading bundled example data…',
    apiUnavailableTitle: 'Local API unavailable',
    apiUnavailableDescription: 'Start the services from the repository root:',
    startCommand: 'make setup && make dev',
  },
};
