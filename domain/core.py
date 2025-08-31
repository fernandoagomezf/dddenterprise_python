from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4
from typing import Any, List

@dataclass(frozen=True)
class ValueObject(ABC):
    def __eq__(self, other:Any) -> bool:
        eq = False
        if isinstance(other, self.__class__):
            eq = self.__dict__ == other.__dict__ 
        return eq 
    
    def __ne__(self, other:Any) -> bool:
        return not self.__eq__(other)
    
    def __hash__(self) -> int:
        return hash(tuple(sorted(self.__dict__.items())))

@dataclass(frozen=True)
class DomainEvent(ValueObject):
    code:str 
    raised:datetime 

class Entity(ABC):
    def __init__(self, id:UUID):
        if id is None:
            raise ValueError("An entity must have a valid ID.")
        self._id = id

    def __eq__(self, other: Any) -> bool:
        eq = False
        if isinstance(other, self.__class__):
            eq = self.id == other.id
        return eq
    
    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)
    
    def __hash__(self) -> int:
        return hash(self.id)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r})"
    
class AggregateRoot(Entity):
    def __init__(self, id:UUID = None):
        super.__init__(id if id is not None else uuid4())
        self._events: List['DomainEvent'] = []

