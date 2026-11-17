# Design tools: Figma and FigCraft

Mockups in this skill are generated as SVG by Python (`kit/`), so no design app is required. Use a design tool when the user wants to edit by hand, hand off to a designer, or prototype clicks.

## Figma
- **Import a mockup:** every example writes an SVG before rendering (`d.save(...)`). Drag the SVG into Figma: groups keep their `id` names (Button, Card, Price, Tag...), so layers arrive named and editable. Text is converted to paths for exact looks; retype a label in Figma if it must stay editable.
- **Figma MCP (official):** when connected, an agent can create frames, components and auto layout directly (`use_figma`), read a design back as context (`get_design_context`), and take screenshots (`get_screenshot`). Load the Figma skill the MCP provides before writing to a file. The free plan has a small tool-call quota, so build the screen as one SVG import instead of hundreds of small calls.
- **Components:** turn buttons, price pills and cards into components with variants (`State=Default/Hover/Pressed`, `Tier=Common..Mythic`) so a whole shop updates from one place.
- **Export for Roblox:** export each interactive piece as PNG at 2x (max 1024 px per side), the static background as one PNG, then follow `roblox-pipeline.md`.

## FigCraft
FigCraft is a free, Figma-like editor with its own MCP (layers, components, variants, auto layout, prototypes, `.fig` export). Useful when the user has no paid Figma plan or wants the agent to drive the editor fully.
- Open or import: `open_file` on an `.svg`, or `file.import {path, x, y}` into an existing document (returns the frame id).
- Fast loop: regenerate the SVG in Python, `edit.delete` the old frame and `file.import` the new one in one `batch`, then `screenshot {ids}` to check.
- Fonts are session-only (`text.loadFont {path}`); text-as-paths from `kit/text_paths.py` avoids the problem.
- Components: `component.create {ids}`, variants with `component.combineVariants` (layer names must be `Prop=Value`).
- Prototype hover/click with `proto.interaction.add`; keep looping idle animations for Roblox itself (FigCraft prototypes get slow with many loops).
- Export: `file.export {ids, format:"png", scale:2, path}`; a Figma copy with `file.export {format:"fig"}`.
- Live view for the user: `collab.share` returns a code and link to join the session.

## Which one
| Situation | Use |
|---|---|
| Quick look, iterate with the agent | Python kit only |
| User wants to tweak by hand / hand off | Figma (import the SVG) |
| No paid Figma, agent drives everything | FigCraft |
| Final assets for Roblox | PNG export, then `roblox-pipeline.md` |
