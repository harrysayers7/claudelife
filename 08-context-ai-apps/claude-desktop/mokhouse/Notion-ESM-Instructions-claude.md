---
date created: Fri, 10 3rd 25, 8:59:27 am
date modified: Fri, 10 3rd 25, 9:32:01 am
relation:
  - "[[97-tags/Claude-desktop|Claude-desktop]]"
  - "[[ESM]]"
---
## ESM Notion Project Management Database

Use this uuid to interact with the "ESM Project (1)" in Notion:

1e64a17b-b7f0-8115-be90-000b4548a3a6


Ive listed the properties you should interact with - do not interact with any other properties in database if not listed below. Only fill in properties you have information on otherwise leave blank.
## Core Project Information

- **Name** (title): The project name/identifier ie XXXX, Coopers, Repco, Nintendo etc
- **Status** (status): Tracks project workflow stages with groups:
    - **To Do**: Current, New Project
    - **In Progress**: Submitted, PO Received, Awaiting PO, Invoiced (invoice has been sent)
    - **Complete**: Awarded (usually shown as "Usage fee" on a PO, it means my song was picked, Complete (use this tag if the song only used for "demo fee")
Mark Status property "Invoiced" when you complete stripe invoice duty whether a draft or finalised in stripe.

## Financial Properties

For obvious reasons do not touch formula properties.

- **Demo Fee** (number): Fee for demo submission (in AUD)
- **Award Fee** (or Usage fee) (number): Fee if project is awarded (in AUD) - used as a projection but only fi
- **Award (if won)** (number): Actual awarded amount (Usage Fee) (in AUD)

## Invoice & Payment Management

- **PO #** (text): Purchase Order number (fill this in from PO related to the project)
- **Invoice** (file): Invoice document attachment (fill this in based on stripe invoice number)


## Administrative

- **APRA** (select): Music rights tracking with options: Done, Not Done, Check - If the job is "awarded" then mark this as "Not Done"
