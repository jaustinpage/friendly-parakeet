# friendly-parakeet

Implement sim.py to simulate logic. The resulting script will take two text files as input (see example input files input.txt and circuit.txt below). It must implement operations supporting the Boolean functions (inv, and2, & or2)as defined below:

output = inv(input)
output = and2(input1, input2)
output = or2(input1, input2)
 
| Inputs     |            | Output   |         |
| ---------- | ---------- | -------- | ------- |
| **Input**  |            | **Inv**  |         |
| 0          |            | 1        |         |
| 1          |            | 0        |         |
| **input1** | **input2** | **and2** | **or2** |
| 0          | 0          | 0        | 0       |
| 0          | 1          | 0        | 1       |
| 1          | 0          | 0        | 1       |
| 1          | 1          | 1        | 1       |

input.txt
```
in1 = [0, 1, 1]
in2 = [1, 0, 1]
in3 = [1, 1, 1] 
```
circuit.txt
```
out1 = and2(out4, in2)
out2 = or2(out1, out3)
out3 = and2(in1, in3)
out4 = inv(in1)
```
> sim.py input.txt circuit.txt
```
out1 = [1, 0, 0]
out2 = [0, 1, 1]
out3 = [1, 1, 1]
out4 = [1, 0, 0]
```

Optional Bonus: Only do this if you're interested
    Add support for 'X' construct, where 'X' means that the state is unknown or simultaneously driven to different values. This construct adds the following combinations to the table above.
 
| Inputs     |            | Output   |         |
| ---------- | ---------- | -------- | ------- |
| **Input**  |            | **Inv**  |         |
| X          |            | X        |         |
| **input1** | **input2** | **and2** | **or2** |
| 0          | X          | 0        | X       |
| X          | 0          | 0        | X       |
| 1          | 0          | 0        | 1       |
| X          | 1          | X        | 1       |

input.txt
```
in1 = [ 0 ,  1, 'X']
in2 = ['X', 'X', 1 ]
in3 = ['X',  1,  1 ]
```

circuit.txt
```
out1 = and2(out4, in2)
out2 = or2(out1, out3)
out3 = and2(in1, in3)
out4 = inv(in1)
```

```
> sim.py input.txt circuit.txt
out1  ['X', 0, 'X']
out2  [ 0 , 1, 'X']
out3  ['X', 1, 'X']
out4  [ 1 , 0, 'X']
```

## Prerequisites

- Python 3.6+
- up to date pip
  ```shell
  # this needs to be done outside of a virtualenv, not inside
  pip install --upgrade pip
  ```

## Install

To Install and use this library:

```shell
pip install --upgrade pip
pip install git+ssh://github.com/jaustinpage/friendly-parakeet#egg=friendly-parakeet
```

Then, in your python script, you can use the library.

```python
import friendly-parakeet
friendly-parakeet.<do something awesome>()
```

If you are using this library from another python library, dont forget to update your
`setup.cfg` \[options\] install-requires section!

## Development Setup

Found a bug? Need a feature? Get set up for development on friendly-parakeet here.

### Windows

#### Windows Development tools

- [PyCharm professional](https://www.jetbrains.com/pycharm/)

#### Windows Setup

1. Update pip
   ```shell
   pip install --upgrade pip
   ```
1. Install tox

```shell
# this needs to be done outside of a virtualenv, not inside
pip install --upgrade tox
```

1. Make a `Documents\github` folder
1. Clone this repo to `Documents\github\friendly-parakeet` folder using git
1. Launch PyCharm
   1. go to `File -> Open...`
   1. Select `Documents\github\friendly-parakeet` in the prompt
   1. Select Open project in `New Window`
   1. In the bottom-right corner of the screen, it says `No Interpreter`. Click on this
      box and select `Add Interpreter`
   1. In the Add Python Interpreter prompt, select `New Interpreter`, Location:
      `Documents\github\friendly-parakeet\.venv`. Select `OK`
   1. Make a branch in git for your feature
   1. Fix the bug or add the feature
   1. Commit, push, let the repo owner know that there is a fix available

### Ubuntu (linux)

#### Ubuntu Development tools

- [PyCharm professional](https://www.jetbrains.com/pycharm/)

#### Ubuntu setup

In a terminal

```shell
# Install and git
sudo apt install git
# Install tox (this needs to be done outside of a virtualenv, not inside)
pip install --upgrade tox
mkdir -p ~/github
# Clone the repo
git clone ssh://github.com/jaustinpage/friendly-parakeet ~/github/friendly-parakeet
# change working directory to repo
cd ~/github/friendly-parakeet
# Build the code
tox
```

At this point, I recommend using PyCharm to continue development.

1. Make a branch in git for your feature
1. Fix the bug or add the feature
1. Commit, push, let the repo owner know that there is a fix available

### A normal day of editing

1. `cd ~/github/friendly-parakeet`
1. Make some edits
1. run `tox`, have failing tests
   1. fix some tests, and run `pytest`. Repeat until tests passing.
1. run `tox`, have linting errors
   1. Linting errors are a great way to learn how python works. Fix these. rerun `tox`.
      Repeat.
1. run `tox`, have code coverage errors. Increase the test coverage and rerun `tox`
1. Wheels are built, test the code manually, commit, and push for review.

##FAQ

### Common Lint Errors and how to fix them:

- `SC100` or `SC200`: If the flagged word is a false positive, add the word to anywhere
  `whitelist.txt` file. `tox` will automatically sort the file alphabetically the next
  time it is run.

##Repo/Library Management Tasks


### How to add a 3rd party (PyPi) runtime dependency

1. In `setup.cfg` find `[options]` and add dependency to `install_requires =`. For
   example to add `pandas` to your runtime dependencies, make the `[options]` secton
   look like this:
   ```shell
   # file: setup.cfg
   <... truncated ...>
   [options]
   <... truncated ...>
   install_requires =
       importlib-metadata; python_version<"3.6"
       pyscaffold>=4.0,<5.0a0
       pyscaffoldext-markdown
       pandas
   ```
1. Run `tox`. Package will automatically be installed.

### Advanced: Creating a new package version

remember to use [Semantic versioning](https://www.python.org/dev/peps/pep-0440/) (tldr:
use #.#.#, and only increment the last digit, unless you are changing the api call
signatures)

1. on the default branch run

   ```shell
   git pull --update
   git status  # Make sure current directory is clean
   git tag -r <version you want to tag> <version>
   git push
   ```

   For example, if you want the current tip to be version 0.0.2, then `git tag 0.0.2`.
   Then push the tag.

### Updating repository boilerplate files

```shell
# Get latest boilerplate
pip install --update git+ssh://github.com/jaustinpage/pyscaffoldext-jaustinpage#egg=pyscaffoldext-jaustinpage
# Make a commit
cd pyscaffold-jaustinpage
git add .
git commit -m "Preparing to update boilerplate"
# Update boilerplate
putup --update
# Make sure the build is good
tox
# Commit new files
git add
git commit -m "Updating boilerplate."
git tag <new package version>
git push
```

<!-- pyscaffold-notes -->

## Note

This project has been set up using PyScaffold 4.1.4. For details and usage information
on PyScaffold see https://pyscaffold.org/.

```
```
