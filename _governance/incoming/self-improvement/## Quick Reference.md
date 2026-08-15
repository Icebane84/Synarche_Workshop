# Self-Improvement Quick Reference

| Situation                   | Action                                                                        |
| --------------------------- | ----------------------------------------------------------------------------- |
| Command/operation fails     | Log to `.learnings/ERRORS.md`                                                 |
| User corrects you           | Log to `.learnings/LEARNINGS.md` with category `correction`                   |
| User wants missing feature  | Log to `.learnings/FEATURE_REQUESTS.md`                                       |
| API/external tool fails     | Log to `.learnings/ERRORS.md` with integration details                        |
| Knowledge was outdated      | Log to `.learnings/LEARNINGS.md` with category `knowledge_gap`                |
| Found better approach       | Log to `.learnings/LEARNINGS.md` with category `best_practice`                |
| Similar to existing entry   | Link with `**See Also**`, consider priority bump                              |
| Broadly applicable learning | Promote to `CLAUDE.md`, `AGENTS.md`, and/or `.github/copilot-instructions.md` |

## Setup

Create `.learnings/` directory in project root if it doesn't exist:

```bash
mkdir -p .learnings
```

Copy templates from `assets/` or create files with headers.
