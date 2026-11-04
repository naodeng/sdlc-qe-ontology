# ADR-UI-017: Adopt Arco Design Pro 2.0 reference

Status: **Accepted for design direction; implementation gated by Spike**.

- Replace Animal Island UI as visual reference and component dependency candidate with **Arco Design Pro 2.0** visual/interaction patterns and **@arco-design/web-react** as candidate React component library.
- Figma reference: https://www.figma.com/design/pwY2A1vuN3AxZFB4Vtdy0e/Arco-Design-Pro-2.0-%E8%AE%BE%E8%AE%A1%E8%B5%84%E6%BA%90--Community-?node-id=342-94144
- **Verified node 342:94144 is a banner labeled “通知、我的👉”, not a full dashboard screen**. Exact full-screen fidelity is pending access to representative dashboard/table/detail/settings nodes.
- Preserve React + TypeScript + Vite, FastAPI, RDFLib/SPARQL/SHACL, local-first read-only semantics, immutable snapshot, tri-state quality policy, assurance status, English/Chinese i18n, light/dark/system theme and version metadata.
- Do not modify RDF/OWL ontology, SHACL shapes, SPARQL CQ or policy rules to fit UI components.
- Historical Animal Island documents remain as archived context only. Their library-specific guidance is **superseded**; not an implementation requirement.
- No package has been installed, no browser screenshot match or runtime build has been verified. Check library license, dependency compatibility, design asset rights and Figma community file reuse terms before shipping.

## Scope
P0: App shell, navigation, Overview, Ontology Explorer, Graph, Evidence Explorer, Quality Decision, Validation Status, Settings. No ontology editing, arbitrary SPARQL input, release approval, or external ingestion in MVP.
