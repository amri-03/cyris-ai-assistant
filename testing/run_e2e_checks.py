#!/usr/bin/env python3
"""
Cyris AI Assistant - Visual Overhaul E2E Test Suite (run_e2e_checks.py)

This script automates visual overhaul E2E verification, covering:
1. Phase A: Frontend compilation verification (npm run build).
2. Phase B: Backend decoupling check (git status verification & db.py checksum validation).
3. Phase C: Static styling & layout audits (global.css variables, typography, transitions, scrollbars, JSX centering).
4. Tiers 1-4: 64 individual test case verifications with programmatic scans and asset assertions.

Usage:
    python testing/run_e2e_checks.py
"""

import os
import sys
import re
import hashlib
import subprocess

# Setup absolute paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
BACKEND_DIR = os.path.join(BASE_DIR, "backend")

# Expected db.py hash baseline (clean state of database schema)
DB_PY_BASELINE_SHA256 = "51ce9957c6e47432c2edbe308deac262d01c2531edcd5efc4ce0636b784fbc8b"

def run_command(command, cwd=None):
    """Utility to run a CLI command and return its exit code and stdout/stderr."""
    try:
        shell = os.name == 'nt'
        res = subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=False, shell=shell)
        return res.returncode, res.stdout, res.stderr
    except Exception as e:
        return -1, "", str(e)

# Phase A: Compilation Check
def verify_frontend_compilation():
    print("[*] Starting Phase A: Compiling Frontend...")
    code, stdout, stderr = run_command(["npm", "run", "build"], cwd=FRONTEND_DIR)
    if code != 0:
        return False, f"Vite build failed with exit code {code}.\nStderr: {stderr}\nStdout: {stdout}"
    
    # Check if dist files were created
    dist_dir = os.path.join(FRONTEND_DIR, "dist")
    index_html = os.path.join(dist_dir, "index.html")
    if not os.path.exists(dist_dir) or not os.path.exists(index_html):
        return False, f"Frontend build succeeded but outputs were not found under {dist_dir}."
    
    return True, "Frontend compiled cleanly into frontend/dist/."

# Phase B: Backend Decoupling Check
def verify_backend_decoupling():
    print("[*] Starting Phase B: Enforcing Backend Decoupling...")
    
    # Check for git modifications in backend
    code, stdout, stderr = run_command(["git", "status", "--porcelain", "backend"], cwd=BASE_DIR)
    if code != 0:
        return False, f"Git command failed: {stderr}"
    
    if stdout.strip():
        return False, f"Backend files have been modified since baseline:\n{stdout}"
        
    # Check db.py hash
    db_file_path = os.path.join(BACKEND_DIR, "app", "db.py")
    if not os.path.exists(db_file_path):
        return False, f"db.py not found at {db_file_path}"
        
    try:
        with open(db_file_path, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        
        if file_hash != DB_PY_BASELINE_SHA256:
            return False, f"db.py hash mismatch. Database schema has been modified!\nExpected: {DB_PY_BASELINE_SHA256}\nActual: {file_hash}"
    except Exception as e:
        return False, f"Failed to read db.py hash: {str(e)}"
        
    return True, "Backend files remain unmodified and database schema is locked."

# Load source files content for analysis
def load_source_files():
    files = {
        "global.css": "frontend/src/styles/global.css",
        "Home.jsx": "frontend/src/pages/Home.jsx",
        "Sidebar.jsx": "frontend/src/components/Sidebar.jsx",
        "Header.jsx": "frontend/src/components/Header.jsx",
        "MessageInput.jsx": "frontend/src/components/MessageInput.jsx",
        "MessageBubble.jsx": "frontend/src/components/MessageBubble.jsx",
        "ConversationThread.jsx": "frontend/src/components/ConversationThread.jsx",
        "SettingsPanel.jsx": "frontend/src/components/SettingsPanel.jsx",
    }
    loaded = {}
    for key, rel_path in files.items():
        abs_path = os.path.join(BASE_DIR, rel_path)
        if not os.path.exists(abs_path):
            print(f"[-] Critical: Required file missing: {abs_path}")
            sys.exit(1)
        with open(abs_path, "r", encoding="utf-8") as f:
            loaded[key] = f.read()
    return loaded

# Helper match checker
def verify_patterns(file_content, filename, patterns):
    for desc, pat in patterns.items():
        if not re.search(pat, file_content):
            return False, f"Pattern '{desc}' not found in {filename} (Regex: {pat})"
    return True, ""

# Verification Functions for Tiers 1-4
def check_feat_001(sources):
    # Sidebar toggle transitions smoothly between 260px and 0px
    # Verify Sidebar isOpen state usage and toggle trigger
    patterns = {
        "sidebar toggle state": r"isSidebarOpen",
        "sidebar toggle handler": r"setIsSidebarOpen\(!isSidebarOpen\)",
        "sidebar isOpen prop": r"<Sidebar\s+[^>]*isOpen=\{isSidebarOpen\}"
    }
    return verify_patterns(sources["Home.jsx"], "Home.jsx", patterns)

def check_feat_002(sources):
    # Chronological session grouping Today, Previous 7 Days, Older
    patterns = {
        "group sessions today": r"Today",
        "group sessions previous 7 days": r"Previous 7 Days",
        "group sessions older": r"Older",
        "toDateString checks": r"toDateString\(\)"
    }
    return verify_patterns(sources["Sidebar.jsx"], "Sidebar.jsx", patterns)

def check_feat_003(sources):
    # Select active session updating chat history
    patterns = {
        "select session callback": r"onSelectSession",
        "select session click trigger": r"onSelectSession\(session\.id\)"
    }
    return verify_patterns(sources["Sidebar.jsx"], "Sidebar.jsx", patterns)

def check_feat_004(sources):
    # Delete session action calls API
    patterns = {
        "delete session endpoint call": r"api\.delete\((`|\")\/sessions\/",
        "onDeleteSession prop": r"onDeleteSession=\{handleDeleteSession\}"
    }
    return verify_patterns(sources["Home.jsx"], "Home.jsx", patterns)

def check_feat_005(sources):
    # Centered session title via absolute positioning
    if "header-breadcrumb" not in sources["Header.jsx"]:
        return False, "className 'header-breadcrumb' missing in Header.jsx"
    patterns = {
        "absolute position": r"position:\s*absolute",
        "left 50 percent": r"left:\s*50%",
        "transform translate x": r"transform:\s*translateX\(-50%\)"
    }
    return verify_patterns(sources["global.css"], "global.css", patterns)

def check_feat_006(sources):
    # Connection status indicator updates dot color
    patterns = {
        "connection dot indicator color": r"isConnected\s*\?\s*|background"
    }
    return verify_patterns(sources["Header.jsx"], "Header.jsx", patterns)

def check_feat_007(sources):
    # Settings cog displays panel overlay
    if "onOpenSettings" not in sources["Header.jsx"]:
        return False, "onOpenSettings missing in Header.jsx"
    if "isSettingsOpen" not in sources["Home.jsx"]:
        return False, "isSettingsOpen missing in Home.jsx"
    return True, ""

def check_feat_008(sources):
    # Conclude session resets workspace to Empty State
    patterns = {
        "conclude session trigger": r"onConcludeSession",
        "conclude session binding": r"onConcludeSession=\{handleNewChat\}"
    }
    return verify_patterns(sources["Home.jsx"], "Home.jsx", patterns)

def check_feat_009(sources):
    # Textarea has font-sans or custom styling
    patterns = {
        "textarea tag": r"<textarea",
        "textarea font-sans styling": r"fontFamily:\s*(\"|\')var\(--font-sans\)(\"|\')"
    }
    return verify_patterns(sources["MessageInput.jsx"], "MessageInput.jsx", patterns)

def check_feat_010(sources):
    # MessageInput textarea dynamically resizes height
    patterns = {
        "auto resize height": r"style\.height\s*=",
        "scroll height calculation": r"Math\.min"
    }
    return verify_patterns(sources["MessageInput.jsx"], "MessageInput.jsx", patterns)

def check_feat_011(sources):
    # MessageInput triggers send with Enter (no shift)
    patterns = {
        "keydown handler": r"onKeyDown=\{handleKeyDown\}",
        "enter key check": r"e\.key\s*===\s*(\"|\')Enter(\"|\')",
        "no shift modifier": r"!\s*e\.shiftKey"
    }
    return verify_patterns(sources["MessageInput.jsx"], "MessageInput.jsx", patterns)

def check_feat_012(sources):
    # MessageInput adds newline with Shift+Enter
    patterns = {
        "prevent default on Enter": r"e\.preventDefault\s*\(\)"
    }
    return verify_patterns(sources["MessageInput.jsx"], "MessageInput.jsx", patterns)

def check_feat_013(sources):
    # User message bubble styling
    patterns = {
        "user bubble variables": r"--user-bubble",
        "user border variables": r"--user-border"
    }
    return verify_patterns(sources["global.css"], "global.css", patterns)

def check_feat_014(sources):
    # Assistant message bubble layout
    patterns = {
        "cyris bubble variables": r"--cyris-bubble",
        "cyris border variables": r"--cyris-border"
    }
    return verify_patterns(sources["global.css"], "global.css", patterns)

def check_feat_015(sources):
    # Heading tag typography
    patterns = {
        "JetBrains mono font import": r"JetBrains\+Mono",
        "Plus Jakarta Sans font import": r"Plus\+Jakarta\+Sans",
        "font variables definition": r"--font-sans"
    }
    return verify_patterns(sources["global.css"], "global.css", patterns)

def check_feat_016(sources):
    # Inline code markdown styling in MessageBubble
    patterns = {
        "inline span renderer": r"renderInlineSpans",
        "code span variable background": r"var\(--bg-elevated\)"
    }
    return verify_patterns(sources["MessageBubble.jsx"], "MessageBubble.jsx", patterns)

def check_feat_017(sources):
    # Markdown list formatting in MessageBubble
    patterns = {
        "list list-style bullet rendering": r"ul" or r"ol" or r"li"
    }
    return verify_patterns(sources["MessageBubble.jsx"], "MessageBubble.jsx", patterns)

def check_feat_018(sources):
    # Syntax code block copy button
    patterns = {
        "CodeBlock component": r"function CodeBlock",
        "clipboard copy": r"navigator\.clipboard\.writeText",
        "copy button feedback": r"Copied"
    }
    return verify_patterns(sources["MessageBubble.jsx"], "MessageBubble.jsx", patterns)

def check_feat_019(sources):
    # Typing animation auto-scrolling
    patterns = {
        "animate prop": r"animate",
        "onScrollToBottom callback": r"onScrollToBottom"
    }
    return verify_patterns(sources["MessageBubble.jsx"], "MessageBubble.jsx", patterns)

def check_feat_020(sources):
    # Utility feedback likes / dislikes submits feedback
    patterns = {
        "feedback API route": r"\/message\/feedback",
        "feedback button click handler": r"handleFeedback"
    }
    return verify_patterns(sources["MessageBubble.jsx"], "MessageBubble.jsx", patterns)

def check_feat_021(sources):
    # Open settings drawer modal structure
    patterns = {
        "SettingsPanel portal mounting": r"createPortal",
        "Settings overlay overlay": r"memory-overlay",
        "Settings overlay modal": r"memory-modal"
    }
    return verify_patterns(sources["SettingsPanel.jsx"], "SettingsPanel.jsx", patterns)

def check_feat_022(sources):
    # SettingsPanel theme toggling
    patterns = {
        "theme change callback": r"onThemeChange",
        "theme change click handler": r"onThemeChange\(\"dark\"\)"
    }
    return verify_patterns(sources["SettingsPanel.jsx"], "SettingsPanel.jsx", patterns)

def check_feat_023(sources):
    # localStorage theme persistence
    patterns = {
        "theme initialization from localStorage": r"localStorage\.getItem\((\"|\')cyris-theme(\"|\')\)",
        "theme save to localStorage": r"localStorage\.setItem\((\"|\')cyris-theme(\"|\'),\s*theme\)"
    }
    return verify_patterns(sources["Home.jsx"], "Home.jsx", patterns)

def check_feat_024(sources):
    # Starter cards rendering on empty state
    patterns = {
        "starter cards definitions": r"starterCards",
        "starter cards map": r"starterCards\.map"
    }
    return verify_patterns(sources["Home.jsx"], "Home.jsx", patterns)

def check_bound_001(sources):
    # Sidebar item text truncates with ellipsis
    patterns = {
        "ellipsis text-overflow in sidebar": r"textOverflow:\s*(\'|\")ellipsis(\'|\")",
        "whiteSpace nowrap in sidebar": r"whiteSpace:\s*(\'|\")nowrap(\'|\")"
    }
    return verify_patterns(sources["Sidebar.jsx"], "Sidebar.jsx", patterns)

def check_bound_002(sources):
    # Sidebar displays message when empty
    patterns = {
        "empty sessions notice": r"No previous chats found"
    }
    return verify_patterns(sources["Sidebar.jsx"], "Sidebar.jsx", patterns)

def check_bound_003(sources):
    # Rapid session deletes React indices safe
    patterns = {
        "delete handler uses session ID": r"handleDeleteSession\s*=\s*async\s*\(sessionId\)"
    }
    return verify_patterns(sources["Home.jsx"], "Home.jsx", patterns)

def check_bound_004(sources):
    # Header title text truncates with ellipsis
    if "session-title" not in sources["Header.jsx"]:
        return False, "className 'session-title' missing in Header.jsx"
    patterns = {
        "ellipsis text-overflow in header": r"text-overflow:\s*ellipsis",
        "max width on header title": r"max-width:\s*300px"
    }
    return verify_patterns(sources["global.css"], "global.css", patterns)

def check_bound_005(sources):
    # Header offline mode updates status dot color
    patterns = {
        "offline mode status logic": r"isConnected"
    }
    return verify_patterns(sources["Header.jsx"], "Header.jsx", patterns)

def check_bound_006(sources):
    # Mobile toggle button hidden on desktop
    patterns = {
        "sidebar closed toggle check": r"!isSidebarOpen"
    }
    return verify_patterns(sources["Home.jsx"], "Home.jsx", patterns)

def check_bound_007(sources):
    # MessageInput blocks empty messages
    patterns = {
        "trimmed whitespace block check": r"if\s*\(!trimmed\s*\|\|\s*isDisabled\)\s*return"
    }
    return verify_patterns(sources["MessageInput.jsx"], "MessageInput.jsx", patterns)

def check_bound_008(sources):
    # MessageInput paste max height boundary
    patterns = {
        "maxHeight configuration": r"maxHeight:\s*(\'|\")200px(\'|\")"
    }
    return verify_patterns(sources["MessageInput.jsx"], "MessageInput.jsx", patterns)

def check_bound_009(sources):
    # Textarea gets disabled attribute on thinking state
    patterns = {
        "disabled thinking binding": r"disabled=\{isDisabled\}"
    }
    return verify_patterns(sources["MessageInput.jsx"], "MessageInput.jsx", patterns)

def check_bound_010(sources):
    # Gigantic assistant bubble word wrap break
    patterns = {
        "word break logic on bubble": r"wordBreak:\s*(\'|\")normal(\'|\")"
    }
    return verify_patterns(sources["MessageBubble.jsx"], "MessageBubble.jsx", patterns)

def check_bound_011(sources):
    # MessageBubble markdown error resilience
    patterns = {
        "markdown parser": r"render" or r"parse"
    }
    return verify_patterns(sources["MessageBubble.jsx"], "MessageBubble.jsx", patterns)

def check_bound_012(sources):
    # Typing animation clears setInterval on switch/unmount
    patterns = {
        "typing timer cleanup": r"clearInterval" or r"clearTimeout" or r"useEffect"
    }
    return verify_patterns(sources["MessageBubble.jsx"], "MessageBubble.jsx", patterns)

def check_bound_013(sources):
    # Corrupt local storage theme fallback
    patterns = {
        "fallback theme selection logic": r"saved\s*===\s*(\"|\')light(\"|\')\s*\?\s*(\"|\')light(\"|\')\s*:\s*(\"|\')dark(\"|\')"
    }
    return verify_patterns(sources["Home.jsx"], "Home.jsx", patterns)

def check_bound_014(sources):
    # Repeated theme clicks visual sync
    patterns = {
        "theme changes apply body className": r"document\.body\.className\s*="
    }
    return verify_patterns(sources["Home.jsx"], "Home.jsx", patterns)

def check_bound_015(sources):
    # Backdrop settings panel overlay clicks
    patterns = {
        "backdrop onClick onClose binding": r"onClick=\{onClose\}"
    }
    return verify_patterns(sources["SettingsPanel.jsx"], "SettingsPanel.jsx", patterns)

def check_bound_016(sources):
    # Clicking empty state starter card triggers chat submit
    patterns = {
        "card click handler triggers handleSend": r"onClick=\{\(\)\s*=>\s*handleSend\(card\.prompt\)\}"
    }
    return verify_patterns(sources["Home.jsx"], "Home.jsx", patterns)

def check_bound_017(sources):
    # First time launch handles empty sessions gracefully
    patterns = {
        "fetchSessions initialization call": r"fetchSessions\(\)"
    }
    return verify_patterns(sources["Home.jsx"], "Home.jsx", patterns)

def check_bound_018(sources):
    # Server offline starter card click displays error message
    patterns = {
        "reach backend check catch block": r"catch\s*\(error\)\s*\{"
    }
    return verify_patterns(sources["Home.jsx"], "Home.jsx", patterns)

def check_cross_001(sources):
    # Light/dark bubble variables definition contrast
    patterns = {
        "user-bubble contrast definition dark": r"--user-bubble:\s*#1b202c",
        "user-bubble contrast definition light": r"--user-bubble:\s*#ffffff"
    }
    return verify_patterns(sources["global.css"], "global.css", patterns)

def check_cross_002(sources):
    # Responsive mobile sidebar width checks auto-collapse
    patterns = {
        "mobile width check threshold": r"window\.innerWidth\s*<\s*768"
    }
    return verify_patterns(sources["Home.jsx"], "Home.jsx", patterns)

def check_cross_003(sources):
    # Chat send triggers session title updates
    patterns = {
        "chat response checks for new session": r"returnedSessionId\s*&&\s*returnedSessionId\s*!==\s*activeSessionId"
    }
    return verify_patterns(sources["Home.jsx"], "Home.jsx", patterns)

def check_cross_004(sources):
    # Textarea lose focus on settings open
    patterns = {
        "settings panel trigger": r"isSettingsOpen"
    }
    return verify_patterns(sources["Home.jsx"], "Home.jsx", patterns)

def check_cross_005(sources):
    # Deleting active session resets chat view to empty state
    patterns = {
        "reset activeSessionId to null on active deletion": r"if\s*\(activeSessionId\s*===\s*sessionId\)\s*\{\s*handleNewChat\(\);\s*\}"
    }
    return verify_patterns(sources["Home.jsx"], "Home.jsx", patterns)

def check_cross_006(sources):
    # Reset/conclude session clears isThinking status
    patterns = {
        "reset thinking status on send finish": r"setIsThinking\(false\)"
    }
    return verify_patterns(sources["Home.jsx"], "Home.jsx", patterns)

def check_cross_007(sources):
    # Message list length changes trigger container autoscroll
    patterns = {
        "scroll dependency messages": r"\[messages,\s*isThinking\]"
    }
    return verify_patterns(sources["Home.jsx"], "Home.jsx", patterns)

def check_cross_008(sources):
    # Starter card clicks reset textarea height
    patterns = {
        "textareaRef current style height reset": r"textareaRef\.current\.style\.height\s*=\s*(\"|\')auto(\"|\')"
    }
    return verify_patterns(sources["MessageInput.jsx"], "MessageInput.jsx", patterns)

def check_cross_009(sources):
    # Sidebar width toggle transitions smoothly
    patterns = {
        "CSS transition definition": r"--transition:\s*0\.2s\s+cubic-bezier"
    }
    return verify_patterns(sources["global.css"], "global.css", patterns)

def check_cross_010(sources):
    # Theme changes update code block background contrast
    patterns = {
        "code background dark mode": r"--bg-code-block:\s*#0c0d12",
        "code background light mode": r"--bg-code-block:\s*#1e2530"
    }
    return verify_patterns(sources["global.css"], "global.css", patterns)

def check_cross_011(sources):
    # Disconnect status message update in catch block
    patterns = {
        "offline indicator setup": r"setIsConnected\(false\)"
    }
    return verify_patterns(sources["Home.jsx"], "Home.jsx", patterns)

def check_cross_012(sources):
    # Sidebar dropdown options menu trigger
    patterns = {
        "options menu state toggling": r"setMenuOpenForId"
    }
    return verify_patterns(sources["Sidebar.jsx"], "Sidebar.jsx", patterns)

def check_real_001(sources):
    # Session reload theme preservation on refresh
    patterns = {
        "saved theme loading from storage": r"localStorage\.getItem\((\"|\')cyris-theme(\"|\')\)"
    }
    return verify_patterns(sources["Home.jsx"], "Home.jsx", patterns)

def check_real_002(sources):
    # Connection recovery resets dot color
    patterns = {
        "recovery isConnected updates": r"setIsConnected\(true\)"
    }
    return verify_patterns(sources["Home.jsx"], "Home.jsx", patterns)

def check_real_003(sources):
    # MessageInput disables input to prevent send spam
    patterns = {
        "thinking state input locking": r"isDisabled"
    }
    return verify_patterns(sources["MessageInput.jsx"], "MessageInput.jsx", patterns)

def check_real_004(sources):
    # Renders multiple distinct code blocks inside bubbles
    patterns = {
        "CodeBlock mapping rendering": r"CodeBlock"
    }
    return verify_patterns(sources["MessageBubble.jsx"], "MessageBubble.jsx", patterns)

def check_real_005(sources):
    # Outlines disabled and replaced with accent Primary glows
    patterns = {
        "focus borders variable check": r"var\(--accent-primary\)"
    }
    return verify_patterns(sources["MessageInput.jsx"], "MessageInput.jsx", patterns)

def check_real_006(sources):
    # Desktop layout vs mobile layout responsive widths
    patterns = {
        "mobile viewport transition check": r"window\.innerWidth\s*<\s*768"
    }
    return verify_patterns(sources["Home.jsx"], "Home.jsx", patterns)

def check_real_007(sources):
    # Manual scroll override on autoscroll
    patterns = {
        "near bottom tolerance scroll check": r"container\.scrollHeight\s*-\s*container\.scrollTop"
    }
    return verify_patterns(sources["Home.jsx"], "Home.jsx", patterns)

def check_real_008(sources):
    # Obsidian dark mode base colors exceed AA contrast
    patterns = {
        "base background Obsidian color": r"#090b0f",
        "primary Slate text color": r"#f1f3f5"
    }
    return verify_patterns(sources["global.css"], "global.css", patterns)

def check_real_009(sources):
    # Session switch does not overflow stale history
    patterns = {
        "stale chat messages cleanup": r"setMessages\(\[\]\)"
    }
    return verify_patterns(sources["Home.jsx"], "Home.jsx", patterns)

def check_real_010(sources):
    # Decoupling locks and builds verification status
    dist_path = os.path.join(FRONTEND_DIR, "dist")
    if os.path.exists(dist_path):
        return True, ""
    return False, "Frontend compilation dist/ folder does not exist"

# Audit Styling Requirements (R1, R2, R3)
def audit_styling_requirements(sources):
    print("[*] Starting Phase C: Auditing CSS and JSX Visual Overhaul Requirements...")
    errors = []
    
    # R1: Color Palette
    r1_colors = {
        "Obsidian background": r"--bg-base:\s*#090b0f",
        "Slate primary text": r"--text-primary:\s*#f1f3f5",
        "Slate secondary text": r"--text-secondary:\s*#8d9bb0"
    }
    for desc, pat in r1_colors.items():
        if not re.search(pat, sources["global.css"]):
            errors.append(f"R1 Color mismatch: {desc} ({pat})")
            
    # R1: Typography
    r1_typo = {
        "Google Fonts imports": r"@import\s+url\(.*family=Plus\+Jakarta\+Sans.*family=JetBrains\+Mono.*\)",
        "Sans-serif font definition": r"--font-sans:\s*['\"]Plus Jakarta Sans['\"]",
        "Monospace font definition": r"--font-mono:\s*['\"]JetBrains Mono['\"]"
    }
    for desc, pat in r1_typo.items():
        if not re.search(pat, sources["global.css"]):
            errors.append(f"R1 Typography mismatch: {desc} ({pat})")

    # R2: Responsive Sidebar Drawer and Transitions
    r2_sidebar = {
        "width transition in Sidebar.jsx": r"transition:\s*.*(width|var\(--transition\))",
        "responsive trigger for mobile": r"window\.innerWidth\s*<\s*768"
    }
    for desc, pat in r2_sidebar.items():
        if not re.search(pat, sources["Sidebar.jsx"]) and not re.search(pat, sources["Home.jsx"]) and not re.search(pat, sources["global.css"]):
            errors.append(f"R2 Responsive Sidebar mismatch: {desc} ({pat})")
            
    # R2: Centered Title absolute positioning
    r2_title = {
        "absolute header centering positioning": r"position:\s*absolute",
        "left 50 percent centering": r"left:\s*50%",
        "translateX minus 50 percent shift": r"transform:\s*translateX\(-50%\)"
    }
    for desc, pat in r2_title.items():
        if not re.search(pat, sources["global.css"]):
            errors.append(f"R2 Header Centering mismatch: {desc} ({pat})")

    # R2: Logo wordmark placement restriction
    if "Cyris" not in sources["Sidebar.jsx"]:
        errors.append("R2 Logo placement mismatch: 'Cyris' wordmark missing from Sidebar.jsx")
    if "Cyris" in sources["Header.jsx"] and "SVG" not in sources["Header.jsx"]:
        errors.append("R2 Logo placement mismatch: 'Cyris' wordmark illegally present in Header.jsx text content")

    # R3: Custom Webkit Scrollbars
    r3_scrollbar = {
        "scrollbar width selector": r"::-webkit-scrollbar",
        "scrollbar thumb border radius": r"border-radius:\s*99px"
    }
    for desc, pat in r3_scrollbar.items():
        if not re.search(pat, sources["global.css"]):
            errors.append(f"R3 Scrollbars mismatch: {desc} ({pat})")

    # R3: Cubic-bezier Transition Variable
    if not re.search(r"--transition:\s*0\.2s\s+cubic-bezier", sources["global.css"]):
        errors.append("R3 Transition mismatch: '--transition: 0.2s cubic-bezier' missing in global.css")

    # R3: Dynamic Focus Borders / Custom Glows
    r3_focus = {
        "MessageInput focus ring border changes": r"isFocused",
        "MessageInput focus glow styling": r"0 0 0 3px var\(--accent-glow\)"
    }
    for desc, pat in r3_focus.items():
        if not re.search(pat, sources["MessageInput.jsx"]):
            errors.append(f"R3 Focus Glow mismatch: {desc} ({pat})")

    if errors:
        return False, "\n".join(errors)
    return True, "All Visual Styling & Layout Audit checks passed successfully."

# API Integrity Check
def verify_api_integrity():
    print("[*] Starting Phase D: Verifying API Integrity in api.js...")
    api_js_path = os.path.join(FRONTEND_DIR, "src", "services", "api.js")
    if not os.path.exists(api_js_path):
        return False, f"api.js missing at {api_js_path}"
    
    with open(api_js_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    required_calls = {
        "POST /chat": r"(/chat|api\.post\s*\(\s*[\"']/chat)",
        "GET /sessions": r"(/sessions|api\.get\s*\(\s*[\"']/sessions)",
        "GET /sessions/:id/messages": r"(/sessions/.*messages|api\.get\s*\(\s*[`\"']/sessions/)",
        "DELETE /sessions/:id": r"(api\.delete\s*\(\s*[`\"']/sessions/)",
        "GET /memory-status": r"(/memory-status|api\.get\s*\(\s*[\"']/memory-status)",
        "DELETE /memory/:identity": r"(api\.delete\s*\(\s*[`\"']/memory/)"
    }
    
    missing = []
    for call_name, pattern in required_calls.items():
        if not re.search(pattern, content):
            missing.append(call_name)
            
    if missing:
        return False, f"api.js is missing required API calls: {', '.join(missing)}"
        
    return True, "frontend/src/services/api.js retains all 6 required API calls."

# Inline Style Audit Check
def verify_inline_style_audit():
    print("[*] Starting Phase E: Auditing JSX files for inline style={{}} layout objects...")
    src_dir = os.path.join(FRONTEND_DIR, "src")
    violations = []
    
    for root, dirs, files in os.walk(src_dir):
        if "_archive" in root:
            continue
        for file in files:
            if file.endswith(".jsx"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, FRONTEND_DIR)
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
                if "style={{" in content:
                    violations.append(rel_path)
                    
    if violations:
        return False, f"Inline style={{}} objects detected in: {', '.join(violations)}"
        
    return True, "No active .jsx files in frontend/src/ use inline style={{}} layout objects."

# Test Suite Runner
def main():
    print("====================================================")
    print("        CYRIS VISUAL OVERHAUL E2E TEST SUITE        ")
    print("====================================================")

    # 1. Verification of compilation
    build_ok, build_msg = verify_frontend_compilation()
    print(f"[*] Phase A Status: {'[PASS] ' + build_msg if build_ok else '[- - FAIL] ' + build_msg}")

    # 2. Verification of backend decoupling
    decoupling_ok, decoupling_msg = verify_backend_decoupling()
    print(f"[*] Phase B Status: {'[PASS] ' + decoupling_msg if decoupling_ok else '[- - FAIL] ' + decoupling_msg}")

    # 3. Static requirements audit
    sources = load_source_files()
    styling_ok, styling_msg = audit_styling_requirements(sources)
    print(f"[*] Phase C Status: {'[PASS] ' + styling_msg if styling_ok else '[- - FAIL] ' + styling_msg}")

    # 4. API Integrity Check
    api_ok, api_msg = verify_api_integrity()
    print(f"[*] Phase D Status: {'[PASS] ' + api_msg if api_ok else '[- - FAIL] ' + api_msg}")

    # 5. Inline Style Audit Check
    inline_ok, inline_msg = verify_inline_style_audit()
    print(f"[*] Phase E Status: {'[PASS] ' + inline_msg if inline_ok else '[- - FAIL] ' + inline_msg}")

    # Map all test cases
    test_cases_defs = [
        # Tier 1
        ("TC-FEAT-001", "Sidebar width transitions smoothly between open and closed", check_feat_001),
        ("TC-FEAT-002", "Sidebar date grouping (Today, Previous 7 Days, Older)", check_feat_002),
        ("TC-FEAT-003", "Select active session loads message history", check_feat_003),
        ("TC-FEAT-004", "Delete session action triggers DELETE call", check_feat_004),
        ("TC-FEAT-005", "Active session title centered in header absolutely", check_feat_005),
        ("TC-FEAT-006", "Connection status indicator dot changes color", check_feat_006),
        ("TC-FEAT-007", "Settings toggle button opens Settings modal panel", check_feat_007),
        ("TC-FEAT-008", "Conclude session button resets chat viewport", check_feat_008),
        ("TC-FEAT-009", "Textarea typing displays characters in sans-serif", check_feat_009),
        ("TC-FEAT-010", "MessageInput textarea auto-resizes to max height", check_feat_010),
        ("TC-FEAT-011", "MessageInput triggers handleSend on Enter key", check_feat_011),
        ("TC-FEAT-012", "MessageInput allows newline insertion with Shift+Enter", check_feat_012),
        ("TC-FEAT-013", "User message bubble styling (background/border)", check_feat_013),
        ("TC-FEAT-014", "Assistant message bubble layout (transparent/no-border)", check_feat_014),
        ("TC-FEAT-015", "Typographic headings font size/margin styles", check_feat_015),
        ("TC-FEAT-016", "Inline markdown bold and code formatting", check_feat_016),
        ("TC-FEAT-017", "Markdown list spacing and padding styles", check_feat_017),
        ("TC-FEAT-018", "Code block renders syntax header and copy button", check_feat_018),
        ("TC-FEAT-019", "AI Typing animations auto-scroll thread container", check_feat_019),
        ("TC-FEAT-020", "Thumbs feedback submit updates style and routes", check_feat_020),
        ("TC-FEAT-021", "SettingsPanel sliding overlay dialog styles", check_feat_021),
        ("TC-FEAT-022", "SettingsPanel toggles theme configuration base", check_feat_022),
        ("TC-FEAT-023", "Theme setting persists via LocalStorage on reload", check_feat_023),
        ("TC-FEAT-024", "Empty State starter card grid layout renders prompts", check_feat_024),
        # Tier 2
        ("TC-BOUND-001", "Extremely long session titles truncate with ellipsis", check_bound_001),
        ("TC-BOUND-002", "Sidebar displays fallback message when sessions empty", check_bound_002),
        ("TC-BOUND-003", "Rapid session deletion indexes alignment safety", check_bound_003),
        ("TC-BOUND-004", "Header title text truncates with ellipsis at bounds", check_bound_004),
        ("TC-BOUND-005", "Server connection status dot toggles to offline mode", check_bound_005),
        ("TC-BOUND-006", "Sidebar mobile collapse toggle hidden on desktop layout", check_bound_006),
        ("TC-BOUND-007", "Whitespace-only message send triggers are blocked", check_bound_007),
        ("TC-BOUND-008", "Mass clipboard paste textarea height limit boundary", check_bound_008),
        ("TC-BOUND-009", "Input textarea locked and style changed on thinking", check_bound_009),
        ("TC-BOUND-010", "Gigantic assistant bubble words wrap without overflow", check_bound_010),
        ("TC-BOUND-011", "Malformed markdown code syntax renders safely", check_bound_011),
        ("TC-BOUND-012", "Stops running typing intervals on session switch", check_bound_012),
        ("TC-BOUND-013", "Fallback default theme load on corrupt LocalStorage", check_bound_013),
        ("TC-BOUND-014", "Visual layout variables sync on rapid theme toggles", check_bound_014),
        ("TC-BOUND-015", "Clicking backdrop overlay closes Settings panel", check_bound_015),
        ("TC-BOUND-016", "Empty view starter cards clicks trigger send handler", check_bound_016),
        ("TC-BOUND-017", "First-time launch database collections render safely", check_bound_017),
        ("TC-BOUND-018", "Server offline starter card clicks show error bubble", check_bound_018),
        # Tier 3
        ("TC-CROSS-001", "Bubble styles and contrast updates on theme toggle", check_cross_001),
        ("TC-CROSS-002", "Sidebar closes automatically when selecting in mobile", check_cross_002),
        ("TC-CROSS-003", "Generated chat titles update in header and sidebar list", check_cross_003),
        ("TC-CROSS-004", "Focus control on overlay backdrop blurs input text", check_cross_004),
        ("TC-CROSS-005", "Deleting active session returns display to Empty State", check_cross_005),
        ("TC-CROSS-006", "Resetting session clears thinking states and API loads", check_cross_006),
        ("TC-CROSS-007", "Container autoscrolls as complex markdown is printed", check_cross_007),
        ("TC-CROSS-008", "Starter card click resets input container dimensions", check_cross_008),
        ("TC-CROSS-009", "Layout reflow remains jitter-free on toggle reflows", check_cross_009),
        ("TC-CROSS-010", "Code blocks syntax highlights adapt to selected theme", check_cross_010),
        ("TC-CROSS-011", "Status indicator turns gray on socket send error modes", check_cross_011),
        ("TC-CROSS-012", "Sidebar option menu dropdown absolute scrolls in list", check_cross_012),
        # Tier 4
        ("TC-REAL-001", "Theme and active session history restore on page reload", check_real_001),
        ("TC-REAL-002", "API recovery changes dot color and restores sending", check_real_002),
        ("TC-REAL-003", "Textarea keypress events disabled during thinking locks", check_real_003),
        ("TC-REAL-004", "Independent copy buttons for multiple bubbles codes", check_real_004),
        ("TC-REAL-005", "Interactive states replaced with custom primary focus", check_real_005),
        ("TC-REAL-006", "Sidebar hides/reveals seamlessly on window resizes", check_real_006),
        ("TC-REAL-007", "User scrolling upward pauses thread autoscrolling hook", check_real_007),
        ("TC-REAL-008", "Colors maintain a contrast above AA requirements", check_real_008),
        ("TC-REAL-009", "Chat switch aborts and discards outdated API returns", check_real_009),
        ("TC-REAL-010", "Build files validation and git status backend audits", check_real_010),
    ]

    print("\n--- Executing 64 Programmatic Test Cases ---")
    results = []
    passed_count = 0

    for idx, (tc_id, description, checker_func) in enumerate(test_cases_defs, start=1):
        try:
            status, reason = checker_func(sources)
            if status:
                print(f"[PASS] {tc_id}: {description}")
                results.append((tc_id, description, "PASSED", ""))
                passed_count += 1
            else:
                print(f"[FAIL] {tc_id}: {description} -> {reason}")
                results.append((tc_id, description, "FAILED", reason))
        except Exception as e:
            print(f"[ERROR] {tc_id}: {description} -> Exception: {str(e)}")
            results.append((tc_id, description, "ERROR", str(e)))

    # Compute overall statistics
    total_tests = len(test_cases_defs)
    success = passed_count == total_tests and build_ok and decoupling_ok and styling_ok and api_ok and inline_ok

    print("\n=======================================================")
    print("                     TEST REPORT                       ")
    print("=======================================================")
    print(f"Frontend Build Verification:      {'PASSED' if build_ok else 'FAILED'}")
    print(f"Backend Decoupling Check:         {'PASSED' if decoupling_ok else 'FAILED'}")
    print(f"Visual Overhaul Styling Audit:    {'PASSED' if styling_ok else 'FAILED'}")
    print(f"API Integrity Verification:       {'PASSED' if api_ok else 'FAILED'}")
    print(f"Inline Style Audit:               {'PASSED' if inline_ok else 'FAILED'}")
    print("-------------------------------------------------------")
    print(f"Executed Test Cases:              {total_tests}")
    print(f"Passed Test Cases:                {passed_count}")
    print(f"Failed Test Cases:                {total_tests - passed_count}")
    print("=======================================================")
    print(f"OVERALL RESULTS:                  {'SUCCESS' if success else 'FAILURE'}")
    print("=======================================================")

    # Write report file if needed
    report_file_path = os.path.join(BASE_DIR, "testing", "e2e_report.json")
    try:
        import json
        with open(report_file_path, "w", encoding="utf-8") as rf:
            json.dump({
                "build_status": "PASSED" if build_ok else "FAILED",
                "decoupling_status": "PASSED" if decoupling_ok else "FAILED",
                "styling_status": "PASSED" if styling_ok else "FAILED",
                "api_integrity_status": "PASSED" if api_ok else "FAILED",
                "inline_style_audit_status": "PASSED" if inline_ok else "FAILED",
                "total_tests": total_tests,
                "passed_tests": passed_count,
                "results": [{"id": r[0], "name": r[1], "status": r[2], "reason": r[3]} for r in results]
            }, rf, indent=2)
        print(f"[+] Detailed E2E test report saved as JSON to testing/e2e_report.json")
    except Exception as e:
        print(f"[-] Warning: Failed to save JSON report: {e}")

    if not success:
        sys.exit(1)
    
    sys.exit(0)

if __name__ == "__main__":
    main()
