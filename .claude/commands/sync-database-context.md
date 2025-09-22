Sync database context files to reflect current Supabase schema.

Steps:
1. Run the schema sync script: `npm run sync-context`
2. Check for any `.memory-capture-needed` file that indicates changes
3. Review updated context files in `context/finance/database/`
4. Confirm schema hash and timestamps are updated
5. Report what changed and any actions needed

This ensures Claude has current database context without manual updates.