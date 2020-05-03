# region: header
import pytest

from regress.ext.pytest import PytestContext, register_addoption
from regress.fixture import RegressFixture
from regress.pub import DefaultRegress


def pytest_addoption(parser):
    register_addoption(parser)


@pytest.fixture(scope='module')
def regress_instance():
    regress = DefaultRegress()
    regress.ensure_exists(clear=True)
    yield regress


@pytest.fixture(scope='function')
def regress(regress_instance, request):
    fixture = RegressFixture(regress_instance,
        PytestContext(request))
    yield fixture
# endregion: header

@pytest.mark.no_console
# region: test_simple
# regress is the helper fixture easy to setup
def test_simple(regress: RegressFixture):
    result = {'a': 1}
    regress.test(result)  # Commit first time

    result2 = {'a': 1}
    regress.test(result2)  # Ok. No object result changes

    result3 = {'a': 3}  # Try commit change. Raised the AssertionError
    with pytest.raises(AssertionError) as e:
        regress.test(result3)
# endregion: test_simple
