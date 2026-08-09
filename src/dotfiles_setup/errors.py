"""Expected setup failures that should be reported without tracebacks."""

from __future__ import annotations


class SetupError(RuntimeError):
    """Base class for expected setup failures."""


class LockError(SetupError):
    """A mutating setup command could not acquire the user lock."""


class LinkError(SetupError):
    """Managed-link planning or mutation failed."""


class CleanupError(SetupError):
    """Managed-link cleanup failed."""


class ManifestError(SetupError):
    """The durable operation manifest could not be read or written."""


class RecoveryError(SetupError):
    """An interrupted operation could not be recovered safely."""


class ShellHandoffError(SetupError):
    """Shell startup files could not be updated safely."""
