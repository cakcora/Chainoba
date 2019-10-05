## Foundation team

**This package includes dataparser with data insertions to PostgreSQL and RESTful APIs.**

### Project structure
foundations/
+-- api
|   +-- __init__.py
|   +-- main.py
+-- dataparser
|   +-- __init__.py
|   +-- bitcoin-parser.py
|   +-- Data_model.sql
+-- __init__.py
+-- environment.yml
+-- README.md
+-- setup.py

## Project Setup

1. Install [Anconda](https://www.anaconda.com/distribution/) to create a virtual environment for the project.
2. Create an environment by executing ` conda create -n blockchain python=3.7`.
3. Activate the environment ` conda activate blockchain`
4. Install dependencies in the environment `pip install -r requirements.txt`
5. Activate the environment ` conda activate blockchain`
6. (Optional) Deactivate the environment `conda deactivate`
7. Install [leveldb](https://github.com/google/leveldb), for linux `sudo apt-get install libleveldb-dev`, for MacOS `brew install leveldb` and for windows ``.
8. To be completed.

## Known Issues

* `conda: Command not found.` Add export PATH=~/anaconda3/bin:$PATH to your ~/.bashrc then test by opening a new terminal
and running `conda --version`.

## Contributors

## Contact
If you find any issues with the code, please contact any of the above mentioned members.
