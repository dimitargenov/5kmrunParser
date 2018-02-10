use fivekmrun;

ALTER TABLE Results
ADD FOREIGN KEY (RaceId) REFERENCES Race(Id);

CREATE TABLE Race(
	Id int,
    Name varchar(255),
    DomParkId int,
    Created datetime,
    PRIMARY KEY (Id),
    FOREIGN KEY (DomParkId) REFERENCES DomPark(Id)
);

CREATE TABLE Runner(
	Id int,
    Name varchar(255),
    RunnerId int unique,
    DomParkId int,
    AgeCategoryId int,
    CityId int,
    Sex tinyint,
    PRIMARY KEY (Id),
    FOREIGN KEY (CityId) REFERENCES City(Id),
    FOREIGN KEY (DomParkId) REFERENCES DomPark(Id),
    FOREIGN KEY (AgeCategoryId) REFERENCES AgeCategory(Id)
);

CREATE TABLE City(
    Id int,
    Name varchar(255),
    PRIMARY KEY (Id)
);

CREATE TABLE DomPark(
	Id int,
    Name varchar(255),
    CityId int,
    PRIMARY KEY (Id),
    FOREIGN KEY (CityId) REFERENCES City(Id)
);

CREATE TABLE AgeCategory(
	Id int,
    Name varchar(255),
    PRIMARY KEY (Id)
);