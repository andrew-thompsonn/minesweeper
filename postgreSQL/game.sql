DROP TABLE IF EXISTS Save_State CASCADE;
DROP TABLE IF EXISTS Game_Info CASCADE;
DROP TABLE IF EXISTS Player_Info CASCADE;

CREATE TABLE Player_Info (
    PlayerID SERIAL,
    Name varchar(25) NOT NULL,
    Type BOOLEAN NOT NULL,
    PRIMARY KEY (PlayerID)
);

CREATE TABLE Game_Info (
    GameID INTEGER NOT NULL,
    PlayerID integer NOT NULL,
    Difficulty varchar(50) NOT NULL,
    Game_Time varchar(10) NOT NULL,/* -> Planning on changing this to NUMERIC(4, 3) */
    Mines_left integer NOT NULL,
    Win boolean,
    status integer NOT NULL,
    PRIMARY KEY(GameId),
    FOREIGN KEY(PlayerID) REFERENCES Player_Info(PlayerID)
);

CREATE TABLE Save_State (
    SaveID integer NOT NULL,
    Size varchar(50) NOT NULL,
    Visible_Bricks integer[] NOT NULL,
    Mine_Locations integer[] NOT NULL,
    flag_locations integer[] NOT NULL,
    GameID integer NOT NULL,
    datetime TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (SaveId),
    FOREIGN KEY (GameID) REFERENCES Game_Info(GameID)
);
