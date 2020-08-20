----------------------------------------------------------------------------------------------------
REQUIREMENTS
----------------------------------------------------------------------------------------------------

CherryPy==18.6.0
pymongo==3.10.0
Jinja2==2.11.2
psycopg2==2.8.5
PyQt5

Docker installation instructions below

----------------------------------------------------------------------------------------------------
INSTALLING DOCKER AND INITIALIZING DATABASE
----------------------------------------------------------------------------------------------------

MUST BE IN postgreSQL directory

1. Install postgresql

    sudo apt install postgresql postgresql-contrib

2. install docker.io

    sudo apt install docker.io

3. install docker-compose

    sudo apt install docker-compose

4. Create a new docker volume

    sudo docker volume create --name=minesweeper

5. start the docker

    sudo docker-compose up -d

    // To view the database:
    psql game -h 127.0.0.1 -U username -p 5433
    password: 'example'

    // To get rid of existing volumes
    sudo docker system prune --volumes

----------------------------------------------------------------------------------------------------
RUN INSTRUCTIONS
----------------------------------------------------------------------------------------------------

RUN GRAPHICS ONLY
    ./minesweeper

RUN NON GUI DEMO
    ./nonGUI_example.py

RUN WEB SERVER ONLY
    ./web/website.py

RUN APPLICATION AS WHOLE
    ./run.py
