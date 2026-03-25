---
description: rapid, zero-downtime deployment of validated governance updates
---

# auto_deploy.md: Automated Governance Deployment

This workflow manages the transition of validated artifacts from `substrate/` to `active/` domains.

## 🚀 Execution Logic

1. **Gate Verification**: Ensure the artifact has passed `validator_simulation.py`.
2. **Atomic Swap**: Replace existing logic/artifact with the new version.
3. **Cache Invalidation**: Signal the engine to refresh the logic registry.
4. **Post-Deployment Audit**: Run a quick connectivity and integrity check.

## 🛠️ Steps

1. Run the validator simulation:

   ```bash
   python axion-core/forge/sentinel.py --mode validation
   ```

2. Perform the atomic update (Mock for pilot):

   ```bash
   # In a real scenario, this would involve a move or a symlink update
   echo "Deploying update to [TARGET_DOMAIN]..."
   ```

3. Trigger Registry Refresh:

   ```bash
   python axion-core/forge/generate_barrels.py
   ```

4. Verify Synthesis:

   ```bash
   # Check CFL logs for regression
   ```
