from _typeshed import Incomplete
from collections.abc import Generator

from networkx.utils.backends import _dispatchable

@_dispatchable
def connected_components(G) -> Generator[Incomplete, None, None]: ...
@_dispatchable
def number_connected_components(G): ...
@_dispatchable
def is_connected(G): ...
@_dispatchable
def node_connected_component(G, n): ...