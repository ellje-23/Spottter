drop table if exists birdcolors;
create table birdcolors(
    species varchar(50),
    colorName varchar(50),
    constraint setColor primary key(species,colorName)
);

drop table if exists sightings;
create table sightings(
    email varchar(50),
    species varchar(50),
    datetime timestamp, 
    longitude decimal,
    latitude decimal,
    stateName varchar(50),
    constraint setsighting primary key(email, species, datetime)
);

drop table if exists groups;
create table groups(
    groupID int primary key not null, 
    numMembers int,
    groupName varchar(50)
);

drop table if exists meetings;
create table meetings(
    groupID integer,
    dateTime timestamp,
    location varchar(50),
    stateName varchar(50),
    meetingTopic varchar(100),
    constraint setMeeting primary key(groupID, dateTime)
);

drop table if exists foundin;
create table foundin(
    species varchar(50),
    stateName varchar(50),
    speciePopulation integer,
    constraint birdFound primary key(stateName, species)
);

drop table if exists checklist;
create table checklist(
    species varchar(50),
    email varchar(50),
    seen boolean,
    constraint userChecklist primary key(species, email)
);

drop table if exists birds;
create table birds(
    species varchar(50),
    commonName varchar(50),
    family varchar(50),
    birdOrder varchar(50),
    wingspan real,
    length real,
    constraint specificBird primary key(species)
);

drop table if exists users;
create table users(
    email varchar(50) primary key,
    firstName varchar(50),
    lastName varchar(50),
    stateName varchar(50),
    groupID integer,
    password varchar(50)
);

drop table if exists states;
create table states(
    stateName varchar(50) primary key,
    region varchar(50)
);