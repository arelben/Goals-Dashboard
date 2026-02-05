---
name: reflex-ui
description: >
  Best practices for Reflex UI components.
  Trigger: When creating or modifying Reflex pages and components.
metadata:
  author: arelben
  version: "1.0"
  scope: [root]
  auto_invoke: "Creating/modifying Reflex UI components"
---

## Critical Rules
- ALWAYS use `rx.vstack` or `rx.hstack` for layout instead of raw CSS if possible.
- ALWAYS use a consistent spacing and color palette (Glassmorphism).
- ALWAYS separate state logic into `State` classes.
- AVOID "AI slop" aesthetics:
    - NO excessive centered layouts.
    - NO purple/generic gradients.
    - NO perfectly uniform rounded corners (use variable radii for a more organic, premium feel).
    - AVOID standard fonts like Inter if better alternatives (Roboto, Outfit) are available.

## Example
```python
def goal_card(goal: dict) -> rx.Component:
    return rx.box(
        rx.text(goal["title"], font_weight="bold"),
        rx.text(goal["description"]),
        border="1px solid #e1e1e1",
        padding="4",
        border_radius="lg",
    )
```
Documentation: https://reflex.dev/docs/getting-started/introduction/
Component Library: https://reflex.dev/docs/library/