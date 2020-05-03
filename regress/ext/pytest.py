from typing import Optional

from regress.base import RegressContext, FileType, Comparator, \
    RegressTestResult


def _make_filename_from_pytest_nodeid(nodeid):
    """Transforms pytest nodeid to safe file name"""
    return (nodeid.lower()
            .replace('/', '_')
            .replace(':', '_')
            .replace('.', '_'))


class PytestComparator(Comparator):
    @classmethod
    def compare(cls, test_obj: any, canon_obj: any):
        """Compares objects"""
        assert test_obj == canon_obj


class PytestResult(RegressTestResult):
    """Pytest test result"""
    def __init__(self, *, test_obj: any, canon_obj: any, exc: Exception,
                 context: 'PytestContext'):
        self._test_obj = test_obj
        self._canon_obj = canon_obj
        self._exc = exc
        self._context = context

    def format_diff(self) -> str:
        # Pytest internal pretty comparison magic
        from _pytest.assertion import util
        compare_result = util._reprcompare('==', self._test_obj,
                                           self._canon_obj)
        return f'{compare_result}'


class PytestContext(RegressContext):
    """Test context from Pytest"""

    def __init__(self, request, comparator: Optional[Comparator] = None):
        """Initializes pytest context

        :param request: standard request fixture
        :param comparator: comparison for objects
        """
        self._request = request
        self._nodeid = request.node.nodeid
        self._comparator = (PytestComparator() if comparator is None
                            else comparator)

    def get_storage_name(self, file_type_hint: FileType,
                         suffix: Optional[str] = None):
        name = _make_filename_from_pytest_nodeid(self._nodeid)
        if suffix is not None:
            name += suffix

        file_ext = file_type_hint.get_file_extension()
        if file_ext is not None:
            name += file_ext

        return name

    def get_storage_name_from_filename(self, filename: str):
        return filename

    def get_comparator(self) -> Optional[Comparator]:
        return self._comparator

    def ask_canonize(self) -> bool:
        """Checks that context allow canonization with user interaction.
        :func:`register_addoption` had to be called
        in `conftest.py` to support `--canonize` parameter in pytest running.
        """
        return self._request.config.getoption("--canonize")

    def create_test_result(self, test_obj: any, canon_obj: any,
                           exc: Exception) -> RegressTestResult:
        return PytestResult(test_obj=test_obj, canon_obj=canon_obj, exc=exc,
                            context=self)


def register_addoption(parser):
    """ Call this function in `conftest.py` to enable canonize online
    such way:

    .. highlight:: python
    .. code-block:: python

        def pytest_addoption(parser):
            register_addoption(parser)

    """
    parser.addoption('--canonize', action='store_true', help='Do canonization '
                                                             'online')
