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
7. Install [leveldb](https://github.com/google/leveldb), for linux `sudo apt-get install libleveldb-dev`, for MacOS `brew install leveldb` and for Windows....
8. Install [Postgres.](https://tecadmin.net/install-postgresql-server-on-ubuntu/)
9. Open a terminal and enter ``sudo su - postgres``, then start Postgres ``psql``. Finally create the user postgres ``CREATE USER postgres WITH SUPERUSER PASSWORD 'postgres';``
9. Connect PyCharm to the database: Navigate to  `View>Tool Windows>Databases` and click `+` select
 `Data Source>Postgres SQL`, and then add in the ``username`` field `postgres` and ``password`` field ``postgres`` select OK from the pop up window.
10. Create the database with the provided DDL. On the Database side bar, right click on Postgres and select ``Jump to console...``
then copy everything inside `/foundations/dataparser/Data_model.sql` into the terminal and execute it. 
11. If you click on the Database side bar, expand ``postgres@localhost>databases>postgres>schemas>bitcoin`` and you should be able to see the database.

## Known Issues

* `conda: Command not found.` Add export PATH=~/anaconda3/bin:$PATH to your ~/.bashrc then test by opening a new terminal
and running `conda --version`.


## Contributors

## Contact
If you find any issues with the code, please contact any of the above mentioned members.
