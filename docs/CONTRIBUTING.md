## Basics

Make sure to understand the basics of building a PyPI package ([example tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/)).



## Requirements (PyPI)

* Create a [TestPyPI](https://test.pypi.org/) account
* Create a [PyPI](https://pypi.org/) account
* Install requirements for developers:

   * `python3 -m pip install --upgrade build`
   * `python3 -m pip install --upgrade twine`

## Build and publish

1. Generate distribution archives:

python3 -m build

2. Upload distribution archives:

python3 -m twine upload --repository testpypi dist/*







## Build and push test version

If you made changes in *setup.py*, run first (and troubleshoot any error message):

```
sudo python setup.py develop
```

Before adding a new version of *pythomac*, please inform about the severity and version numbering semantics on [python.org](https://www.python.org/dev/peps/pep-0440/).

1. `cd` to your local *pythomac* folder (in *Terminal*)
1. Create *pythomac* locally 
	* Linux (in Terminal): `sudo python setup.py sdist bdist_wheel`
	* Window (in Anaconda Prompt with flussenv): `python setup.py sdist bdist_wheel`


## Push to PyPI

If you could build and install the test version successfully, you can push the new version to PyPI. **Make sure to increase the `VERSION="major.minor.micro" in *ROOT/setup.py***. Then push to PyPI (with your PyPI account):

`twine upload dist/*`

## Test

1. Create a new environment and activate it to test if the upload and installation work
    * On *Linux*:</br>`python -m venv test_env`</br>`source test_env/bin/activate`
    * On *Windows* (with Anaconda):</br>`conda activate pythomac-test`
1. Install the new version of *pythomac* in the environment:
	* `pip install -i https://test.pypi.org/simple/ pythomac`
1. Launch python and import *pythomac*:
	* `python`
	* `>>> import pythomac`

