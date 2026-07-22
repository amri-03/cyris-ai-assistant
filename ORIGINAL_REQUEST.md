# Original User Request

## Initial Request — 2026-07-15T10:31:05+05:30

Deliver a complete visual overhaul of the Cyris frontend into a premium, polished, industry-standard experience comparable to products like Linear and Claude.

Working directory: c:\Developer_Workspace\active_projects\AI-Projects\cyris-ai-assistant
Integrity mode: benchmark

## Requirements

### R1. Visual System and Premium Language
Define and apply a cohesive visual direction using the `/frontend-design` skill guidelines. This includes layout proportions, a refined color system (obsidian/slate-based palette), typography hierarchy (sans/mono scale), and modern interface styling.

### R2. Responsive Layout Refactoring
Refactor React layout components (`Home.jsx`, `Sidebar.jsx`, `Header.jsx`, `MessageInput.jsx`, `MessageBubble.jsx`, and `global.css`) to optimize layout branding and titles. Explore modern positioning options (e.g., brand logo in the sidebar vs. centered navbar titles) and present the best visual spec for approval.

### R3. Visual Polish & Micro-Interactions
Implement professional, understated layout spacing, custom slim scrollbars, clean transition animations (hover states, collapsing sidebars), and polished state indicator styles (avoiding browser default focus rings).

### R4. Integrity & Decoupling Constraint
All updates must be restricted to the frontend directory (`frontend/src/` and associated assets). The team must not modify any backend python code (`backend/app/` or database schemas).

## Verification Resources
- [frontend-design skill SKILL.md](file:///c:/Developer_Workspace/active_projects/AI-Projects/cyris-ai-assistant/.agents/skills/frontend-design/SKILL.md): Design instructions and guidelines.

## Acceptance Criteria

### Visual Consistency (Design QA Audited)
- [ ] Wordmark branding and active session titles are positioned in a clean, modern, and approved visual hierarchy.
- [ ] Custom scrollbars are rounded, slim, and visually integrated.
- [ ] Form inputs have polished, modern active focus indicator states.
- [ ] Elements use consistent, theme-based CSS transition speeds and visual hover cues.

### Decoupling & Compilation (Programmatic Verification)
- [ ] Frontend compiles without any errors or warnings when running `npm run build` from the `frontend/` directory.
- [ ] Running `git status` shows zero modifications in the `backend/` directory.

## Follow-up — 2026-07-22T05:44:27Z

Redesign the Cyris AI Assistant frontend into a minimal, premium, and visually intentional interface — clean and direct like a focused tool, not a ChatGPT/Claude clone. All existing backend API integrations must continue to work unchanged.

Working directory: c:\Developer_Workspace\active_projects\AI-Projects\cyris-ai-assistant\frontend
Integrity mode: development

---

## Context

The frontend lives at `frontend/src/`. The backend runs on `http://localhost:8000`. The API service is in `frontend/src/services/api.js`. All existing API calls (`POST /chat`, `GET /sessions`, `GET /sessions/:id/messages`, `DELETE /sessions/:id`, `GET /memory-status`, `DELETE /memory/:identity`) must continue working.

The existing `global.css` has a solid design token system (color variables, typography, radius, transitions) — **preserve the CSS variables and design tokens**, but the visual layout and component styles are open for a full overhaul.

The current design has too many visual layers (glassmorphic headers, ambient pulse animations, collapsible sidebars) that add noise without adding clarity. The goal is **restraint, not richness**.

---

## Requirements

### R1. Minimal, Focused Chat Interface
The primary view should be a single, centered conversation thread. The user should feel they are in dialogue with a focused assistant — not navigating a product. The message input must always be accessible. Empty state must feel calm and intentional — not generic.

### R2. Session Management — Minimal, Not Prominent
Past sessions must be accessible (the backend supports `GET /sessions`), but the session list should not dominate the layout. It may be a subtle sidebar, a top-bar dropdown, or a slide-in panel — whichever approach best serves minimalism. The active session's title should be visible but understated.

### R3. Memory Panel — Accessible, Not Intrusive
The user must be able to view and delete continuity memory items (via `GET /memory-status` and `DELETE /memory/:identity`). This feature should be available but not foregrounded — a subtle access point is preferred over a persistent panel.

### R4. Theme Support
Light and dark themes must both work correctly and look polished. The existing CSS variable system (`--bg-base`, `--text-primary`, `--accent-primary`, etc.) should be used as the foundation. Theme preference must persist via `localStorage`.

### R5. Visual Quality Bar
The result must feel intentional and restrained. No generic gradients. No excessive animation. Typography, spacing, and color contrast must work together. The interface should feel like it was designed for a specific person, not assembled from a UI kit.

---

## Acceptance Criteria

### Functionality
- [ ] Sending a chat message and receiving a response works end-to-end
- [ ] Page refresh restores the current session's messages
- [ ] Past sessions are accessible and can be switched between
- [ ] Memory panel opens, shows continuity items, and deletion works
- [ ] Light and dark themes both render correctly and persist on reload
- [ ] Mobile viewport (375px width) is usable — no broken layouts or overflow

### Visual Quality (agent-as-judge)
- [ ] Empty state feels calm and intentional — not generic assistant boilerplate
- [ ] Message thread is easy to read — clear user/assistant distinction without heavy bubbles
- [ ] Input area is clean and keyboard-accessible
- [ ] Session navigation is minimal — does not compete with the conversation for visual weight
- [ ] No layout elements feel like they were copied from ChatGPT or Claude
- [ ] Both light and dark themes look like deliberate design choices, not inversions of each other

### Code Quality
- [ ] No inline `style={{}}` objects for layout or decoration — CSS classes only
- [ ] All existing API integrations preserved — no removed endpoints or broken calls
- [ ] No new npm packages added unless absolutely necessary
