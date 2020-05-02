import mimetypes
from abc import ABC, abstractmethod
from dataclasses import dataclass
from io import IOBase
from typing import Optional


class FileTypeNoExtension:
    pass


@dataclass
class FileType:
    """File type hint for tests.

    :param mime: required MIME type
    :param override_file_ext: override default MIME type extension
    """
    mime: str
    override_file_ext: Optional[str] = FileTypeNoExtension

    def get_file_extension(self) -> Optional[str]:
        if self.override_file_ext is not FileTypeNoExtension:
            return self.override_file_ext

        return mimetypes.guess_extension(self.mime, strict=False)


class Comparator(ABC):
    """Abstract type comparator"""
    @abstractmethod
    def compare(self, test_obj: any, canon_obj: any):
        """Compares objects"""
        pass  # pragma: no cover


class RegressContext(ABC):
    """Abstract test context"""
    @abstractmethod
    def get_storage_name(self, file_type_hint: FileType,
                         suffix: Optional[str] = None):
        """Gets name for test"""
        pass  # pragma: no cover

    @abstractmethod
    def get_storage_name_from_filename(self, filename: str):
        pass  # pragma: no cover

    @abstractmethod
    def get_comparator(self) -> Optional[Comparator]:
        pass  # pragma: no cover


class CanonizePolicy(ABC):
    """Abstract run decisions with conflicted tests"""
    @abstractmethod
    def ask_canonize(self, context: RegressContext, exc: Exception) -> bool:
        """Asks user for canonization or decide it by internal tests
        policies"""
        pass  # pragma: no cover


class RegressSerializer(ABC):
    """Abstract serializer for objects canonization"""
    def __init__(self, file_type_hint: FileType):
        """Init

        :param file_type_hint: hint for generating file or resource name
        """
        self._file_type_hint = file_type_hint

    @abstractmethod
    def load(self, stream: IOBase) -> any:
        pass  # pragma: no cover

    @abstractmethod
    def dump(self, obj: any, stream: IOBase):
        pass  # pragma: no cover

    @property
    def file_type_hint(self) -> FileType:
        return self._file_type_hint


class RegressStorage(ABC):
    """Abstract storage for canonized data"""
    @abstractmethod
    def open_read(self, key: str) -> Optional[IOBase]:
        pass  # pragma: no cover

    @abstractmethod
    def open_write(self, key: str) -> IOBase:
        pass  # pragma: no cover


class UserInteraction(ABC):
    """Abstract interaction with user"""
    @abstractmethod
    def ask_canonize(self, context: RegressContext, exc: Exception) -> bool:
        """Asks user for canonization"""
        pass  # pragma: no cover