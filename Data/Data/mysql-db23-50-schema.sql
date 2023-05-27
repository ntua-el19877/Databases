

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

DROP SCHEMA IF EXISTS testDB1;
CREATE SCHEMA testDB1;
USE testDB1;


SET SQL_SAFE_UPDATES = 0;

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
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
    Language VARCHAR(50),
    CONSTRAINT `fk_book_school` FOREIGN KEY (SchoolID) REFERENCES School (SchoolID) 
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
--
-- Table structure for table `Author`
--


CREATE TABLE Author (
	BookID INT UNSIGNED,
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    AuthorName VARCHAR(120),
    CONSTRAINT `fk_author_book` FOREIGN KEY (BookID) REFERENCES Book (BookID)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `Category`
--

CREATE TABLE Category (
    BookID INT UNSIGNED,
    LastUpdate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CategoryName VARCHAR(255),
    CONSTRAINT `fk_category_book` FOREIGN KEY (BookID) REFERENCES Book (BookID)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Table structure for table `Image`
--

CREATE TABLE Image (
    BookID INT UNSIGNED,
    LastUpdate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    ImageLink VARCHAR(255),
    CONSTRAINT `fk_image_book` FOREIGN KEY (BookID) REFERENCES Book (BookID)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Table structure for table `Keyword`
--

CREATE TABLE Keyword (
    BookID INT UNSIGNED,
    LastUpdate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    KeywordName VARCHAR(255),
    CONSTRAINT `fk_keyword_book` FOREIGN KEY (BookID) REFERENCES Book (BookID)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


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
    HashedPassword VARCHAR(100),
    CONSTRAINT `fk_user_school` FOREIGN KEY (SchoolID) REFERENCES School (SchoolID)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
    Active VARCHAR(13),
    CONSTRAINT `fk_reservation_school` FOREIGN KEY (SchoolID) REFERENCES School (SchoolID),
    CONSTRAINT `fk_reservation_user` FOREIGN KEY (UserID) REFERENCES User (UserID),
    CONSTRAINT `fk_reservation_book` FOREIGN KEY (BookID) REFERENCES Book (BookID)

)ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
    ApprovalStatus VARCHAR(20),
    CONSTRAINT `fk_review_school` FOREIGN KEY (SchoolID) REFERENCES School (SchoolID),
    CONSTRAINT `fk_review_user` FOREIGN KEY (UserID) REFERENCES User (UserID),
    CONSTRAINT `fk_review_book` FOREIGN KEY (BookID) REFERENCES Book (BookID)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Table structure for table `Summary`
--

CREATE TABLE Summary (
    BookID INT UNSIGNED,
    Summary VARCHAR(5000),
    CONSTRAINT `fk_summary_book` FOREIGN KEY (BookID) REFERENCES Book (BookID)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
