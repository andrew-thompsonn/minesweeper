#!/usr/bin/env python3


from psql_database import PsqlDatabase

def main():

    database = PsqlDatabase()
    database.connectToDatabase()
    database.getSinglePlayerScores()


if __name__ == "__main__":
    main()
