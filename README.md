# python-project-lvl2
[![Build Status](https://travis-ci.org/sharkvoice/python-project-lvl2.svg?branch=master)](https://travis-ci.org/sharkvoice/python-project-lvl2)
[![Maintainability](https://api.codeclimate.com/v1/badges/a39b88f77390224636bb/maintainability)](https://codeclimate.com/github/sharkvoice/python-project-lvl2/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/a39b88f77390224636bb/test_coverage)](https://codeclimate.com/github/sharkvoice/python-project-lvl2/test_coverage)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
##
gendiff is a CLI utility that shows the difference between two JSON or YAML files.
##
To install the package, copy the following into the terminal:  
```
python3 -m pip install --user -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple sharkvoice-gendiff==0.3.1
```  
To run, type gendiff and the names of the files.  
  
Example:  
[![asciicast](https://asciinema.org/a/sQp6GyMHUPt87iOQYAhIpz4nW.svg)](https://asciinema.org/a/sQp6GyMHUPt87iOQYAhIpz4nW)  
  
By default, gendiff shows the difference with a jsonlike structure, but you can also change the output to real machine-readable JSON:  
```
gendiff before.json after.json -f json
```  
or more human-friendly plain text:
```
gendiff before.json after.json -f plain
```  
Example:  
[![asciicast](https://asciinema.org/a/AAWNQc7EpRJlHVmlaDSst94DA.svg)](https://asciinema.org/a/AAWNQc7EpRJlHVmlaDSst94DA)
