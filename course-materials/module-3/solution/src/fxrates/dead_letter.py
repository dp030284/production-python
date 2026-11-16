"""Where records go when they can't be processed.

Not silently dropped. Not crashing the whole run over one bad record.
Captured somewhere you can actually go look, with a reason attached.
"""

from dataclasses import dataclass, field


@dataclass
class DeadLetter:
    entries: list[dict[str, str]] = field(default_factory=list)

    def add(self, identifier: str, reason: str) -> None:
        self.entries.append({"identifier": identifier, "reason": reason})

    def __len__(self) -> int:
        return len(self.entries)
