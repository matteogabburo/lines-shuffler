# lines-shuffler
A simple tool that can be used to randomly shuffle the lines of a document.

### Installation:

#### pip + git
```
pip install git+https://github.com/matteogabburo/lines-shuffler
```

### Usage:

```.sh
usage: __main__.py [-h] -i PATH_IN -o PATH_OUT [-s SEED]

A simple tool that can be used to shuffle the lines of a
document.

required arguments:
  -i PATH_IN, --path_in PATH_IN
                        The input file

  -o PATH_OUT, --path_out PATH_OUT
                        The output file
optional arguments:
  -s SEED, --seed SEED  The random seed
```