# Rules for Antigravity

- **Ignore conversation‑summary blocks**: When a message contains a section titled "Conversation Summaries" (or similar headings) treat the entire block as read‑only context. Do **not** infer new tasks from any sentences inside that block, even if they look like user intents.

- **Respect explicit user intent**: Only generate content when the user explicitly asks for it in the current turn.

These rules prevent accidental generation of titles/objectives/LinkedIn posts from historical summaries.
