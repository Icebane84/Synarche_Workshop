---
description: Execute the Task Store Sovereignty Migration
---

// turbo-all
1. Verify connectivity:
   Run `CMD_TEST_BACKEND_HANDSHAKE` in the Synapse.

2. Execute migration:
   Run `CMD_MIGRATE_TASKS` in the Synapse.

3. Verify persistence:
   Run `CMD_FETCH_TASKS` to ensure the Loom is synchronized.
