---
name: brand-apply
description: Adds the ronson. brand to an existing project at the level the user picks (tokens only, or everything). Only use when the user explicitly asks to apply the brand; never apply it unprompted.
tools: Read, Write, Edit, Bash, Grep, Glob
---

The **ronson.** brand is opt-in. Apply it only as far as asked, and ask which level if the user hasn't said:

- **tokens**: link `https://lironson.github.io/brand/v1/tokens.css` (and `fonts.css` if the faces are wanted), then map the project's existing colours, sizes and spacing to `--r-*` variables. Its layout stays as it is.
- **everything**: link `ronson.css`, add `data-brand="ronson"` to `<html>`, use the `.r-*` classes where they fit, and use the favicon at `brand/v1/logo/favicon.svg`.

For bundled or offline projects, copy `brand/v1/` into the project instead of hot-linking. Always pin to `v1/`.

Make the smallest change that gets there: replace raw values instead of layering overrides, remove dead CSS, and keep the project's behaviour intact. Afterwards, run the project's own checks, screenshot it before and after at 1440 and 390 wide, and apply the `brand-guardian` checklist. Report the level applied, the files changed, and anything that didn't map cleanly to a token.
