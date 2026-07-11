---
name: smart_git_commits
description: "Comprehensive guidelines for writing clean, high-level Git commit messages, utilizing conventional commits, and handling trivial file changes."
---

# Smart Git Commits Etiquette

This skill governs the behavior for creating Git commits. A well-crafted Git commit message is the best way to communicate context about a change to other developers (and future AI agents). A diff will tell you *what* changed, but only the commit message can properly tell you *why*.

When asked to commit changes to a repository, you MUST adhere strictly to the following comprehensive guidelines.

## 1. Core Philosophy

* **Focus on the Big Picture**: Commit messages must summarize the core architectural upgrades, feature implementations, or major bug fixes.
* **Ignore the Trivial in the Message**: Do NOT mention minor, one-off cleanups in the commit message. If a commit contains a major feature alongside trivial cleanups (e.g., deleting temporary test files, moving a scratch script, fixing whitespace, correcting a typo in a comment), **omit the trivial changes from the commit message entirely**. The diff will show them, but they do not belong in the high-level summary.
* **Keep it Professional**: Avoid overly verbose, emotional, or "lame" descriptions. Use clear, objective, and actionable language.

## 2. Conventional Commits Specification

All commit messages must follow the Conventional Commits specification. This provides a lightweight convention on top of commit messages, creating an explicit history.

### Format
```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Allowed Types

* **`feat`**: A new feature (e.g., adding a new endpoint, a new UI component).
* **`fix`**: A bug fix.
* **`docs`**: Documentation only changes.
* **`style`**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc).
* **`refactor`**: A code change that neither fixes a bug nor adds a feature (e.g., renaming variables, extracting functions).
* **`perf`**: A code change that improves performance.
* **`test`**: Adding missing tests or correcting existing tests.
* **`build`**: Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm).
* **`ci`**: Changes to our CI configuration files and scripts.
* **`chore`**: Other changes that don't modify `src` or `test` files (e.g., updating dependencies, moving one-off scripts).

## 3. The Seven Rules of a Great Commit Message

When writing the `<description>` and `[optional body]`, follow these seven rules:

1. **Separate subject from body with a blank line**: If the commit requires a body for further explanation, it must be separated from the subject line by a single blank line.
2. **Limit the subject line to 50 characters**: This forces you to be concise and think about what the commit actually does. (If you're having trouble summarizing it in 50 characters, you might be committing too many things at once).
3. **Capitalize the subject line**: Begin the `<description>` with a capital letter. (Note: the `<type>` should be lowercase). Example: `feat: Add user authentication system`.
4. **Do not end the subject line with a period**: Space is precious in the subject line.
5. **Use the imperative mood in the subject line**: A properly formed Git commit subject line should always be able to complete the following sentence: *If applied, this commit will `<your subject line here>`*.
    * *Good*: `feat: Add login endpoint`
    * *Bad*: `feat: Added login endpoint`
    * *Bad*: `feat: Adding login endpoint`
6. **Wrap the body at 72 characters**: Git never wraps text automatically. When you write a body, you must wrap it manually at 72 characters to ensure it renders nicely in all tools.
7. **Use the body to explain what and why vs. how**: The body should focus on the *why* of the change (the context before the change, and why this approach was taken). The *how* is usually visible in the code diff itself.

## 4. Examples of Good vs. Bad Commits

### Example 1: Feature Implementation with Trivial Cleanup

You implemented a new PostgreSQL migration script, added a new vector memory service, and also deleted a temporary `test_script.py` you used for debugging.

**BAD (Too verbose, mentions trivial cleanup):**
```text
feat: migrated to postgres and added vector memory and deleted test_script.py

I added a new migration script to move our data to postgres. I also created a vector memory service using pgvector. While I was at it, I deleted the test_script.py because we don't need it anymore.
```

**GOOD (Focuses on the big picture, uses imperative mood):**
```text
feat: Migrate database to PostgreSQL and implement semantic memory

- Set up PostgreSQL connection in db.py using psycopg2
- Implement VectorMemoryService for semantic search via pgvector
- Integrate context injection into Gemini and Groq AI clients
```
*(Notice how the deletion of `test_script.py` is entirely omitted from the message).*

### Example 2: Simple Bug Fix

**BAD:**
```text
fix: Fixed the bug where the UI crashed when clicking conclude
```

**GOOD:**
```text
fix: Prevent UI crash on session conclusion

Check if the session object exists before attempting to clear
the context state in Header.jsx.
```

## 5. Execution Workflow

When instructed to commit changes, you will:
1. Run `git status` to review the staged and unstaged changes.
2. Group logical changes together mentally.
3. Identify the core feature, fix, or refactor.
4. Identify any trivial files (scratch scripts, temporary data, etc.) that were modified or deleted.
5. Formulate a commit message that adheres to the rules above, deliberately omitting any mention of the trivial files.
6. Execute the commit using `git commit -m "<subject>" -m "<body>"`.
