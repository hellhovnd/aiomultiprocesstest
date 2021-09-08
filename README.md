aiomultiprocess vs pure asyncio
===============================

**Requirements**
* python>=3.7
* pipenv
* aiohttp==\*
* aiomultiprocess==\*

To run the tests use the following command:
```python
$ pipenv run run_tests.py
```

aiomultiprocess could work for tasks that are more CPU-bound than IO-bound but
for IO-bound tasks it really sucks!
