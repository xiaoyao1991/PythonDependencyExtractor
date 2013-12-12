### Python Package Dependency Extractor
This script will extract the dependencies of a python file, or a directory that contains python files. This will be useful in either using third-party package that doesn't come with a "requirement.txt", or creating your own "requirement.txt" when porting to server. 

#### Usage:
./extract-dependencies.py [-r] *<path-to-file-or-dir>* > requirement.txt


### Note:
Currently this script only supports python 2.7. If you want support for other versions of python, just extract the builtin modules list from <http://docs.python.org/2.7/py-modindex.html> and assign the list to the builtin_modules in the **DependencyExtractor** class. Or even easier, simply uncomment the *get_builtin_packages* method.

#### TODO:  
1. Avoid comment area (Done)
2. Eliminate project modules (Done)