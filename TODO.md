# TODO

## Next
- `git`: make first commit (repo already init)
- Fix/lock build chain: `tools/build_actions_catalog.py` must run before `tools/build_api_aliases.py` (ids affect translations)
- Remove/merge duplicates: root scripts vs `tools/*` (keep `tools/*` as source of truth)
- DSL compiler: `*.mldsl` -> `/placeadvanced ...` (done, but needs nicer CLI / VS Code task)
- Use `out/api_aliases.json` for action lookup and slot/enum mapping
- Add enum sugar: `separator=" "` -> `clicks(slot,n)=0` (done for known enums)
- Decide event syntax and action namespace: `event(join) { player.message(...) }`
- Improve error messages: show which line failed + near-token
- Decide strategy for `/placeadvanced` 240-char limit (for now: hard error)
- Docs site (RU-first): MkDocs Material + GitHub Pages, generate tracked `docs/` (don't rely on ignored `out/`)

## Later
- Improve English names in `tools/action_translations_by_id.json`
- Add action docs export (web/markdown)
- Add formatting/linting rules for DSL
