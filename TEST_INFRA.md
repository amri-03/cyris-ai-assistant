# Cyris AI Assistant - Visual Overhaul Test Infrastructure (TEST_INFRA.md)

This document outlines the testing infrastructure, verification protocols, and E2E test suite matrix for the Cyris AI Assistant Visual Overhaul. This framework covers programmatic compilation verification, backend decoupling checks, visual style and layout audits, and a comprehensive suite of 64 test cases across Tiers 1 to 4.

---

## 1. Introduction and Objectives

The primary objective of the Cyris Visual Overhaul is to deliver a premium, industry-standard visual and interactive experience comparable to Linear or Claude, while adhering to strict structural and behavioral constraints. The testing infrastructure is designed to:
- Programmatically verify styling consistency, theme token adherence, custom scrollbars, and focus indicator requirements (R1, R3).
- Programmatically verify layout structure, brand positioning, and mobile responsive behaviors (R2).
- Programmatically enforce backend decoupling, ensuring zero modifications to `backend/` files and database schemas (R4).
- Provide a robust coverage matrix of 64 test cases spanning functional, boundary, interaction, and real-world scenarios.

---

## 2. Requirement Mapping and Verification Scope

### Target Scope
The test infrastructure monitors and verifies the following frontend targets:
- `frontend/src/pages/Home.jsx`
- `frontend/src/components/Sidebar.jsx`
- `frontend/src/components/Header.jsx`
- `frontend/src/components/MessageInput.jsx`
- `frontend/src/components/MessageBubble.jsx`
- `frontend/src/styles/global.css`

### Interface Contracts
- **Home.jsx ↔ Sidebar.jsx**: Communicates active session states, toggles drawer views, groups conversations by date, and dispatches deletion operations.
- **Home.jsx ↔ Header.jsx**: Passes sidebar collapse state, current session title, settings visibility, and session conclusion triggers.
- **Home.jsx ↔ MessageInput.jsx**: Feeds user inputs into the API POST handlers, disabling input fields during active AI thinking state.
- **MessageBubble.jsx ↔ CodeBlock / Markdown**: Renders nested inline code blocks, headers, bulleted lists, and supports typing animation with auto-scrolling hooks.

---

## 3. Programmatic Verification Suite

To automate verification, a test runner script (`testing/run_e2e_checks.py`) will perform three sequential phases:

### Phase A: Compilation Check
The script executes:
```bash
cd frontend && npm run build
```
It monitors the return code (must be `0`) and verifies that output bundles are successfully generated under `frontend/dist/`.

### Phase B: Backend Decoupling Enforcement (R4)
The script verifies that the backend remains unmodified:
1. Runs `git status --porcelain backend` and fails if any modifications are detected.
2. Computes the SHA256 checksum of `backend/app/db.py` and compares it to a baseline:
   `db_py_baseline_sha256 = "c08e5e7ab3d6d03cf1e95fa8093db2e8f1766a2e4e137bfa5034c56ab6fb70ab"` (computed from the unmodified db.py).

### Phase C: Static Analysis Audits
The script scans file contents using regex patterns to verify visual and structural requirements:

| Requirement | Target File(s) | Audited Regex Patterns & Rules | Verification Objective |
| :--- | :--- | :--- | :--- |
| **R1: Color Palette** | `global.css` | `--bg-base:\s*#080809;`<br>`--text-primary:\s*#f4f4f5;`<br>`--text-secondary:\s*#a1a1aa;` | Ensure Obsidian dark base background and Slate primary text color hierarchy are defined. |
| **R1: Typography** | `global.css` | `@import url\(.*family=DM\+Mono.*family=Inter.*\);`<br>`--font-mono:\s*['"]DM Mono['"]`;<br>`--font-sans:\s*['"]Inter['"]`; | Ensure Google Font imports and font family definitions are correctly registered. |
| **R2: Responsive Sidebar** | `Sidebar.jsx`<br>`Home.jsx` | `window\.innerWidth\s*<\s*768`<br>`transition:\s*.*width\s+0\.3s` | Verify responsiveness window-size conditionals and CSS drawer width transitions. |
| **R2: Header Centering** | `Header.jsx` | `position:\s*["']absolute["']`<br>`left:\s*["']50%["']`<br>`transform:\s*["']translateX\(-50%\)["']` | Verify active session title is centered via absolute positioning in the header. |
| **R2: Logo Positioning** | `Sidebar.jsx`<br>`Header.jsx` | Sidebar must match: `Cyris`<br>Header must not contain: `Cyris` wordmark | Ensure wordmark branding is placed inside the sidebar only. |
| **R3: Custom Scrollbars** | `global.css` | `::-webkit-scrollbar`<br>`::-webkit-scrollbar-thumb`<br>`border-radius:\s*99px` | Verify that standard browser scrollbars are overridden with rounded, slim styling. |
| **R3: CSS Transitions** | `global.css` | `--transition:\s*0\.25s\s+cubic-bezier` | Verify application of a unified, custom cubic-bezier transition variable. |
| **R3: Focus Indicators** | `MessageInput.jsx` | `outline:\s*["']none["']` or `border:\s*["']none["']`<br>`isFocused\s*\?\s*["']var\(--accent-primary\)["']` | Verify default outlines are disabled and replaced with custom border glows on focus. |

---

## 4. Test Case Matrix (Tiers 1-4)

### Tier 1: Feature Coverage (24 Test Cases)

| Test ID | Feature | Description | Action / Input | Expected Output / Verification |
| :--- | :--- | :--- | :--- | :--- |
| **TC-FEAT-001** | Sidebar | Toggle Sidebar view. | Click sidebar collapse toggle button. | Sidebar width transitions smoothly between `260px` (open) and `0px` (closed). |
| **TC-FEAT-002** | Sidebar | Chronological session grouping. | Populate database with sessions updated today, 3 days ago, and 10 days ago. | Sessions are correctly categorized under headers "Today", "Previous 7 Days", and "Older". |
| **TC-FEAT-003** | Sidebar | Select active session. | Click a session item in the sidebar list. | Triggers `onSelectSession`, active session ID updates, chat panel is cleared, history loaded from API. |
| **TC-FEAT-004** | Sidebar | Delete session action. | Click session item menu `...` -> select "Delete Chat". | Sends `DELETE /sessions/{session_id}` request and removes the session from the list. |
| **TC-FEAT-005** | Header | Centered session title. | Select session with title "Refine UI Layout". | Active session title is positioned exactly in the center of the header via absolute positioning. |
| **TC-FEAT-006** | Header | Connection status dot. | Toggle backend server offline / online. | Connection indicator dot updates: green (`#4ade80`) for online, gray (`var(--text-muted)`) for offline. |
| **TC-FEAT-007** | Header | Settings toggle. | Click the settings cog button in the header. | Triggers `onOpenSettings` and displays the Settings Panel overlay. |
| **TC-FEAT-008** | Header | Conclude session. | Click the "Conclude" button in the header. | Current session concludes, resets the workspace to Empty State, clearing active session title. |
| **TC-FEAT-009** | Message Input | Textarea typing. | Type character sequence into input. | Text is displayed correctly inside the textarea with standard Inter font. |
| **TC-FEAT-010** | Message Input | Auto-resize container. | Type long, multi-line paragraph. | Textarea dynamically resizes height up to maximum of `160px` and displays inner scrollbar. |
| **TC-FEAT-011** | Message Input | Send with Enter key. | Press "Enter" key on keyboard without Shift. | Triggers `handleSend`, sends prompt to backend, clears the textarea and resets height to `26px`. |
| **TC-FEAT-012** | Message Input | Newline with Shift+Enter. | Press "Shift+Enter" on keyboard. | Adds a new line character inside the textarea, expanding container height without sending. |
| **TC-FEAT-013** | Message Bubble | User bubble styling. | Submit a user message. | Renders bubble aligned to the right, using `var(--user-bubble)` background and `var(--user-border)`. |
| **TC-FEAT-014** | Message Bubble | Assistant bubble layout. | Receive AI assistant message. | Renders message aligned to the left with transparent background and no borders. |
| **TC-FEAT-015** | Message Bubble | Typographic headings. | Receive text with `# Heading 1` and `## Heading 2`. | Displays headings with appropriate sizes (22px, 18px), weights (600), and margins. |
| **TC-FEAT-016** | Message Bubble | Inline markdown formatting. | Receive text with `**bold**` and `` `code` `` spans. | Renders bold text using `font-weight: 600` and code spans in monospace font with `var(--bg-elevated)`. |
| **TC-FEAT-017** | Message Bubble | Markdown list formatting. | Receive text with bullet (`*`) or numbered (`1.`) lines. | Renders as standard `<ul>` / `<ol>` with left padding (`24px`) and line spacing. |
| **TC-FEAT-018** | Message Bubble | Syntax code block. | Receive code snippet wrapped in triple backticks. | Code renders inside a custom pre block with headers indicating language and a working "Copy code" button. |
| **TC-FEAT-019** | Message Bubble | Typing animation. | Receive AI response with `animate: true`. | Text renders word-by-word with a 25ms delay, autoscrolling the thread container to the bottom. |
| **TC-FEAT-020** | Message Bubble | Utility feedback action. | Click the thumbs up/down buttons on assistant bubble. | Updates button active border and submits feedback to `/message/feedback` endpoint. |
| **TC-FEAT-021** | Settings Panel | Open Settings drawer. | Click settings gear button in header. | Settings panel slides in from the right, displaying theme and configuration toggles. |
| **TC-FEAT-022** | Settings Panel | Theme toggle switch. | Toggle theme between "light" and "dark". | App theme toggles, applying corresponding variables to elements. |
| **TC-FEAT-023** | Settings Panel | LocalStorage persistence. | Select "light" theme and reload the page. | Light theme remains active on reload; local storage value `"cyris-theme"` is preserved. |
| **TC-FEAT-024** | Empty State | Starter cards rendering. | Start a new session (0 messages). | Displays warm greeting, subtitle, starter prompt cards, and MessageInput in centered layout. |

---

### Tier 2: Boundary & Corner Cases (18 Test Cases)

| Test ID | Feature | Boundary Condition | Action / Input | Expected Output / Verification |
| :--- | :--- | :--- | :--- | :--- |
| **TC-BOUND-001** | Sidebar | Extremely long session titles. | Create chat session with a 150-character title. | Sidebar item text truncates with ellipsis (`text-overflow: ellipsis`) and does not break layout. |
| **TC-BOUND-002** | Sidebar | Empty session state. | Delete all sessions in the sidebar list. | Sidebar displays "No previous chats found." and does not crash or throw exceptions. |
| **TC-BOUND-003** | Sidebar | Rapid session deletes. | Click option menu -> delete on multiple sessions quickly. | Session lists update synchronously; React indices remain aligned, preventing deletion errors. |
| **TC-BOUND-004** | Header | Oversized session title. | Select session with long, multi-word title. | Centered title text truncates cleanly and does not overlap right-aligned buttons. |
| **TC-BOUND-005** | Header | Server connection drop. | Kill backend FastAPI server process. | Header connection status dot instantly changes to offline (`var(--text-muted)`) mode. |
| **TC-BOUND-006** | Header | Mobile toggle button hide. | Open sidebar on a desktop screen. | Sidebar toggle button in header is hidden since sidebar is already visible in layout. |
| **TC-BOUND-007** | Message Input | Whitespace only message. | Type spaces and press Enter or click send. | Send button is disabled, Enter key action is ignored, message is not sent. |
| **TC-BOUND-008** | Message Input | Mass clipboard paste. | Paste 10,000 words into the input textarea. | Input area expands to max-height `160px` with active scrollbar without hanging the browser. |
| **TC-BOUND-009** | Message Input | Input lock on thinking. | Send a message and wait during active thinking state. | Textarea gets `disabled` attribute; border color resets to `var(--border-subtle)`. |
| **TC-BOUND-010** | Message Bubble | Gigantic message block. | Load AI message containing 5000+ words. | Bubble renders completely, applying word-wrap/word-break rules without overflowing horizontally. |
| **TC-BOUND-011** | Message Bubble | Malformed markdown. | Load message with unmatched backticks or bold indicators. | Bubble renders text content safely, falling back to literal characters without breaking DOM. |
| **TC-BOUND-012** | Message Bubble | Interrupt typing animation. | Click a different sidebar session while typing is active. | Clears running `setInterval` loops instantly, discarding animation hooks. |
| **TC-BOUND-013** | Settings Panel | Corrupt local storage theme. | Set `"cyris-theme"` key in localStorage to `"corrupt_val"`. | Application falls back gracefully to dark theme, resetting localStorage to `"dark"`. |
| **TC-BOUND-014** | Settings Panel | Rapid theme toggling. | Click light/dark toggle buttons repeatedly in 1 second. | Body class and CSS variables update in sync without visual artifacts or memory leaks. |
| **TC-BOUND-015** | Settings Panel | Backdrop overlay interaction. | Click outside settings panel while open. | Closes settings panel, restoring interaction with the main workspace. |
| **TC-BOUND-016** | Empty State | Transition from empty view. | Click starter card prompt in Empty State. | Starters and greetings disappear, scrollable conversation view loads instantly. |
| **TC-BOUND-017** | Empty State | First time launch database. | Clear all PostgreSQL table contents and run app. | Greeting loads, session title remains empty, no errors appear in console. |
| **TC-BOUND-018** | Empty State | Server offline card click. | Disconnect server and click a starter card. | User bubble is added, followed by an error message. Start view transitions to thread view. |

---

### Tier 3: Cross-Feature Combinations (12 Test Cases)

| Test ID | Features Combined | Description / Interaction | Action / Input | Expected Output / Verification |
| :--- | :--- | :--- | :--- | :--- |
| **TC-CROSS-001** | Theme Switch x Messages | Bubble contrast updates on theme toggle. | Toggle theme light/dark in Settings with active chat history. | Bubble backgrounds (`var(--user-bubble)`) and borders update contrast to maintain WCAG AA compliance. |
| **TC-CROSS-002** | Mobile View x Sidebar | Sidebar collapse behavior on small screens. | Simulate mobile viewport (width < 768px) and select a chat session. | Sidebar closes automatically (`isOpen` = false, width `0px`) to free screen space. |
| **TC-CROSS-003** | Chat Send x Title Gen | Title update in header and sidebar list. | Send first message in a brand new chat. | Post chat triggers title generation thread; centered header title and sidebar item update from empty to generated title. |
| **TC-CROSS-004** | Settings x Input Focus | Focus control on panel overlay. | Open Settings Panel while MessageInput textarea is focused. | Input textarea loses focus (`onBlur` triggered); settings backdrop intercepts inputs. |
| **TC-CROSS-005** | Sidebar Delete x View | Deleting active session resets chat view. | Delete the active session from the sidebar options menu. | Chat view resets to Empty State; Header title is cleared; activeSessionId is reset to null. |
| **TC-CROSS-006** | Thinking State x Reset | Conclude session during active thinking. | Click "Conclude" button in header while AI response is loading. | Aborts active state, sets `isThinking` to false, and returns workspace to Empty State. |
| **TC-CROSS-007** | Markdown x Autoscroll | Autoscrolling during complex rendering. | Let AI return markdown containing images, code blocks, lists. | Container continues autoscrolling to the bottom as each block element renders. |
| **TC-CROSS-008** | Starter Card x Input | Starter card clicks reset textarea height. | Click starter card when input contains text. | Starter card prompt overrides input value, sends message, and resets input height to `26px`. |
| **TC-CROSS-009** | Sidebar Toggle x Reflow | Smooth viewport reflow on toggle. | Toggle sidebar open/closed repeatedly. | Main chat panel width adjusts smoothly with transitions; text blocks reflow without jitter. |
| **TC-CROSS-010** | Theme x Code Contrast | Code blocks adapt to theme. | Switch theme from dark to light with code block visible. | Code background (`var(--bg-code-block)`) changes from `#111113` to `#f4f4f7`; text color matches readability standards. |
| **TC-CROSS-011** | Status Dot x Send | Send message in offline mode. | Disconnect server and send message. | Header status dot turns gray; Message is sent, followed by a failure message bubble. |
| **TC-CROSS-012** | Dropdown x Scroll | Dropdown menu positioning on sidebar scroll. | Open options dropdown menu in sidebar and scroll sidebar. | Dropdown remains attached to parent session item or closes. |

---

### Tier 4: Real-World Scenarios (10 Test Cases)

| Test ID | Scenario Name | Description | Action / Input | Expected Output / Verification |
| :--- | :--- | :--- | :--- | :--- |
| **TC-REAL-001** | Tab Reload Restoration | Session reload and theme preservation. | Refresh page while viewing a specific session in light theme. | Re-activates light theme; reloads active session history; sidebar retains scroll position. |
| **TC-REAL-002** | Connection Recovery | Auto-recovery of API connectivity. | Disconnect backend during chat, submit message, reconnect backend, submit message. | First message fails; connection status dot changes to gray. Reconnect restores green status dot and subsequent message succeeds. |
| **TC-REAL-003** | Rapid Input Spam | Rapid message sending during thinking state. | Rapidly press enter / submit button before AI response returns. | UI ignores additional submissions while input remains disabled during `isThinking` state. |
| **TC-REAL-004** | Multi-Language Code | Code blocks rendering in single bubble. | Request code block in Python and code block in Javascript. | Bubble renders two distinct, styled code blocks with correct language labels and independent copy buttons. |
| **TC-REAL-005** | Keyboard Accessibility | Fully accessible keyboard navigation. | Navigate workspace using `Tab` and `Shift+Tab`. | Custom focus states (glowing outline, colored borders) appear on all active elements. |
| **TC-REAL-006** | Viewport Transitions | Resizing layout desktop/mobile. | Resize browser width from `1200px` to `480px` and back. | Sidebar transitions from visible desktop drawer to responsive mobile overlay; header content positions adjust correctly. |
| **TC-REAL-007** | Autoscroll Interruption | Manual scroll overrides autoscroll. | Scroll upward while AI is typing response. | Autoscroll pauses, allowing user to read previous text. Autoscroll resumes if user scrolls back to bottom. |
| **TC-REAL-008** | Accessibility Contrast | Text contrast WCAG conformance. | Test text colors on dark and light backgrounds. | Primary, secondary, and badge colors exceed contrast ratio of 4.5:1 on background surfaces. |
| **TC-REAL-009** | Rapid Session Switch | Switch sessions during loading states. | Click different sessions rapidly in sidebar while history is loading. | Only the history of the last selected session is rendered; older API responses are discarded. |
| **TC-REAL-010** | Decoupled Lock | Verify backend files remain unmodified. | Run compile check and git audit. | Frontend compiles cleanly into `dist/`; git status verifies zero modifications in `backend/` files or db schemas. |
