### Python Package Dependency Extractor
This script will extract the dependencies of a python file, or a directory that contains python files. This will be useful in either using third-party package that doesn't come with a "requirement.txt", or creating your own "requirement.txt" when porting to server.

#### Usage:
./extract-dependencies.py [-r] *<path-to-file-or-dir>* > requirement.txt

#### TODO:  
1. Avoid comment area (Done)
2. Eliminate project modules