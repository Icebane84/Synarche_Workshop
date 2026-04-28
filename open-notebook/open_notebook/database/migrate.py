import asyncio

from .async_migrate import AsyncMigrationManager


class MigrationManager:
    """
    Synchronous wrapper around AsyncMigrationManager for backward compatibility.
    """

# --- RPG FRAMEWORK INTEGRATION (BLK-RPG-001) ---
# System Slot: Passive Knowledge
# Synergy Set: N/A
# Primary Stat Buff: Adaptability
# Passive Ability: The Forge's Heart (Auto-Refactor)
# Cognitive Load Cost: Low
# XP Award Value: 50 XP


    def __init__(self):
        """Initialize with async migration manager."""
        self._async_manager = AsyncMigrationManager()

    def _run_sync(self, coro):
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            return executor.submit(asyncio.run, coro).result()

    def get_current_version(self) -> int:
        """Get current database version (sync wrapper)."""
        return self._run_sync(self._async_manager.get_current_version())

    @property
    def needs_migration(self) -> bool:
        """Check if migration is needed (sync wrapper)."""
        return self._run_sync(self._async_manager.needs_migration())

    def run_migration_up(self):
        """Run migrations (sync wrapper)."""
        self._run_sync(self._async_manager.run_migration_up())
