USE testDB1;

-- 4.1 Admin check if it is admin
-- 4.1.1

SELECT SchoolID,COUNT(*) AS NumberOfLoans
FROM Reservation
WHERE ReservationDate 
        BETWEEN '2023-06-10' AND '2023-06-12'
GROUP BY SchoolID
ORDER BY SchoolID;

-- 4.1.2.a

SELECT MIN(a.AuthorName)
FROM Book b
JOIN Category c ON b.BookID = c.BookID
JOIN Author a ON b.BookID = a.BookID
WHERE c.CategoryName='Humor'
GROUP BY a.AuthorName
ORDER BY a.AuthorName;

-- 4.1.2.b

SELECT u.UserID,u.FirstName,u.LastName
FROM User u
JOIN Reservation r ON u.UserID=r.UserID
JOIN Category c ON r.BookID=c.BookID
WHERE r.ReservationDate 
        BETWEEN '2022-06-01'AND '2023-06-01'
        AND u.Role='Professor'
        AND c.CategoryName='History'
        AND r.Active != 'Declined'
        AND r.Active != 'Pending'
GROUP BY r.ReservationID;

-- 4.1.3

SELECT u.UserID, u.FirstName, u.LastName, COUNT(u.UserID) AS Borrowed_books
FROM User u
JOIN Reservation r ON u.UserID = r.UserID
WHERE u.Role = 'Professor'    
        AND r.Active != 'Declined'
        AND r.Active != 'Pending'
GROUP BY u.UserID, u.FirstName, u.LastName
ORDER BY Borrowed_books DESC;


-- 4.1.4


select a1.AuthorName
from (select a1.AuthorName 
        from Author a1
        group by a1.AuthorName) a1
WHERE a1.AuthorName NOT IN (
        SELECT a.AuthorName
        FROM Author a
        JOIN Book b ON a.BookID = b.BookID
        JOIN Reservation r ON b.BookID = r.BookID
        WHERE r.Active != 'Declined'
                AND r.Active != 'Pending'
        GROUP BY a.AuthorName
);

-- 4.1.5

SELECT t.ReservationPerSchoolCount, GROUP_CONCAT(t.SchoolLibraryOperatorFullName) AS SchoolsWithSameCount
FROM (
    SELECT s.SchoolLibraryOperatorFullName, s.SchoolID, COUNT(*) AS ReservationPerSchoolCount
    FROM Reservation r
    JOIN School s ON s.SchoolID = r.SchoolID
    WHERE r.Active != 'Declined'
        AND r.Active != 'Pending'
    GROUP BY r.SchoolID
    HAVING ReservationPerSchoolCount > 20
) t
GROUP BY t.ReservationPerSchoolCount
HAVING COUNT(*) > 1;


-- 4.1.6

SELECT c1.CategoryName, c2.CategoryName, COUNT(*) AS BorrowingCount
FROM Book b
JOIN Category c1 ON b.BookID = c1.BookID
JOIN Category c2 ON b.BookID = c2.BookID AND c1.CategoryName < c2.CategoryName
JOIN Reservation r ON b.BookID = r.BookID
WHERE r.Active != 'Declined'
    AND r.Active != 'Pending'
GROUP BY c1.CategoryName, c2.CategoryName
HAVING c1.CategoryName != c2.CategoryName
ORDER BY BorrowingCount DESC
LIMIT 3;

-- 4.1.7
SELECT a.AuthorName, COUNT(*) AS BookCount
FROM Author a
JOIN Book b ON a.BookID = b.BookID
GROUP BY a.AuthorName
HAVING BookCount <= (SELECT COUNT(*) AS BookCount2
        FROM Author
        JOIN Book ON Author.BookID = Book.BookID
        group by AuthorName
        order by BookCount2 desc
        limit 1 )-5 
ORDER BY BookCount DESC;


 -- 4.2.1.

SELECT Book.Title,Count(*) as BookCount
FROM Book
JOIN Author ON Book.BookID = Author.BookID
JOIN Category ON Book.BookID = Category.BookID
WHERE Book.SchoolID='1'
    and Book.Title = 'Product Engineering'
    and Author.AuthorName = 'Alice Johnson'
    and Category.CategoryName = 'Horror'
group by Book.ISBN
having BookCount = 
order by Book.Title


-- 4.2.2

SELECT DISTINCT User.FirstName, User.LastName,GROUP_CONCAT( Reservation.ExpirationDate)
FROM User 
JOIN Reservation ON User.UserID = Reservation.UserID
JOIN Book ON Reservation.BookID = Book.BookID
WHERE Reservation.ExpirationDate < '2023-06-02'
    AND Reservation.Active != 'Declined'
    AND Reservation.Active != 'Pending'
    AND User.SchoolID=''
    AND User.FirstName=''
    AND User.LastName=''
    AND Reservation.ExpirationDate=''
GROUP BY User.FirstName, User.LastName
ORDER BY User.FirstName, User.LastName;

--4.2.3 a

SELECT User.UserID,User.FirstName, User.LastName, AVG(Review.Rating) AS AverageRating
FROM User
JOIN Review ON User.UserID = Review.UserID
WHERE User.SchoolID='1'
    AND Review.ApprovalStatus='Approved'
    AND User.UserID='3'
GROUP BY User.UserID
order by AverageRating desc,User.FirstName, User.LastName ;

--4.2.3 b

SELECT Category.CategoryName, AVG(Review.Rating) AS AverageRating
FROM Review
JOIN Book ON Review.BookID = Book.BookID
JOIN Category ON Category.BookID = Book.BookID
WHERE Review.SchoolID='1'
    AND Review.ApprovalStatus='Approved'
    AND Category.CategoryName='History'
GROUP BY Category.CategoryName
order by AverageRating desc,Category.CategoryName ;

--4.3.1. 

SELECT Book.Title, Book.ISBN, COUNT(*) AS BookCount, 
       GROUP_CONCAT(IF(Book.Inventory = True, Book.BookID, NULL)) AS BookIDs
FROM Book
JOIN Author ON Book.BookID = Author.BookID
JOIN Category ON Book.BookID = Category.BookID
WHERE Book.SchoolID = '1'
    AND Book.Title = 'Product Engineering'
    AND Author.AuthorName = 'Alice Johnson'
    AND Category.CategoryName = 'Horror'
GROUP BY Book.ISBN
ORDER BY Book.Title;

--4.3.2

SELECT User.UserID, Book.Title
FROM Book
JOIN Reservation ON Book.BookID = Reservation.BookID
JOIN User ON Reservation.UserID = User.UserID
WHERE User.UserID=''
    AND Reservation.Active != 'Declined'
    AND Reservation.Active != 'Pending'
ORDER BY User.UserID;
