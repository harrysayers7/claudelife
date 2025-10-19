# Context7 Smart Detection Hook

## Overview

The Context7 detector hook analyzes your prompts in real-time to intelligently suggest when to use Context7 MCP for retrieving up-to-date library documentation. It runs on every message you send to Claude Code.

## What is Context7?

Context7 is an MCP server that provides **version-specific, up-to-date documentation** directly from source repositories. Unlike LLMs trained on outdated data, Context7:

- ✅ Pulls latest documentation from official sources
- ✅ Provides version-specific API references
- ✅ Includes current code examples
- ✅ Eliminates hallucinated/deprecated APIs
- ✅ Filters docs by topic (routing, validation, etc.)

## How the Detector Works

### Detection Logic

The hook uses a **multi-factor confidence scoring system**:

#### 1. **Library Detection** (40% weight)
Identifies mentions of:

**Fast-Moving Frameworks** (high value):
- Next.js, React Query, TanStack Query
- Tailwind CSS, Zod, tRPC
- Trigger.dev, Prisma, Drizzle
- Shadcn, Radix UI, Lucia Auth

**Complex API Libraries**:
- FastAPI, SQLAlchemy, Pydantic
- Playwright, Puppeteer
- Stripe, Supabase
- OpenAI, Anthropic, LangChain

#### 2. **Version Sensitivity** (30% weight)
Detects patterns like:
- "new [feature/function/API]"
- "latest [library]"
- "how does X.method work?"
- Package version mentions (`@package/name@1.2.3`)
- "upgraded to", "version X"
- "breaking change", "migration"

#### 3. **Documentation Signals** (30% weight)
Catches phrases like:
- "how do I", "how to", "what is"
- "example", "documentation", "docs"
- "api reference", "usage"
- "implement", "integrate"
- "getting started", "tutorial"

### Confidence Scoring

| Confidence | Threshold | Action |
|------------|-----------|--------|
| **0.8+** | High | 🎯 Strong recommendation with specific usage suggestion |
| **0.65-0.79** | Medium-High | 📚 Gentle suggestion to consider Context7 |
| **0.50-0.64** | Medium | 💡 Subtle hint displayed |
| **<0.50** | Low | No suggestion shown |

### Smart Filtering

**Excluded** (won't trigger suggestions):
- Stable languages: JavaScript, Python, TypeScript, HTML, CSS, SQL
- Generic programming concepts
- Architecture discussions
- Questions about your own codebase
- Prompts already containing "context7"

## Example Triggers

### High Confidence (≥0.8)

**Example 1:**
```
How do I use the new Next.js after() function?
```
**Detection:**
- Library: Next.js (fast-moving) ✅
- Version sensitivity: "new ... function" ✅
- Documentation need: "how do I" ✅
- **Confidence: 0.9**

**Output:**
```
🎯 Detected next.js - Context7 highly recommended for latest docs
⚡ Version-specific query detected - use Context7 for accurate API info
💡 Suggested: Add 'use context7' to get current next.js documentation
```

**Example 2:**
```
Implement authentication with Lucia Auth using the latest version
```
**Detection:**
- Library: Lucia Auth (fast-moving) ✅
- Version sensitivity: "latest version" ✅
- Documentation need: "implement" ✅
- **Confidence: 0.85**

### Medium-High Confidence (0.65-0.79)

**Example 3:**
```
How does Prisma's interactive transactions API work?
```
**Detection:**
- Library: Prisma (complex API) ✅
- Documentation need: "how does ... work" ✅
- **Confidence: 0.7**

**Output:**
```
📚 Consider using Context7 for up-to-date prisma documentation
💡 Add 'use context7' to your prompt for current API references
```

### Low Confidence (<0.5) - No Suggestion

**Example 4:**
```
What's the difference between async and sync in Python?
```
**Detection:**
- No specific libraries detected
- Generic programming concept
- **Confidence: 0.3**
- **No suggestion shown**

## Hook Configuration

### Location
```
.claude/hooks/context7_detector.py
```

### Settings Entry
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/context7_detector.py"
          }
        ]
      }
    ]
  }
}
```

### Requirements
- Python 3.6+
- No external dependencies (uses stdlib only)
- Executable permissions: `chmod +x .claude/hooks/context7_detector.py`

## Customization

### Adding Libraries

Edit `context7_detector.py` to add libraries:

```python
# Fast-moving frameworks
FAST_MOVING_LIBS = {
    "next.js", "nextjs",
    "your-framework-here",  # Add new framework
}

# Complex API libraries
COMPLEX_API_LIBS = {
    "fastapi", "sqlalchemy",
    "your-library-here",  # Add new library
}
```

### Adjusting Confidence Thresholds

```python
# In generate_reminder()
if confidence >= 0.8:      # Change high-confidence threshold
    # Strong recommendation
elif confidence >= 0.65:   # Change medium-high threshold
    # Gentle suggestion
```

### Custom Patterns

Add detection patterns:

```python
VERSION_PATTERNS = {
    r"your_custom_pattern",
    r"another_pattern"
}

DOCUMENTATION_SIGNALS = {
    "your custom signal",
    "another signal"
}
```

## Testing the Hook

### Manual Testing

```bash
# Test with different prompts
python3 .claude/hooks/context7_detector.py "How do I use Next.js after function?"
python3 .claude/hooks/context7_detector.py "What is a variable in Python?"

# Check JSON output format
python3 .claude/hooks/context7_detector.py "Implement Stripe checkout with latest API" | jq
```

### Expected Output Format

```json
{
  "reminders": [
    "🎯 Detected stripe - Context7 highly recommended for latest docs",
    "⚡ Version-specific query detected - use Context7 for accurate API info",
    "💡 Suggested: Add 'use context7' to get current stripe documentation"
  ],
  "metadata": {
    "detected_libraries": ["stripe"],
    "confidence": 0.85,
    "version_sensitive": true
  }
}
```

## Performance

- **Execution Time**: <50ms typical
- **Impact**: Minimal (runs before prompt processing)
- **Blocking**: Non-blocking unless exit code != 0
- **Caching**: No external API calls, pure text analysis

## Troubleshooting

### Hook Not Triggering

1. **Check hook is enabled:**
   ```bash
   cat .claude/settings.json | grep -A 10 "UserPromptSubmit"
   ```

2. **Verify executable permissions:**
   ```bash
   ls -la .claude/hooks/context7_detector.py
   # Should show: -rwxr-xr-x
   ```

3. **Test manually:**
   ```bash
   python3 .claude/hooks/context7_detector.py "test prompt"
   echo $?  # Should be 0
   ```

### False Positives

If getting too many suggestions:

1. **Increase confidence threshold** in `generate_reminder()`
2. **Add exclusions** to `STABLE_LIBS`
3. **Reduce pattern weights** in `calculate_confidence()`

### False Negatives

If missing important cases:

1. **Add libraries** to detection sets
2. **Add patterns** to detection regexes
3. **Lower confidence threshold**
4. **Check library name variations** (e.g., "nextjs" vs "next.js")

## Integration with Context7 MCP

### Using Context7 in Your Prompts

When the hook suggests Context7:

**Before:**
```
How do I use Zod's transform function?
```

**After (with suggestion):**
```
How do I use Zod's transform function? use context7
```

### Context7 Workflow

1. Hook detects library mention
2. Suggests adding "use context7"
3. You add the phrase to your prompt
4. Context7 MCP:
   - Resolves library name → Context7 ID
   - Fetches latest documentation
   - Filters by topic
   - Injects into Claude's context
5. Claude responds with current, accurate information

### MCP Tools Available

```javascript
// Resolve library name to Context7 ID
mcp__context7__resolve-library-id({
  libraryName: "fastapi"
})
// Returns: "/tiangolo/fastapi"

// Get documentation
mcp__context7__get-library-docs({
  context7CompatibleLibraryID: "/tiangolo/fastapi",
  topic: "authentication",  // Optional filter
  tokens: 10000            // Max tokens to retrieve
})
```

## Best Practices

### When to Follow Hook Suggestions

✅ **Do use Context7 when:**
- Working with fast-moving frameworks
- Need latest API documentation
- Implementing new features
- Debugging version-specific issues
- Learning unfamiliar libraries
- Production code generation

❌ **Don't need Context7 when:**
- Discussing architecture
- Generic programming concepts
- Stable, well-known APIs
- Questions about your own code

### Prompt Enhancement Tips

**Good prompts for Context7:**
```
✅ "How do I use the new Next.js after() function? use context7"
✅ "Implement Stripe checkout with latest API use context7"
✅ "What's the correct way to validate with Zod? use context7"
```

**Less effective:**
```
❌ "How do I code?" (too vague)
❌ "Best practices" (no specific library)
❌ "Python basics" (stable, no specific library)
```

## Advanced Configuration

### Multi-Library Detection

The hook can detect multiple libraries and suggest the primary one:

```
Prompt: "Build a Next.js app with Prisma and tRPC"

Detection:
- next.js ✅
- prisma ✅
- trpc ✅

Suggestion: "Add 'use context7' to get current next.js documentation"
(Primary = first alphabetically, but all detected in metadata)
```

### Custom Confidence Boosters

Add boost conditions in `calculate_confidence()`:

```python
# Boost for "migrate" or "upgrade"
if "migrate" in text_lower or "upgrade" in text_lower:
    score += 0.2

# Boost for error messages
if "error" in text_lower and libraries:
    score += 0.15
```

## Metrics & Analytics

Hook outputs metadata for tracking:

```json
{
  "metadata": {
    "detected_libraries": ["fastapi", "pydantic"],
    "confidence": 0.75,
    "version_sensitive": true
  }
}
```

Use this to:
- Track which libraries are frequently queried
- Tune confidence thresholds
- Identify missing library patterns
- Measure suggestion acceptance rate

## Related Documentation

- [Context7 Official Docs](https://upstash.com/blog/context7-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Claude Code Hooks Guide](https://docs.claude.com/en/docs/claude-code/hooks)
- [MCP Integration in Claude Code](https://docs.claude.com/en/docs/claude-code/mcp)

## Contributing

Found a library that should be detected? Want to improve detection logic?

1. Edit `context7_detector.py`
2. Add library to appropriate set
3. Test with relevant prompts
4. Update this README with examples

---

**Version**: 1.0.0
**Last Updated**: 2025-10-16
**Author**: Claude Code + Context7 Research
