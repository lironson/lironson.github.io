# ronson. brand

A quiet system: mostly paper, a little ink, and one orange dot. It borrows a few small things from shop drawings (hairlines with end ticks, mono numbering, a "rev" note) and nothing more.

The brand is opt-in. A project can take as much or as little as it wants:

```html
<!-- variables only: changes nothing on its own -->
<link rel="stylesheet" href="https://lironson.github.io/brand/v1/tokens.css">

<!-- everything: fonts, tokens, .r-* classes, and base styles inside data-brand -->
<link rel="stylesheet" href="https://lironson.github.io/brand/v1/ronson.css">
<html data-brand="ronson">
```

Between those two levels, you can also link `fonts.css`, `tokens.css` and `components.css` separately. The classes do nothing until you use them.

| Class | What it is |
|---|---|
| `.r-page` | centred single column, 36rem wide |
| `.r-wordmark` + `.r-dot` | `ronson<span class="r-dot">.</span>` |
| `.r-rule`, `.r-rule--ticked` | hairline, with optional end ticks (use a `div role="separator"`) |
| `.r-dim` | a dimension line `├── 640 ──┤` |
| `.r-note` | small mono note: numbers, revs, dates |
| `.r-list` / `.r-item` | numbered list separated by hairlines |
| `.r-link` | link with a hairline underline |

**Theme:** follows the OS. Force a theme with `data-theme="light"` or `data-theme="dark"`.

**Versioning:** `v1/` only changes in backward-compatible ways. Breaking changes go in `v2/`.

**Offline use:** copy `brand/v1/`; all paths are relative. `tokens.json` covers non-web tools.

- Brand sheet: `v1/guidelines.html`
- Mockups: `mockups/`
- Logo: `v1/logo/`, regenerated with `python3 brand/v1/_build/build_logo.py`

## Agents
`.claude/agents/` has three Claude Code agents: `brand-guardian` (a read-only review), `brand-designer` (pages and assets), and `brand-apply` (adds the brand to a project, only when asked). To use them in every project, run `sh brand/install-agents.sh`, which copies them to `~/.claude/agents/`.
