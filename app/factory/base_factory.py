from abc import ABC, abstractmethod
from typing import Any

class BaseFactory(ABC):
    @abstractmethod
    def create(self) -> Any:
        pass