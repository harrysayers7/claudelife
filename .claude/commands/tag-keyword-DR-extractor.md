# /tag-keyword-DR-extractor

Scan markdown files in claudelife/ for frontmatter containing `research-type: deep research` and intelligently extract keywords and tags for RAG optimization.

## Steps

1. **Find Deep Research Files**
   - Search all `.md` files in `/Users/harrysayers/Developer/claudelife/`
   - Filter for files with frontmatter property containing `research-type` with value matching "deep research" (case-insensitive)
   - Handle both formats:
     - Single value: `research-type: deep research` or `research-type: Deep research`
     - Array format: `research-type:\n  - Deep research` or `research-type: [Deep research]`
   - Use Serena's `search_for_pattern` tool with pattern: `research-type[\s\S]{0,20}[Dd]eep\s+research`
   - List all matching files for processing

2. **Extract Keywords (5-7 optimal)**
   - Analyze file content to extract **5-7 keywords** maximum
   - Prioritize specificity over generality
   - Focus on: technical terms, proper nouns, key concepts, domain-specific language
   - These keywords optimize RAG retrieval and semantic search
   - Add to frontmatter property: `keywords: [keyword1, keyword2, ...]`

   **Why 5-7?**
   - Fewer than 5 = insufficient retrieval pathways
   - More than 7 = keyword dilution, diminishing returns on token efficiency
   - Sweet spot for embedding similarity without noise

3. **Add Tags (3-5 recommended)**
   - Extract **3-5 tags** that create connections across the vault
   - **Prioritize existing tags** from other files' `tags` or `relations` properties
   - Tag hierarchy: **domain → type → context**

   **Tag discovery priority:**
   1. Check `relations` property for connection hints (mokai, mok-house, etc.)
   2. Scan existing vault tags for pattern matches
   3. Only create new tags if they establish valuable new pathways

   **Tag types to consider:**
   - Domain: `#music-production`, `#cybersecurity`, `#business`, `#health`
   - Type: `#project`, `#resource`, `#insight`, `#workflow`, `#deep-research`
   - Context: Entity names, tools, techniques, locations

4. **Add Description (1-2 sentences)**
   - Generate a concise description summarizing the document's content
   - Maximum **1-2 sentences** that capture the core purpose/findings
   - Add to frontmatter property: `description: "Brief summary here"`
   - If description already exists, preserve it unless it's generic/unhelpful

5. **Update Frontmatter Structure**
   ```yaml
   ---
   research-type: deep research
   keywords: [keyword1, keyword2, keyword3, keyword4, keyword5]
   tags: [domain-tag, type-tag, context-tag]
   description: "Concise 1-2 sentence summary of document content and purpose"
   relations: [existing-relation-1, existing-relation-2]
   date created: [existing]
   date modified: [auto-update]
   ---
   ```

6. **Preserve Existing Data**
   - Never remove existing frontmatter properties
   - Append to existing `tags` or `relations` arrays
   - Only add `keywords` if missing
   - Add `description` if missing or unhelpful
   - Update `date modified` timestamp

7. **Report Summary**
   - List all files processed
   - Show keywords, tags, and descriptions added to each file
   - Highlight any new tags created vs existing tags reused
   - Note any files skipped (e.g., already has keywords)
   - Include count of descriptions added

## Example Usage

```bash
/tag-keyword-DR-extractor
```

**Example Output:**
```
Processed 3 deep research files:

1. mokai/docs/research/cybersecurity-landscape.md
   Keywords: [IRAP, Essential8, ASD, penetration-testing, compliance-framework]
   Tags: [#cybersecurity, #deep-research, #mokai] (2 existing, 1 new)
   Description: "Analysis of Australian government cybersecurity procurement landscape and compliance requirements"

2. mok-music/resources/audio-plugin-design.md
   Keywords: [VST3, JUCE, DSP, audio-processing, Max-for-Live]
   Tags: [#music-production, #deep-research, #mok-music] (all existing)
   Description: "Comprehensive guide to designing and developing professional audio plugins for DAWs"

3. health/fitness/strength-training-principles.md
   Keywords: [progressive-overload, hypertrophy, periodization, recovery, volume]
   Tags: [#health, #deep-research, #fitness] (all existing)
   Description: (already exists)

Summary: 15 keywords added, 9 tags added (7 existing, 2 new), 2 descriptions added
```

## Notes

- **RAG Optimization**: Keywords are designed for semantic search and vector embedding retrieval
- **Tag Reuse**: Prioritize existing tags to strengthen vault graph connections
- **Specificity**: Keywords should be specific enough to uniquely identify content, general enough to connect related documents
- **Dry Run**: Can add `--dry-run` flag to preview changes without modifying files
- **Batch Processing**: Processes all matching files in one command execution
