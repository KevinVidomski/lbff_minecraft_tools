"""Type stubs for debugpy (expanded subset used by this project).

These stubs live in-tree so editors and linters (Pylance/pyright/pylint)
can resolve `import debugpy` even when the runtime package is only available
inside Blender's embedded Python. The goal is to provide useful completions
for the functions this repo uses without depending on an external types
package.
"""
from typing import Any, Iterable, Optional, Tuple


def listen(address: Tuple[str, int] | int | str = ...) -> None: ...
"""Start a debugpy listener.

Parameters
----------
address:
	Either a (host, port) tuple, an integer port, or a string address. When
	listening on all interfaces, use ("0.0.0.0", port).
"""


def wait_for_client(timeout: Optional[float] = None) -> None: ...
"""Block until a client connects or optional timeout (seconds) elapses.

If ``timeout`` is None the call may block indefinitely.
"""


def connect(address: Tuple[str, int] | str, timeout: Optional[float] = ...) -> None: ...
"""Connect the debugpy client to a listening debug server.

Parameters
----------
address:
	Address to connect to (host, port) or an address string.
timeout:
	Optional timeout in seconds.
"""


def enable_attach(address: Tuple[str, int] | None = ...) -> None: ...
"""Enable attaching a debugger (platform-specific hooks).

This is a convenience wrapper in the real package; providing a stub helps
editors surface the symbol.
"""


def breakpoint() -> None: ...
"""Programmatic breakpoint helper (invokes a debug break if attached).
"""


__all__: Iterable[str] = [
	'listen', 'wait_for_client', 'connect', 'enable_attach', 'breakpoint'
]
