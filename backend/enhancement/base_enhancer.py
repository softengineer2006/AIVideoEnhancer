from abc import ABC, abstractmethod
from pathlib import Path


class BaseEnhancer(ABC):
    """
    Base class for all image enhancement models.
    """

    @abstractmethod
    def load(self) -> None:
        pass

    @abstractmethod
    def enhance(
        self,
        input_image: Path,
        output_image: Path,
    ) -> None:
        pass