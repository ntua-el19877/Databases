

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

DROP SCHEMA IF EXISTS testDB1;
CREATE SCHEMA testDB1;
USE testDB1;


--
-- Table structure for table `Author`
--


SET SQL_SAFE_UPDATES = 0;
CREATE TABLE Author (
    ISBN VARCHAR(13) NOT NULL,
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    AuthorName VARCHAR(120),
    KEY idx_author_isbn (ISBN)
);

--
-- Table structure for table `Book`
--

CREATE TABLE Book (
    BookID INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    LastUpdate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    SchoolID INT UNSIGNED NOT NULL,
    Title VARCHAR(255),
    Publisher VARCHAR(255),
    ISBN VARCHAR(13) NOT NULL,
    NumOfPages INT,
    Inventory BOOLEAN,
    Language VARCHAR(50)
);

--
-- Table structure for table `Category`
--

CREATE TABLE Category (
    ISBN VARCHAR(13) NOT NULL,
    LastUpdate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CategoryName VARCHAR(255),
    KEY idx_author_isbn (ISBN)
);

--
-- Table structure for table `Image`
--

CREATE TABLE Image (
    ISBN VARCHAR(13) NOT NULL,
    LastUpdate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    ImageLink VARCHAR(255),
    KEY idx_author_isbn (ISBN)
);

--
-- Table structure for table `Keyword`
--

CREATE TABLE Keyword (
    ISBN VARCHAR(13) NOT NULL,
    LastUpdate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    KeywordName VARCHAR(255),
    KEY idx_author_isbn (ISBN)
);

--
-- Table structure for table `Reservation`
--

CREATE TABLE Reservation (
    ReservationID INT UNSIGNED PRIMARY KEY AUTO_INCREMENT , 
    LastUpdate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    SchoolID INT UNSIGNED NOT NULL,
    UserID INT UNSIGNED NOT NULL,
    BookID INT UNSIGNED NOT NULL,
    ReservationDate Date,
    ExpirationDate Date,
    Active VARCHAR(13)
);

--
-- Table structure for table `Review`
--

CREATE TABLE Review (
    ReviewID INT UNSIGNED PRIMARY KEY AUTO_INCREMENT , 
    LastUpdate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    SchoolID INT UNSIGNED NOT NULL,
    UserID INT UNSIGNED NOT NULL,
    BookID INT UNSIGNED NOT NULL,
    Rating INT UNSIGNED,
    Comment VARCHAR(255),
    ApprovalStatus VARCHAR(20)
);

--
-- Table structure for table `School`
--

CREATE TABLE School (
    SchoolID INT UNSIGNED PRIMARY KEY AUTO_INCREMENT , 
    LastUpdate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    SchoolName VARCHAR(50),
    `Address` VARCHAR(50),
    `City` VARCHAR(50),
    PhoneNumber VARCHAR(20),
    Email VARCHAR(50),
    SchoolLibraryOperatorFullName VARCHAR(50),
    SchoolDirectorFullName VARCHAR(50)
);

--
-- Table structure for table `Summary`
--

CREATE TABLE Summary (
    ISBN VARCHAR(13),
    Summary VARCHAR(5000)
);

--
-- Table structure for table `User`
--

CREATE TABLE USER(
    UserID INT UNSIGNED PRIMARY KEY AUTO_INCREMENT ,
    SchoolID INT UNSIGNED,
    Username VARCHAR(50),
    `Role` VARCHAR(20),
    FirstName VARCHAR(30),
    LastName VARCHAR(30),
    BorrowerCard VARCHAR(13),
    HashedPassword VARCHAR(100)
)