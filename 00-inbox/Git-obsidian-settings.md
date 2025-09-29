---
tags:
description:
date: "2025-09-29 15:39"
---
 Core Settings

  - Auto commit-and-sync interval: 20-30 minutes
  (not too frequent)
  - Auto commit-and-sync after stopping file
  edits: ✅ ON (prevents conflicts while editing)
  - Auto commit-and-sync after latest commit: ✅
  ON (works well with Claude Code commits)

  Push/Pull Settings

  - Auto push interval: 0 (disabled - let
  commit-and-sync handle it)
  - Auto pull interval: 5-10 minutes (frequent
  pulls to catch Claude Code changes)
  - Pull on startup: ✅ ON
  - Push on commit-and-sync: ✅ ON
  - Pull on commit-and-sync: ✅ ON

  Commit Messages

  - Commit message on auto commit-and-sync:
  vault: {{date}} - {{numFiles}} files
  - Merge strategy: Merge (handles conflicts
  better than rebase)

  Why These Settings Work

  1. 20-30 min intervals give you time to do
  Claude Code work without interruption
  2. After stopping edits prevents commits while
  you're actively writing
  3. Frequent pulls catch Claude Code commits
  quickly
  4. Descriptive commit messages distinguish
  vault changes from code changes

  Alternative: Manual Control

  If you want more control:
  - Set all intervals to 0 (disabled)
  - Use Obsidian's manual "Commit and Sync"
  button when needed
  - Pull manually before starting work sessions

  This gives you complete control but requires
  remembering to sync.

  Which approach do you prefer - automated with
  these settings, or manual control?











##### References:
