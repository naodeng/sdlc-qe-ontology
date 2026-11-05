# Plan: 20261105-pr-review-fixes

Status: Implemented after review of PR #1 comments (2026-11-05).
Linked Requirement: REQ-WORKSPACE-001.

## Goal

Address the two P2 findings on PR #1 without changing the workspace API or phase 1 scope:

1. Prevent manifest publication from following a UUID directory replaced with a symlink.
2. Prevent direct Playwright package-script runs from writing into persistent user workspace storage.

## Implementation

- On POSIX systems with directory-descriptor support, open the claimed destination with `O_DIRECTORY | O_NOFOLLOW`, verify the opened and named directory have the same device/inode, and publish the already-fsynced manifest through that descriptor with a non-overwriting hard link. Verify identity again after publication and remove the linked manifest through the descriptor if the path was replaced.
- On Windows, atomically rename the complete staging directory into the UUID destination. `os.rename` raises `FileExistsError` when the destination already exists on Windows, so a replaced destination is not followed and collisions retry.
- Route `npm --workspace frontend run e2e` through `scripts/e2e-run.sh`. The runner creates and cleans its own temporary data root, sets a matching isolation marker, and forwards Playwright arguments. The Playwright config rejects launches without that marker.

## Compatibility and boundaries

- No public API, manifest schema, ontology URI, mapping, or snapshot contract changes.
- Workspace paths remain server-side. A completed workspace is still visible only after its manifest is fully written.
- E2E remains loopback-only, uses a strict ephemeral frontend port, and removes only its own temporary data root.

## Verification

- Added a regression test that injects a destination-directory-to-symlink replacement at publication time; the previous implementation did not raise and overwrote the outside manifest.
- Re-ran the workspace-store tests, repository verification script, and Playwright through the direct npm workspace command.
- Windows behavior is covered by the collision test shape but was not executed in the macOS environment.

## Rollback

Revert the PR follow-up commit. It changes no existing workspace data and adds no migration.
