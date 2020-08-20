#!/usr/bin/env python3


from psql_database import PsqlDatabase

def main():

    database = PsqlDatabase()
    database.connectToDatabase()
    data = database.getMultiplayerScores()
    print(data)

if __name__ == "__main__":
    main()
