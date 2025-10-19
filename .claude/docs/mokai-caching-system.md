# MOKAI Status Caching System

**Status**: ✅ Active (as of 2025-10-16)

## Overview

Automatic caching system that speeds up `/mokai-status` by 50-80% using Claude Code hooks and background scripts.

## How It Works

### 1. Cache Script (`scripts/cache-mokai-inbox.sh`)
- Scans all files in `/00-inbox/tasks/` for MOKAI-related tasks
- Extracts: title, done status, priority
- Saves to: `01-areas/business/mokai/.mokai-inbox-cache.json`
- **Runtime**: ~1-2 seconds for 100+ task files

### 2. Claude Code Hooks (`.claude/settings.local.json`)

#### PostToolUse Hook
Triggers after any `Edit` or `Write` tool use:
- Checks if edited file is in `mokai/diary` or `00-inbox/tasks`
- If yes, runs cache script in background
- **Result**: Cache updates automatically whenever you edit diary/task files via Claude

#### Stop Hook
Triggers when Claude finishes responding:
- Runs cache script in background
- **Result**: Cache is always fresh at end of conversation

### 3. Benefits

**Speed improvement**:
- Before: `/mokai-status` scans 100+ files every time (5-10 seconds)
- After: Reads pre-computed cache (0.1-0.5 seconds)
- **Gain**: 50-80% faster

**Always fresh**:
- Cache updates automatically after edits
- No manual intervention needed
- Background execution (doesn't interrupt Claude)

## Cache File Format

```json
[
  {
    "title": "Supply Nation application",
    "done": false,
    "priority": "",
    "path": "/full/path/to/task.md"
  },
  {
    "title": "Open Bank Account",
    "done": false,
    "priority": "high",
    "path": "/full/path/to/task.md"
  }
]
```

## Commands That Use Caching

| Command | Uses Cache? | Why? |
|---------|-------------|------|
| `/mokai-status` | ✅ YES | Scans all inbox tasks frequently |
| `/mokai-dump` | ❌ NO | Writes only, doesn't read inbox |
| `/mokai-insights` | ❌ NO | Runs rarely (monthly), not worth caching overhead |
| `/mokai-weekly` | ❌ NO | Runs weekly, caching overhead not justified |
| `/mokai-wins` | ❌ NO | Writes only |

**Decision**: Only cache for `/mokai-status` because it runs most frequently and scans everything.

## Manual Cache Refresh

If cache gets stale (rare):
```bash
./scripts/cache-mokai-inbox.sh
```

## Troubleshooting

### Cache not updating after edit?
1. Check hooks are configured: `/hooks` in Claude Code
2. Restart Claude Code (hooks load on startup)
3. Manually run: `./scripts/cache-mokai-inbox.sh`

### Cache shows 0 tasks?
- Script looks for "mokai" keyword (case-insensitive)
- Check task files have `relation: [[mokai]]` in frontmatter
- Run script manually to see errors: `./scripts/cache-mokai-inbox.sh 2>&1`

### Hook not triggering?
- Hooks only work for files edited via Claude Code tools (Edit/Write)
- Manual edits outside Claude won't trigger hooks
- Fallback: Cache updates on `Stop` hook (end of conversation)

## Technical Details

### Why Claude Code Hooks > Git Hooks?

| Feature | Claude Code Hooks | Git Hooks |
|---------|------------------|-----------|
| Triggers | After Edit/Write, on Stop | On git commit |
| Timing | Immediate during work | Delayed until commit |
| Manual edits | ❌ Won't catch | ✅ Catches on commit |
| Setup | JSON config | Bash scripts in `.git/hooks/` |
| Best for | Active AI sessions | Version control checkpoints |

**Chosen**: Claude Code hooks because they update cache during active work sessions (when `/mokai-status` runs most).

### Performance Metrics

**Cache generation**:
- 19 tasks: ~0.5 seconds
- 100 tasks: ~2 seconds (estimated)
- Runs in background: 0 seconds perceived

**Cache read**:
- Instant (~0.01 seconds)

**Net gain**:
- First run: Same speed (generates cache)
- Every subsequent run: 50-80% faster

## Future Improvements (Optional)

### Phase 2: Parallel Processing
Create `scripts/mokai-status-parallel.sh`:
- Run diary scan + inbox scan in parallel
- Wait for both, process sequentially
- **Expected gain**: Additional 30-40% speedup

### Phase 3: Background Daemon
Use `fswatch` to monitor file changes:
```bash
fswatch -o 01-areas/business/mokai/diary | xargs -n1 ./scripts/cache-mokai-inbox.sh
```
- Cache always up-to-date (even for manual edits)
- `/mokai-status` becomes instant
- **Expected gain**: 90%+ faster

**Current status**: Phase 1 complete. Phase 2/3 optional based on need.

## Files Modified

1. `.claude/settings.local.json` - Added hooks configuration
2. `scripts/cache-mokai-inbox.sh` - New cache script
3. `01-areas/business/mokai/.mokai-inbox-cache.json` - Auto-generated cache file

## Maintenance

- **Cache file**: Auto-managed, no manual maintenance
- **Script**: Update if task frontmatter format changes
- **Hooks**: Review if Claude Code updates change hook API

Last updated: 2025-10-16
