# Phase 18 — Behavioral Understanding & Mood Awareness

## Objective

Deliver the first implementation of Cyris's Emotional Intelligence and Behavioral Learning Engine by dynamically observing and classifying the user's emotional tone, energy level, and recurring behavioral/energy patterns from their conversations, persisting them chronologically, and adapting the system's tone and welcome greetings accordingly.

---

# Backend Progress

## 1. Valid Continuity Types & Keyword Gate Expansion
- **New Continuity Types**: Added `mood_signal`, `behavioral_pattern`, and `energy_pattern` to the valid extraction categories inside [continuity_ai_extractor.py](file:///c:/Developer_Workspace/active_projects/AI-Projects/cyris-ai-assistant/backend/app/services/ai/continuity_ai_extractor.py) along with detailed instruction guidelines.
- **Rule-Based Filter Expansion**: Added emotional, mood, energy, and behavioral signal keywords to `CONTINUITY_TOPICS` inside [continuity_extractor.py](file:///c:/Developer_Workspace/active_projects/AI-Projects/cyris-ai-assistant/backend/app/memory/continuity_extractor.py) to prevent the pre-filter gate from blocking these signals.
- **Priority Rules**: Configured base priorities for the new categories in [continuity_memory_service.py](file:///c:/Developer_Workspace/active_projects/AI-Projects/cyris-ai-assistant/backend/app/memory/continuity_memory_service.py):
  - `"mood_signal": 2`
  - `"behavioral_pattern": 3`
  - `"energy_pattern": 2`

## 2. Behavioral Signals Database Table
- **Schema Creation**: Initialized the `behavioral_signals` table in [db.py](file:///c:/Developer_Workspace/active_projects/AI-Projects/cyris-ai-assistant/backend/app/db.py) to store timestamped mood/energy observations over time:
  ```sql
  CREATE TABLE IF NOT EXISTS behavioral_signals (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      signal_type TEXT NOT NULL,
      signal_value TEXT NOT NULL,
      context TEXT,
      created_at TEXT NOT NULL
  )
  ```

## 3. Mood Classification Service
- **Classification Engine**: Created [mood_classifier.py](file:///c:/Developer_Workspace/active_projects/AI-Projects/cyris-ai-assistant/backend/app/services/ai/mood_classifier.py) to analyze the last 5 messages, assessing the user's current mood (out of 12 valid moods) and energy levels (`high`, `medium`, `low`).
- **Non-Blocking Run**: Integrated the mood classifier into `save_continuity` in [continuity_memory_service.py](file:///c:/Developer_Workspace/active_projects/AI-Projects/cyris-ai-assistant/backend/app/memory/continuity_memory_service.py) to run non-blockingly at the end of the memory extraction background thread.
- **Noise Filtering**: Automatically discards `"neutral"` mood classifications to keep database storage free from conversational noise.

## 4. Tone Adaptation & System Prompt Wiring
- **Mood Context Builder**: Implemented `build_mood_context()` in [continuity_memory_service.py](file:///c:/Developer_Workspace/active_projects/AI-Projects/cyris-ai-assistant/backend/app/memory/continuity_memory_service.py) to retrieve the last 5 signals and identify behavioral trends (e.g. consistent stress/frustration or mixed patterns across sessions).
- **Prompt Wiring**: Wired the mood context into [gemini_client.py](file:///c:/Developer_Workspace/active_projects/AI-Projects/cyris-ai-assistant/backend/app/services/ai/gemini_client.py) and [groq_client.py](file:///c:/Developer_Workspace/active_projects/AI-Projects/cyris-ai-assistant/backend/app/services/ai/groq_client.py).
- **Adaptive Tone Guidelines**: Updated [system_prompt_manager.py](file:///c:/Developer_Workspace/active_projects/AI-Projects/cyris-ai-assistant/backend/app/services/ai/system_prompt_manager.py) to adapt responses subtly:
  - *Stressed/Frustrated/Overwhelmed*: More supportive, less directive, suggests smaller steps.
  - *High Energy/Motivated*: Ambitious suggestions, matches user's momentum.
  - *Low Energy*: Shorter, more focused, gentle suggestions.

## 5. Dynamic Session-Start Welcome Greetings
- **Tone-Aware Welcome**: Modified the `/session-start` welcome greeting generation inside [main.py](file:///c:/Developer_Workspace/active_projects/AI-Projects/cyris-ai-assistant/backend/app/main.py) to retrieve behavioral context and naturally adjust the warmth and energy of Cyris's opening messages without explicitly mentioning mood detection to the user.

---

# Current State

Cyris dynamically classifies and registers emotional/behavioral signals in SQLite, allowing the assistant's persona to subtly align with the user's mental/emotional state. These changes are stored chronologically to support long-term behavioral trend learning.

---

# Outcome

Phase 18 successfully delivered:
- Chronological logging of emotional and behavioral signals in SQLite.
- Seamless context injection and tone-adapting guidelines.
- Mood-aware dynamic greetings during session startups.
