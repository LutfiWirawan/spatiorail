"""Pipeline domain model."""

from dataclasses import dataclass, field

from spatiorail.core.pipeline.task import Task


@dataclass
class Pipeline:
    """A collection of tasks forming a workflow."""

    id: str
    name: str
    tasks: list[Task] = field(default_factory=list)
