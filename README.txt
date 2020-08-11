// Set up volume and create docker
sudo docker volume create --name=minesweeper
sudo docker-compose up -d

// To view the database:
psql game -h 127.0.0.1 -U username -p 5433

  password: 'example'

// To run the application
./minesweeper
