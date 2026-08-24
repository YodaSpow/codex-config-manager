"""Project exception hierarchy."""


class CCMError(RuntimeError):
    """Base error safe to present to an operator."""


class ConfigurationError(CCMError):
    """Configuration is missing, malformed, or unsafe."""


class IdentityError(CCMError):
    """Detected and configured machine identity do not agree."""


class PathSafetyError(CCMError):
    """A path cannot be proven safe for the requested operation."""


class ValidationError(CCMError):
    """Managed state or a generated projection is invalid."""


class RsyncError(CCMError):
    """The repository-owned rsync contract failed."""


class GitSafetyError(CCMError):
    """Git state is unsafe or ambiguous."""


class PublicationHeld(CCMError):
    """Publication is validly held by settlement or configured mode."""
