# Sprint 0 and MVP TDD acceptance

| ID | Scenario | Expected result | Level |
|---|---|---|---|
| UI-001 | first run, OS dark | system mode renders dark before first paint | Playwright |
| UI-002 | manual light, OS switches | stays light | Playwright |
| UI-003 | manual dark, reload | dark persists | Playwright |
| UI-004 | malformed localStorage | fallback system, no crash | Unit/E2E |
| UI-005 | locale en/zh-CN/system | navigation and reason codes localized; English fallback | Unit/E2E |
| UI-006 | runtime version unavailable | show Unavailable, never fake version | API/E2E |
| UI-007 | snapshot switches during fetch | old responses ignored; all panels same snapshot | Integration/E2E |
| UI-008 | SHACL unavailable | browse works; Qualified assurance is blocked | API/E2E |
| UI-009 | incomplete obligation set | Unknown, not Qualified | Policy/E2E |
| UI-010 | known failing obligation | Unqualified per policy precedence | Policy/E2E |
| UI-011 | mixed valid and invalid evidence | backend policy determines outcome; UI cannot override | Integration |
| UI-012 | graph exceeds cap | truncation announced and list fallback available | Component/E2E |
| UI-013 | keyboard-only navigation | menus, table, drawer, graph fallback usable | Accessibility |
| UI-014 | theme light/dark | WCAG 2.2 AA checks for text/focus/status | Accessibility |
| UI-015 | read-only API | no arbitrary SPARQL, path reads or writes | Security |
| UI-016 | Arco dependency | clean install, production build, test and license audit | CI Spike |

## Gate evidence
Record exact dependency versions, lockfile, commands, CI job URL, screenshots at representative viewport widths, accessibility findings and license review. **Do not mark a gate passed without actual evidence.**
