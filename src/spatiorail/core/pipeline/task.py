"""Task domain model."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Task:
    """A single unit of work within a pipeline."""

    id: str
    name: str
    operator: str
    params: dict[str, Any] = field(default_factory=dict)
    depends_on: tuple[str, ...] = ()
