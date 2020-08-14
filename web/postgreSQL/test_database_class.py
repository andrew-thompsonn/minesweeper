#!/usr/bin/env python3


from psql_database import PsqlDatabase

def main():

    database = PsqlDatabase()
    database.connectToDatabase()
    database.checkMultiplayer(2)


if __name__ == "__main__":
    main()
