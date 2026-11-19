---
id: T013
map: docs/wayfinder/W001-public-chef-council/MAP.md
type: build
status: resolved
blocked_by: [T009, T011]
claimed_by: spec-pipeline
claimed_at: 2026-11-19T05:27:42Z
cross_examined: none
issue: https://github.com/thecharlessamuel/chef-council/issues/14
spec: docs/specs/archive/S007-chat-path-and-adapters.md
---

## Question
Give chat apps with no file access the same system, and give notes-app users a safe mirror:

- `chat/project-instructions.md`: the canonical, vendor-neutral paste-in, under 8,000 characters, that every setup note follows and never diverges from;
- `scripts/build-chat-bundle.sh`, which generates `chat/bundle.md` from `kitchen/`, the skills, and the templates, with CI failing when the bundle is stale;
- `chat/README.md`: setup for Claude Projects, ChatGPT Projects, Gemini Gems, and Muse, plus the editor check in a new chat;
- `adapters/README.md`, the sync contract: search before creating, store the external ID in the sync map, read the live version before updating, never create a duplicate as a retry, report each destination separately, and read back before claiming success;
- `adapters/sync-map.md`, an empty template, and `adapters/mem.md`, one worked example with no IDs.

Done when the instructions file is under the limit, the bundle regenerates byte for byte in CI, and no adapter file holds an ID, URL, or collection name from a real account.

## Evidence and constraints
- Decisions T005 and T006.
- Design report §3 items 11 and 13, §5.1 (one harness-agnostic instructions file), §6 (the chat-only path: "when asked to save, return the complete file and its path; never claim a save").
- Sources: `private-sources/cooking/context/claude-project-setup.md`, `private-sources/home-design/context/assistant-instructions.md`, and `private-sources/council-skills/recipe-publish/` (the persistence check and "an update needs the current version" only; drop IDs, raw URLs, pushing `main`, and emoji titles).

## Resolution
Shipped as docs/specs/archive/S007-chat-path-and-adapters.md through PR #30, merged 2026-11-19; harvest: L007.

## Rationale

## Resulting map updates
