DROP TABLE IF EXISTS Employees CASCADE;
DROP TABLE IF EXISTS Animals CASCADE;
DROP TABLE IF EXISTS Owners CASCADE;
DROP TABLE IF EXISTS Events CASCADE;
DROP TABLE IF EXISTS Vet_Visit CASCADE;
DROP TABLE IF EXISTS Participation CASCADE;

DROP TYPE IF EXISTS jobs;
DROP TYPE IF EXISTS plannedEvent;

CREATE TYPE jobs AS ENUM ('Trainer', 'Vet', 'Secretary', 'Groomer', 'Daycare');
CREATE TYPE plannedEvent AS ENUM ('Basic Obedience Training', 'Advanced On Leash Training', 'Off Leash Adventure Training', 'Daycare', 'Vet Visit', 'Grooming Visit');

CREATE TABLE Employees (
    EmployeeID SERIAL,
    name varchar(50) NOT NULL,
    position jobs NOT NULL,
    phone varchar(50) NOT NULL,
    address1 varchar(50) NOT NULL,
    PRIMARY KEY (EmployeeID)
);

CREATE TABLE Owners (
    OwnerID SERIAL,
    Name varchar(50) NOT NULL,
    phone varchar(50) NOT NULL,
    PRIMARY KEY(OwnerID)
);

CREATE TABLE Animals (
    AnimalID SERIAL,
    Name varchar(50) NOT NULL,
    breed varchar(50),
    age integer,
    ownerID integer NOT NULL,
    PRIMARY KEY (AnimalID),
    FOREIGN KEY(ownerID) REFERENCES Owners(OwnerID)
);

CREATE TABLE Vet_Visit (
    VisitID SERIAL,
    Visit_Date DATE NOT NULL,
    Weight INTEGER,
    Temperature INTEGER,
    Blood_Pressure VARCHAR(100),
    Pulse INTEGER,
    Respiration VARCHAR(100),
    Pain VARCHAR(100),
    Initials BOOL,
    Animal_ID INTEGER NOT NULL,
    PRIMARY KEY(VisitID),
    FOREIGN KEY(Animal_ID) REFERENCES Animals(AnimalID)
);

CREATE TABLE Events(
    EventID SERIAL,
    EventType plannedEvent NOT NULL,
    EventDate DATE,
    EmployeeID INTEGER NOT NULL,
    PRIMARY KEY (EventID),
    FOREIGN KEY(EmployeeID) REFERENCES Employees(EmployeeID)
);

CREATE TABLE Participation (
    EventID INTEGER,
    AnimalID INTEGER,
    FOREIGN KEY(AnimalID) REFERENCES Animals(AnimalID),
    FOREIGN KEY(EventID) REFERENCES Events(EventID)
);
