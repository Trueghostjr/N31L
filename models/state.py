from dataclasses import dataclass
from typing import Optional

from hikari import User


@dataclass(kw_only=True)
class State:
    """Dataclass object containing a temporary bot state."""

    raidOffense: bool
    raidOffAge: Optional[int]
    raidOffReason: Optional[str]
    raidOffActor: Optional[User]
    raidOffCount: Optional[int]

    raidDefense: bool
