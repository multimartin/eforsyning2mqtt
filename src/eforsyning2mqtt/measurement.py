from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Iterable, Iterator, Mapping, Optional


@dataclass(slots=True)
class Measurement:
    """
    Complete dataset received from eForsyning.
    """

    timestamp: datetime

    values: dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Return the value for ``key`` or ``default`` if not present."""
        return self.values.get(key, default)

    def items(self) -> Iterable[tuple[str, Any]]:
        """Yield (key, value) pairs."""
        return self.values.items()

    def keys(self) -> Iterable[str]:
        """Return view of keys in the measurement."""
        return self.values.keys()

    def as_dict(self) -> Mapping[str, Any]:
        """Return underlying dictionary representation."""
        return self.values