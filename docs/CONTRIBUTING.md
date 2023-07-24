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

twine upload dist/*



## Test

1. Create a new environment and activate it to test if the upload and installation work
    * On *Linux*:</br>`python -m venv test_env`</br>`source test_env/bin/activate`
    * On *Windows* (with Anaconda):</br>`conda activate pythomac-test`
1. Install the new version of *pythomac* in the environment:
	* `pip install pythomac`
1. Launch python and import *pythomac*:
	* `python`
	* `>>> import pythomac`

