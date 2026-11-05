# Plan: 20261105-pr-review-second-pass

Status: Implemented after the second review of PR #1 (2026-11-05).
Linked Requirement: REQ-WORKSPACE-001.

## Goal

Fix staging cleanup and workspace-directory read races found after the first two PR review fixes, and make the remaining evidence boundaries explicit.

## Implementation

- Publish the fully written staging directory with an atomic no-replace rename, so a UUID collision cannot replace an existing directory and successful creation leaves no staging directory.
- On POSIX systems with `O_DIRECTORY`, `O_NOFOLLOW`, and directory-descriptor operations, anchor the data root, `workspaces/`, UUID directories, manifest reads, publication, and cleanup to opened directory handles. The no-replace rename uses Darwin `renameatx_np(RENAME_EXCL)` or Linux `renameat2(RENAME_NOREPLACE)`. Root or workspace path swaps fail closed without reading or writing through an outside symlink. If safe handles or filesystem no-replace rename are unavailable, fail closed.
- On Windows, hold no-follow data/workspaces root handles and open child workspace directories with `FILE_FLAG_OPEN_REPARSE_POINT` and no delete sharing during file access. Reads open the manifest itself as a no-follow Win32 handle; creation locks the staging directory while writing, retains its file identity across the rename, and reopens/validates the final directory before success. Windows junction race tests run in the `windows-storage` CI job; this path was not runtime-verified in the macOS session.
- Correct the original plan's initial RED entries: missing implementation modules/routes prevented behavior assertions, so these are attempts rather than valid RED evidence. The initial UI E2E attempt also ended before assertions. A separate replay of the new E2E case against an isolated `origin/main` archive records the expected baseline failure; this is a review-time baseline replay, not a claim that the original implementation followed RED-first sequencing.
- The current UI is light-only: no dark theme or `prefers-color-scheme` behavior exists. Dark-theme review is not applicable to this phase and is recorded as not implemented/not tested.

## Compatibility and boundaries

- No API, manifest schema, ontology URI, mapping, snapshot, or workspace product behavior changes.
- Workspace paths remain server-side; invalid directory/manifest races become corrupt/unavailable states rather than returning outside manifest data.
- E2E continues to use isolated temporary storage and an ephemeral loopback port.

## TDD and verification

- The pre-fix store tests failed: successful creation left `.staging-<uuid>`, a workspace-directory-to-symlink swap returned the outside manifest as a valid workspace, replacing `workspaces/` during list/create could read or write through the outside symlink, an ordinary destination-directory replacement could receive a manifest after the directory was claimed, and a regular manifest swapped to FIFO could block a read.
- After the fixes, those regression assertions pass. Repository and Playwright gates are recorded in [`pr-review-second-pass-20261105.md`](../qa/pr-review-second-pass-20261105.md).

## Rollback

Revert the PR follow-up commit. It changes no existing workspace contents and introduces no migration.
