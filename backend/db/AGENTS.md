# DB Agent Notes

## Template lifecycle and current ownership

- This database layer is a starter template. No demo table, query, seed data, migration example, or helper must be kept merely because it came with the template.
- Replace or remove starter schema and queries as needed for the user's application. Preserve actual user data when changing an application database.
- With every database feature request, update the ownership inventory here and in the root and backend `AGENTS.md` files. Say which tables and modules are still examples and which now belong to the user's application.
- Remaining template: all of `backend/db/` and the example `users`, `refresh_sessions`, and `notes` schema in `backend/migrations/`.
- User application: none yet.
- When no template parts remain, remove all template inventories, wording, and template-only rules here. Keep only instructions for the application database.

## Working defaults

- Keep DB code easy enough for students to trace from route to SQL.
- Every table must be created by yoyo migrations in `backend/migrations`.
- Use `STRICT` tables whenever SQLite allows it.
- Store booleans as `INTEGER CHECK (... IN (0, 1))`.
- Keep queries small, named clearly, and close to the table they work with.
- Prefer explicit `INSERT`, `UPDATE`, `DELETE`, and careful `ON CONFLICT`.
- Add or update tests whenever DB schema or query behavior changes, including success paths and important failure paths.
- After every DB change, run `uv run pytest` and confirm all tests pass before calling the task done.
- Start each DB file with a short simple-English docstring that says what table or query group it owns, when to edit it, and whether it can be copied to add another table or query module.
- Usual pattern for a new table:
  - add a new migration file in `backend/migrations`;
  - add a new query module in `backend/db`;
  - call that module from the matching route file;
  - add backend tests that touch the new table through real routes or helpers.
- Copy an existing table query module when you add another table with CRUD-style queries.
- Extend an existing DB file only when the queries still belong to the same table or helper topic.
