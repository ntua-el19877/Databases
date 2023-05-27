USE testDB1;

-- Gets all distinct books from school based on the category

SELECT MIN(b.BookID) ,b.Title
FROM Book b
Join Category c on b.BookID = c.BookID
where c.CategoryName='Humor' 
    and b.SchoolID='1' 
group by b.Title
order by b.Title;

-- 4.1 Admin check if it is admin
-- 4.1.1

select *
from Reservation
where SchoolID='1'
    and ReservationDate 
        between '2023-06-10'and '2023-06-12';

-- 4.1.2.a

select MIN(a.AuthorName)
from Book b
Join Category c on b.BookID = c.BookID
join Author a on b.BookID = a.BookID
where c.CategoryName='Humor'
group by a.AuthorName
order by a.AuthorName;

-- 4.1.2.b

select Min(r.ReservationID),u.UserID,r.BookID,r.ReservationDate,u.FirstName
from User u
join Reservation r on u.UserID=r.UserID
join Category c on r.BookID=c.BookID
where r.ReservationDate 
        between '2023-05-01'and '2023-06-02'
    and u.Role='Professor'
    and c.CategoryName='Horror'
group by r.ReservationID;

-- 4.1.3

SELECT u.UserID, u.FirstName, u.LastName, COUNT(u.UserID) AS `Borrowed books`
FROM User u
JOIN Reservation r ON u.UserID = r.UserID
WHERE u.Role = 'Professor'
GROUP BY u.UserID, u.FirstName, u.LastName
ORDER BY COUNT(u.UserID);

-- 4.1.4

SELECT a.AuthorName, COUNT(a.AuthorName) AS BookCount
FROM Author a
LEFT JOIN Book b ON a.BookID = b.BookID
LEFT JOIN Reservation r ON b.BookID = r.BookID
GROUP BY a.AuthorName
HAVING BookCount = 0
ORDER BY BookCount;

-- 4.1.5

SELECT u.UserID,u.FirstName,u.LastName, COUNT(r.ReservationID) AS ReservationCount
FROM Reservation r
LEFT JOIN User u on u.UserID=r.UserID
where u.Role='Operator'
GROUP BY u.UserID
HAVING ReservationCount > 20
ORDER BY ReservationCount;

-- Count Operator Reservations

SELECT u.UserID,u.FirstName,u.LastName, COUNT(r.ReservationID) AS ReservationCount
FROM Reservation r
LEFT JOIN User u on u.UserID=r.UserID
where u.Role='Operator'
GROUP BY u.UserID
ORDER BY ReservationCount;

-- 4.1.6

SELECT c1.CategoryName, c2.CategoryName, COUNT(*) AS BorrowingCount
FROM Book b
JOIN Category c1 ON b.BookID = c1.BookID
JOIN Category c2 ON b.BookID = c2.BookID AND c1.CategoryName < c2.CategoryName
JOIN Reservation r ON b.BookID = r.BookID
GROUP BY c1.CategoryName, c2.CategoryName
HAVING c1.CategoryName != c2.CategoryName
ORDER BY BorrowingCount DESC
LIMIT 3;

-- 4.1.7
SELECT a.AuthorName, COUNT(b.BookID) AS BookCount
FROM Author a
JOIN Book b ON a.BookID = b.BookID
GROUP BY a.AuthorName
HAVING BookCount <= (SELECT COUNT(Book.BookID) AS BookCount2
        FROM Author
        JOIN Book ON Author.BookID = Book.BookID
        group by AuthorName
        order by BookCount2 desc
        limit 1 )-5 
ORDER BY BookCount DESC;

-- gets max bookcoun by author
SELECT COUNT(Book.BookID) AS BookCount,AuthorName
        FROM Author
        JOIN Book ON Author.BookID = Book.BookID
        group by AuthorName
        order by BookCount desc
        limit 2 

