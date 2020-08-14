sudo docker system prune --volumes

// Set up volume and create docker
sudo docker volume create --name=minesweeper
sudo docker-compose up -d

// To view the database:
psql game -h 127.0.0.1 -U username -p 5433

  password: 'example'

REQUIREMENTS


INSTALLING DOCKER AND INITIALIZING DATABASE
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


RUN THE APPLICATION
    ./minesweeper
