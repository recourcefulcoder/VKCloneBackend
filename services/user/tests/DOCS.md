# Documentation for written tests

There is one thing to be considered when writing tests for this code - TokenManager class 
creates only one instance of redis.asyncio.Redis(), which is expected to use same asyncio event
loop for all the calls to that instance. 

Since that, using TokenManager in pytest fixtures
(as well as tests related to tested codebase, using this class) requires ensuring that tests 
and fixtures run in the same asyncio event loop.

This is ensured by two conventions:
- loop_scope of asyncio tests is "session", which is specified on a package level (in \_\_init\_\_.py) with 
```python
import pytest
pytestmark = pytest.mark.asyncio(loop_scope="session")
```
in order to use this pytestmark, it should be imported to testfiles with
```
from . import pytestmark
```

- asynchronous fixture loop scope is "session", which is specified with config options in pyproject.toml

## crucial configuration keys in pyproject.toml

```ini
[tool.pytest.ini_options]
asyncio_default_fixture_loop_scope = "session"
```
this sets loop scope for asynchronous tests, as mentioned in [intro section](#documentation-for-written-tests)

## conftest.py fixtures

1. session
2. _run_services_if_needed - if tests are run in debug mode, runs Redis service and a Celery worker
3. client

