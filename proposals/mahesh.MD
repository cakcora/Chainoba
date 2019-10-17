


# Foundation Team

The primary tasks of the foundation team are as follows:
1. Data parser [[1](mahya.MD)] to extract the details from [Bitcoin Core](https://bitcoin.org/en/bitcoin-core/).
2. APIs to query the parsed blockchain data.
3. Hosting the APIs and Data server (*PostgreSQL*) on a remote machine (details of the remote machine will updated later)
4. [API Documentation](http://159.203.28.234:8000/) (**under development**)

# My Contribution
1. Setting up the PostgreSQL data server (**development**) on [Digital Ocean](https://www.digitalocean.com/) for API development and to store the parsed data of Bitcoin (currently storing data for only **2009**) based on the ERM diagram described in [[1](mahya.MD)].
2. Contributed to the API design of `foundations/api`. The overall project directory is shown in foundations [README.md](../foundations/README.md).
3. I have initiated the following scripts for APIs:
    1. `foundations/api/main.py`: A [Flask-restful](https://flask-restful.readthedocs.io) application file to run the endpoints.
    2. `foundations/api/models/models.py`: The script to stores all the PostgresSQL table structures as classes for [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com) to interact with the database. 
    3. `foundations/api/resources/block.py`: The primary endpoint to query block data. (Contributions: API structure, query params validation, querying PostgreSQL)
    4. `foundations/api/resources/transaction.py`: An internal endpoint to send the transaction data to the block endpoint. (Contributions: basic template)
    
4. Documenting [[2](http://159.203.28.234:8000/)]  the API endpoints in `foundations/apidoc`.

### TODO
1. Migrating the database from **development** machine to the **production** machine.
2. Use production-ready web server ([Nginx](https://www.nginx.com/)), application web server ([Gunicorn](https://gunicorn.org/)) and maybe a message-broker ([Redis](https://redis.io/)).
3. Diagrammatic representation of the project.
