---
Done: true
today: true
follow up: false
this week: false
back burner: false
ASAP: false
type: Task
status:
relation:
description:
effort:
ai-assigned: true
ai-ignore: false
ai-ask: false
priority:
agent:
---
Create a issues system function

Will use id convention:
ID: 001

Need to create a slash command for creating and calling issues and maybe an auto detetction

For a little more context, the reason I have the issue call slash command is because often I have to restart Claude Code to verify whether a fix has actually worked, like when an MCP needs reconfiguring, but you can't see the changes until it's been restarted.  So I would use the call issue / command to pull the last or specified issue into the context for the new session.
### /issue-create

This Would create an issue with a new ID based on past id's to avoid duplication. Would need to have a log or something so you know what ID to give it
You then create a detailed issue report including what you attempted and the results, anything that would help an llm have full context so it doesn't try fixing the issue with the same approach and would try something new. Please suggest the best way we approach this workflow.

Issue should be created matching the yaml of the template 98-templates/issue. Add these properties to this command and also any other properties you see fit.

Oncw report created add to 01-area/claude-code/issues/ as a md files with relevant information in the yaml for optimal parsing


### /issue-call

This is the command i use when call on the issue. I would either use /issue-call with $ARGUMENTS or the id number ie 001

Ensure the LLM knows to read the yaml file for information. If you are unable to fix update the issue report with what you attempted and other relevant info

If you do fix the issue reply with a celebration 🎉🎉🎉 and report your fix in the same issue file at the bottom under ## SOLVED. Provide a short summary in the yaml of the fix
Add what you learnt in the lesson: property
Mark the "solved" property as true

Create a lesson file and add it to 04-resources/lessons-learnt folder. Also if you think its necessary  ask me if I would like this lesson added as a rule in claude.md of any other slash command that would be relevant. A good idea may be to add to the rule to the /create-issue command so when I use the command it will know to check those rules first so it can possibly fix before starting to debug etc

Maybe would be smart to add lesson to serena some how too? then the /create-issue command could also search serena before startin debug to check for solution from the past, what do you think?

---

Needs id
Also the call-issue command will call the last created issur and one complete will mark complete or if not will udate issue



type: issue
title: name of issue
ID: 001, 002 etc
category: mcp, hook, just whatever tool or script etc
relation: eg mokai etc
description:
related-files: files it relates
complete: true/false

 Also, any other properties you suggest that would ensure this file would be readable and provide optimal context.
lets discuss
