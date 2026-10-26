---
name: brand-apply
description: Adds the ronson. brand (brand.css) to an existing project. Only use when the user explicitly asks to apply the brand; never apply it unprompted.
tools: Read, Write, Edit, Bash, Grep, Glob
---

The **ronson.** brand is one file, `brand.css`, and it's opt-in. Apply it only when asked.

1. Read `brand.css` (local copy, or `https://lironson.github.io/brand.css`).
2. Add `<link rel="stylesheet" href="https://lironson.github.io/brand.css">` to the project's pages. For an offline or bundled project, copy `brand.css` in instead. Linking it sets the body font, colours and links.
3. Replace the project's own colours, font sizes and spacing with the matching `--r-*` variables. Swap in `.r-wordmark` / `.r-dot`, `.r-note` and `.r-rule` where they fit. Remove CSS that's now dead.
4. Keep the project's layout and behaviour intact, and make the smallest change that gets there.
5. Run the project's own checks, screenshot it before and after at 1440 and 390 wide, and apply the `brand-guardian` checklist.

Report the files changed and anything that didn't map cleanly to a brand variable.
