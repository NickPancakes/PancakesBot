class ParoariaException(Exception):
	"""Base class that all Paroaria exceptions extend."""
	pass

class InternalError(ParoariaException):
	"""Non-recoverable error in the internals of Paroaria."""
	pass

class PluginError(ParoariaException):
	"""Raised when a plugin is invalid in some way."""
	pass

class CommandNotFoundError(ParoariaException):
	"""Raised when a given command isn't loaded."""
	pass

class ConfigNotFoundError(ParoariaException):
	"""Raised when an expected plugin config isn't found."""

class AmbiguousConfigError(ParoariaException):
	"""Raised when multiple configs exist for a plugin."""

class EventAlreadyExistsError(ParoariaException):
	"""Raised durring attempt to register an event name already registered."""

class EventDoesNotExistError(ParoariaException):
	"""Raised during attempt to register a callback for a nonexistent event."""

class EventCallbackError(ParoariaException):
	"""Raised when there is an error with a callback."""

class EventRejectedMessage(ParoariaException):
	"""Raised when an event callback wants to reject an event."""
