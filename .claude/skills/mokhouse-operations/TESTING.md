# MOK HOUSE Operations Skill - Testing Guide

## Activation Testing

### Test 1: Automatic Detection

**How to Test:**
1. Start a new Claude Code session (restart if currently running)
2. Ask: "How does the MOK HOUSE ESM submission workflow work?"
3. Claude should automatically load the skill and answer accurately

**Expected Behavior:**
- Claude recognizes "MOK HOUSE" and "ESM" as skill triggers
- Loads SKILL.md context automatically
- Provides accurate ESM workflow (Brief → Submission → Selection → Demo/Usage Fee)

**Success Criteria:**
✅ No manual context loading needed
✅ Accurate ESM workflow description
✅ Mentions demo fee ($250-$1k) and usage fee ($2.5k-$8k) ranges

---

### Test 2: Client Knowledge

**How to Test:**
Ask: "What was the Nintendo Exchange Mode project budget?"

**Expected Behavior:**
- Queries Graphiti for Nintendo project details
- Returns: Usage fee $3,250, Demo fee $650, Total $3,900
- Status: Paid Oct 17, 2025

**Success Criteria:**
✅ Accurate budget details
✅ Includes demo + usage fee breakdown
✅ References Graphiti knowledge if available

---

### Test 3: Team Context

**How to Test:**
Ask: "Who should I contact at ESM for a creative question?"

**Expected Behavior:**
- References team structure from SKILL.md
- Recommends: Glenn (Producer/Creative Director)
- Explains: Kate handles logistics, Glenn handles creative

**Success Criteria:**
✅ Correct contact (Glenn for creative)
✅ Explains role differences
✅ No need to search external files

---

### Test 4: Indigenous Positioning

**How to Test:**
Ask: "What's our Indigenous procurement advantage?"

**Expected Behavior:**
- References Indigenous positioning section
- Explains: 100% Indigenous-owned, Supply Nation pending
- Mentions: IPP eligibility, RAP target market

**Success Criteria:**
✅ Explains Indigenous ownership structure
✅ Mentions Supply Nation and IPP
✅ Describes procurement advantages

---

### Test 5: Shortcut Recognition

**How to Test:**
Ask: "What's the pricing for MH music projects?"

**Expected Behavior:**
- Recognizes "MH" = MOK HOUSE
- Provides pricing: $5k-$30k+ projects
- Breaks down: Demo fees, usage fees, project ranges

**Success Criteria:**
✅ Recognizes shortcut automatically
✅ Accurate pricing ranges
✅ Explains fee structure

---

### Test 6: Creative Patterns

**How to Test:**
Ask: "What creative approach works well for Nintendo?"

**Expected Behavior:**
- Queries Graphiti for Nintendo patterns
- References: Sweet, endearing, story-focused
- Explains: Japanese influences, heartwarming scores

**Success Criteria:**
✅ Retrieves client-specific patterns
✅ Quotes successful creative direction
✅ Explains why approach worked

---

## Integration Testing

### Test 7: Slash Command Compatibility

**How to Test:**
1. Run `/mokhouse-create-project`
2. Verify skill context is available during project creation

**Expected Behavior:**
- Skill provides team structure knowledge
- Project metadata standards applied
- Financial context available for pricing

**Success Criteria:**
✅ No context conflicts
✅ Skill enhances slash command execution
✅ Consistent metadata structure

---

### Test 8: Graphiti Learning

**How to Test:**
1. Say: "We won the ABC project because the client loved the upbeat tempo. Invoice #123 for $4,500."
2. Check if Graphiti captures the pattern

**Expected Behavior:**
- Skill detects project outcome information
- Automatically stores in Graphiti with group_id "mokhouse"
- Captures: Win reason, budget, invoice number

**Success Criteria:**
✅ Information stored without explicit instruction
✅ Proper Graphiti structure (episode, entities, facts)
✅ Retrievable in future conversations

---

### Test 9: Dashboard Integration

**How to Test:**
Ask: "What's our current financial status?"

**Expected Behavior:**
- References dashboard location from SKILL.md
- Reads `/01-areas/business/mokhouse/mokhouse-dashboard.md`
- Reports: Total Paid, Outstanding, Active Projects

**Success Criteria:**
✅ Knows dashboard location without asking
✅ Provides current financial snapshot
✅ Includes context from skill (what metrics mean)

---

### Test 10: Multi-Project Portability

**How to Test:**
1. Navigate to a different project directory (outside claudelife)
2. Ask: "What's the MOK HOUSE ESM workflow?"

**Expected Behavior:**
- Skill activates regardless of current directory
- Same accurate ESM workflow provided
- No dependency on being in claudelife folder

**Success Criteria:**
✅ Skill works from any directory
✅ Consistent knowledge across projects
✅ No manual context needed

---

## Performance Testing

### Test 11: Response Speed

**How to Test:**
Time how long it takes to answer: "Explain MOK HOUSE business model"

**Expected Behavior:**
- Skill loads quickly (under 2 seconds)
- Response is immediate after loading
- No noticeable delay vs. manual context loading

**Success Criteria:**
✅ Fast skill activation
✅ Comprehensive answer
✅ No performance degradation

---

### Test 12: Context Window Efficiency

**How to Test:**
1. Have a long conversation about MOK HOUSE
2. Check context usage
3. Verify skill doesn't dominate context window

**Expected Behavior:**
- Skill loads relevant sections only
- Not loading entire SKILL.md each turn
- Context usage is reasonable (~1,500-2,500 tokens upfront)

**Success Criteria:**
✅ Efficient context usage
✅ Long conversations possible
✅ No context overflow issues

---

## Error Handling

### Test 13: Partial Information Handling

**How to Test:**
Ask: "What was the XYZ project budget?" (non-existent project)

**Expected Behavior:**
- Skill acknowledges it doesn't have that project
- Suggests checking dashboard or project files
- Doesn't hallucinate data

**Success Criteria:**
✅ Honest about missing information
✅ Suggests where to find information
✅ No false data generation

---

### Test 14: Conflicting Information

**How to Test:**
Say: "Actually, the demo fee range is $100-$500" (incorrect info)

**Expected Behavior:**
- Skill recognizes conflict with stored knowledge
- Asks for clarification or confirms correction
- Updates knowledge if confirmed

**Success Criteria:**
✅ Detects conflicting information
✅ Seeks confirmation before updating
✅ Maintains data integrity

---

## Update Testing

### Test 15: Skill Modification

**How to Test:**
1. Edit SKILL.md (change a demo fee range)
2. Restart Claude Code
3. Verify new information is used

**Expected Behavior:**
- Updated SKILL.md loaded in new session
- New information reflected in answers
- Old information no longer used

**Success Criteria:**
✅ Updates take effect after restart
✅ Changes reflected accurately
✅ No cache issues

---

## Comprehensive Test Scenario

### Test 16: End-to-End Workflow

**Scenario:**
You receive a new brief from ESM for a Nintendo project.

**Test Steps:**
1. "I got a new Nintendo brief from ESM"
2. "What should I check in the brief?"
3. "Who do I contact if I have creative questions?"
4. "What creative approach worked last time for Nintendo?"
5. "Help me create a project file"
6. "If I win, what's the typical usage fee?"
7. "If I don't win, what do I get paid?"

**Expected Behavior:**
- Skill provides brief checklist guidance (Test 1)
- Recommends Glenn for creative questions (Test 3)
- References Nintendo patterns from Graphiti (Test 6)
- Uses project template from resources (Test 7)
- Explains usage fee range $2.5k-$8k (Test 5)
- Explains demo fee $250-$1k guaranteed (Test 2)

**Success Criteria:**
✅ Seamless end-to-end guidance
✅ All information accurate and contextual
✅ No repeated explanations needed
✅ Workflow feels natural and efficient

---

## Test Results Log

Use this section to track test results:

### Testing Session: [Date]

| Test # | Test Name | Status | Notes |
|--------|-----------|--------|-------|
| 1 | Automatic Detection | [ ] Pass / [ ] Fail | |
| 2 | Client Knowledge | [ ] Pass / [ ] Fail | |
| 3 | Team Context | [ ] Pass / [ ] Fail | |
| 4 | Indigenous Positioning | [ ] Pass / [ ] Fail | |
| 5 | Shortcut Recognition | [ ] Pass / [ ] Fail | |
| 6 | Creative Patterns | [ ] Pass / [ ] Fail | |
| 7 | Slash Command Compatibility | [ ] Pass / [ ] Fail | |
| 8 | Graphiti Learning | [ ] Pass / [ ] Fail | |
| 9 | Dashboard Integration | [ ] Pass / [ ] Fail | |
| 10 | Multi-Project Portability | [ ] Pass / [ ] Fail | |
| 11 | Response Speed | [ ] Pass / [ ] Fail | |
| 12 | Context Window Efficiency | [ ] Pass / [ ] Fail | |
| 13 | Partial Information | [ ] Pass / [ ] Fail | |
| 14 | Conflicting Information | [ ] Pass / [ ] Fail | |
| 15 | Skill Modification | [ ] Pass / [ ] Fail | |
| 16 | End-to-End Workflow | [ ] Pass / [ ] Fail | |

**Overall Status:** [ ] Ready for Production / [ ] Needs Refinement

**Issues Found:**
- [List any issues discovered during testing]

**Improvements Needed:**
- [List any improvements identified]

---

## Next Steps After Testing

1. ✅ All tests pass → Skill ready for daily use
2. ⚠️ Some tests fail → Refine SKILL.md and retest
3. 📝 Document any edge cases discovered
4. 🔄 Update skill based on real-world usage patterns
5. 📊 Monitor Graphiti for automatic learning quality
