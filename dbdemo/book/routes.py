from datetime import date, timedelta
from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import db ## initially created by __init__.py, needs to be used here
from dbdemo.book import book
from dbdemo.book.forms import BookForm

@book.route("/books")
def getBooks():
    """
    Retrieve books from database
    """
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM Book group by ISBN order by Title")
        column_names = [i[0] for i in cur.description]
        data = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("book.html", data = data, pageTitle = "Book Page")
    except Exception as e:
        print(e)
        abort(500)

@book.route("/4_1_1")
def get4_1_1():
    """
    Retrieve List with the total number of loans per school (Search criteria: year, calendar month, e.g. January).
    """
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    exec_str=f"select SchoolID,COUNT(*) as NumberOfLoans\
                from Reservation\
                where ReservationDate \
                between '{start_date}'and '{end_date}'\
                group by SchoolID\
                order by SchoolID\
                ;"

    try:
        cur = db.connection.cursor()
        cur.execute(exec_str)
        column_names = [i[0] for i in cur.description]
        data = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("4_1_1.html", data = data, pageTitle = "4.1.1")
    except Exception as e:
        print(e)
        abort(500)


@book.route("/4_1_2a")
def get4_1_2a():
    """
    For a given book category (user-selected), which authors belong to it
    """
    Category = request.args.get("Category")
    exec_str=f"select MIN(a.AuthorName) as Authors\
                from Book b\
                Join Category c on b.BookID = c.BookID\
                join Author a on b.BookID = a.BookID\
                where c.CategoryName='{Category}'\
                group by a.AuthorName\
                order by a.AuthorName;"

    try:
        cur = db.connection.cursor()
        cur.execute(exec_str)
        column_names = [i[0] for i in cur.description]
        data = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("4_1_2a.html", data = data, pageTitle = "4.1.2a")
    except Exception as e:
        print(e)
        abort(500)

@book.route("/4_1_2b")
def get4_1_2b():
    """
    For a given book category (user-selected),  which teachers have borrowed books from that category in the last year
    """

    current_date = date.today()
    formatted_date = current_date.strftime("%Y-%m-%d")
    one_year_ago = current_date - timedelta(days=365)
    formatted_date2 = one_year_ago.strftime("%Y-%m-%d")
    Category = request.args.get("Category")
    exec_str=f"select u.UserID,u.FirstName,u.LastName\
                from User u\
                join Reservation r on u.UserID=r.UserID\
                join Category c on r.BookID=c.BookID\
                where r.ReservationDate \
                        between '{formatted_date2}'and '{formatted_date}'\
                    and u.Role='Professor'\
                    and c.CategoryName='{Category}'\
                    AND r.Active != 'Declined'\
                    AND r.Active != 'Pending'\
                group by r.ReservationID;"

    try:
        cur = db.connection.cursor()
        cur.execute(exec_str)
        column_names = [i[0] for i in cur.description]
        data = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("4_1_2b.html", data = data, pageTitle = "4.1.2b")
    except Exception as e:
        print(e)
        abort(500)

@book.route("/4_1_3")
def get4_1_3():
    """
    Find teachers who have borrowed the most books and the number of books    
    """

    exec_str=f"SELECT u.UserID, u.FirstName, u.LastName, COUNT(u.UserID) AS Borrowed_books\
                FROM User u\
                JOIN Reservation r ON u.UserID = r.UserID\
                WHERE u.Role = 'Professor'\
                        AND r.Active != 'Declined'\
                        AND r.Active != 'Pending'\
                GROUP BY u.UserID, u.FirstName, u.LastName\
                ORDER BY Borrowed_books DESC,u.FirstName,u.LastName;"

    try:
        cur = db.connection.cursor()
        cur.execute(exec_str)
        column_names = [i[0] for i in cur.description]
        data = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("4_1_3.html", data = data, pageTitle = "4.1.3")
    except Exception as e:
        print(e)
        abort(500)

@book.route("/4_1_4")
def get4_1_4():
    """
    Find authors whose books have not been borrowed    
    """

    exec_str=f"select a1.AuthorName\
                from (select a1.AuthorName \
                from Author a1\
                        group by a1.AuthorName) a1\
                WHERE a1.AuthorName NOT IN (\
                        SELECT a.AuthorName\
                        FROM Author a\
                        JOIN Book b ON a.BookID = b.BookID\
                        JOIN Reservation r ON b.BookID = r.BookID\
                        WHERE r.Active != 'Declined'\
                            AND r.Active != 'Pending'\
                        GROUP BY a.AuthorName\
                );"

    try:
        cur = db.connection.cursor()
        cur.execute(exec_str)
        column_names = [i[0] for i in cur.description]
        data = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("4_1_4.html", data = data, pageTitle = "4.1.4")
    except Exception as e:
        print(e)
        abort(500)

@book.route("/4_1_5")
def get4_1_5():
    """
    Which operators have loaned the same number of books in a year with more than 20 loans?  
    """

    exec_str=f"SELECT t.ReservationPerSchoolCount, GROUP_CONCAT(t.SchoolLibraryOperatorFullName) AS SchoolsWithSameCount\
                FROM (\
                    SELECT s.SchoolLibraryOperatorFullName, s.SchoolID, COUNT(*) AS ReservationPerSchoolCount\
                    FROM Reservation r\
                    JOIN School s ON s.SchoolID = r.SchoolID\
                    WHERE r.Active != 'Declined'\
                        AND r.Active != 'Pending'\
                    GROUP BY r.SchoolID\
                    HAVING ReservationPerSchoolCount > 20\
                ) t\
                GROUP BY t.ReservationPerSchoolCount\
                HAVING COUNT(*) > 1;"

    try:
        cur = db.connection.cursor()
        cur.execute(exec_str)
        column_names = [i[0] for i in cur.description]
        data = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("4_1_5.html", data = data, pageTitle = "4.1.5")
    except Exception as e:
        print(e)
        abort(500)

@book.route("/4_1_6")
def get4_1_6():
    """
    Many books cover more than one category. Among field pairs (e.g., history and poetry) that 
    are common in books, find the top-3 pairs that appeared in borrowings    
    """

    exec_str=f"SELECT c1.CategoryName as cat1, c2.CategoryName as cat2, COUNT(*) AS BorrowingCount\
                FROM Book b\
                JOIN Category c1 ON b.BookID = c1.BookID\
                JOIN Category c2 ON b.BookID = c2.BookID AND c1.CategoryName < c2.CategoryName\
                JOIN Reservation r ON b.BookID = r.BookID\
                WHERE r.Active != 'Declined'\
                    AND r.Active != 'Pending'\
                GROUP BY c1.CategoryName, c2.CategoryName\
                HAVING c1.CategoryName != c2.CategoryName\
                ORDER BY BorrowingCount DESC\
                LIMIT 3;"

    try:
        cur = db.connection.cursor()
        cur.execute(exec_str)
        column_names = [i[0] for i in cur.description]
        data = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("4_1_6.html", data = data, pageTitle = "4.1.6")
    except Exception as e:
        print(e)
        abort(500)

@book.route("/4_1_7")
def get4_1_7():
    """
    Find all authors who have written at least 5 books less than the author with the most books.
    """

    exec_str=f"SELECT a.AuthorName, COUNT(*) AS BookCount\
                FROM Author a\
                JOIN Book b ON a.BookID = b.BookID\
                GROUP BY a.AuthorName\
                HAVING BookCount <= (SELECT COUNT(*) AS BookCount2\
                        FROM Author\
                        JOIN Book ON Author.BookID = Book.BookID\
                        group by AuthorName\
                        order by BookCount2 desc\
                        limit 1 )-5 \
                ORDER BY BookCount DESC;"

    try:
        cur = db.connection.cursor()
        cur.execute(exec_str)
        column_names = [i[0] for i in cur.description]
        data = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("4_1_7.html", data = data, pageTitle = "4.1.7")
    except Exception as e:
        print(e)
        abort(500)

@book.route("/4_2_1")
def get4_2_1():
    """
    Find all authors who have written at least 5 books less than the author with the most books.
    """
    OperatorSchoolID = request.args.get("OperatorSchoolID")

    Title = request.args.get("Title")
    Author = request.args.get("Author")
    Category = request.args.get("Category")
    BookCount=request.args.get("BookCount")

    Title_str=f"and Book.Title = '{Title}'"
    Author_str=f"and Author.AuthorName = '{Author}'"
    Category_str=f"and Category.CategoryName = '{Category}'"
    if Title=='' or Title=='__Title__':
        Title_str=''
    if Author=='' or Author=='__Author__':
        Author_str=''
    if Category=='' or Category=='__Category__':
        Category_str=''
    if BookCount=='' or BookCount=='__BookCount__':
        Books_str=''
    else:
        try:       
            Books_str=f"HAVING BookCount = {int(BookCount)}"
        except:
            Books_str=''

    exec_str=f"SELECT Book.Title,Count(*) as BookCount\
                FROM Book\
                JOIN Author ON Book.BookID = Author.BookID\
                JOIN Category ON Book.BookID = Category.BookID\
                WHERE Book.SchoolID='{OperatorSchoolID}'\
                    {Title_str}\
                    {Author_str}\
                    {Category_str}\
                group by Book.ISBN\
                {Books_str}\
                order by Book.Title"

    try:
        cur = db.connection.cursor()
        cur.execute(exec_str)
        column_names = [i[0] for i in cur.description]
        data = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("4_2_1.html", data = data, pageTitle = "4.2.1")
    except Exception as e:
        print(e)
        abort(500)

@book.route("/4_2_2")
def get4_2_2():
    """
    Find all borrowers who own at least one book and have delayed its return. (Search criteria: 
    First Name, Last Name, Delay Days).    
    """
    OperatorSchoolID = request.args.get("OperatorSchoolID")

    FirstName = request.args.get("FirstName")
    LastName = request.args.get("LastName")
    DelayedDays = request.args.get("DelayedDays")

    current_date = date.today()
    formatted_date = current_date.strftime("%Y-%m-%d")

    FirstName_str=f"AND User.FirstName='{FirstName}'"
    LastName_str=f"AND User.LastName='{LastName}'"
    
    #insert only if not defalut or empty value
    if FirstName=='' or FirstName=='__FirstName__':
        FirstName_str=''
    if LastName=='' or LastName=='__LastName__':
        LastName_str=''
    if DelayedDays=='' or DelayedDays=='__DelayedDays__':
        DelayedDays_str=''
    else:
        DelayedDays_toDate=current_date-timedelta(days=int(DelayedDays))
        formatted_date2=DelayedDays_toDate.strftime("%Y-%m-%d")
        DelayedDays_str=f"AND Reservation.ExpirationDate='{formatted_date2}'"

    exec_str=f"SELECT DISTINCT User.FirstName, User.LastName,GROUP_CONCAT( Reservation.ExpirationDate) as ExpDates\
                FROM User \
                JOIN Reservation ON User.UserID = Reservation.UserID\
                JOIN Book ON Reservation.BookID = Book.BookID\
                WHERE Reservation.ExpirationDate < '{formatted_date}'\
                    AND Reservation.Active != 'Declined'\
                    AND Reservation.Active != 'Pending'\
                    AND User.SchoolID='{OperatorSchoolID}'\
                    {FirstName_str}\
                    {LastName_str}\
                    {DelayedDays_str}\
                GROUP BY User.FirstName, User.LastName\
                ORDER BY User.FirstName, User.LastName;"

    try:
        cur = db.connection.cursor()
        cur.execute(exec_str)
        column_names = [i[0] for i in cur.description]
        data = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("4_2_2.html", data = data, pageTitle = "4.2.2")
    except Exception as e:
        print(e)
        abort(500)

@book.route("/4_2_3")
def get4_2_3():
    """
    Average Ratings per borrower and category (Search criteria: user/category)  
    """
    OperatorSchoolID = request.args.get("OperatorSchoolID")

    UserID = request.args.get("UserID")
    Category = request.args.get("Category")

    UserID_str=f"AND User.UserID='{UserID}'"
    Category_str=f"AND Category.CategoryName='{Category}'"
    
    #insert only if not defalut or empty value
    if UserID=='' or UserID=='__UserID__':
        UserID_str=''
    if Category=='' or Category=='__Category__':
        Category_str=''

    exec_str=f"SELECT User.UserID,User.FirstName, User.LastName, AVG(Review.Rating) AS AverageRating\
                FROM User\
                JOIN Review ON User.UserID = Review.UserID\
                WHERE User.SchoolID='{OperatorSchoolID}'\
                    AND Review.ApprovalStatus='Approved'\
                    {UserID_str}\
                GROUP BY User.UserID\
                order by AverageRating desc,User.FirstName, User.LastName ;"

    exec_str2=f"SELECT Category.CategoryName, AVG(Review.Rating) AS AverageRating\
                FROM Review\
                JOIN Book ON Review.BookID = Book.BookID\
                JOIN Category ON Category.BookID = Book.BookID\
                WHERE Review.SchoolID='{OperatorSchoolID}'\
                    AND Review.ApprovalStatus='Approved'\
                    {Category_str}\
                GROUP BY Category.CategoryName\
                order by AverageRating desc,Category.CategoryName ;"
    try:
        cur = db.connection.cursor()
        cur.execute(exec_str)
        column_names = [i[0] for i in cur.description]
        data = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        
        cur = db.connection.cursor()
        cur.execute(exec_str2)
        column_names = [i[0] for i in cur.description]
        data2 = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()

        return render_template("4_2_3.html", data = data, data2=data2, pageTitle = "4.2.3")
    except Exception as e:
        print(e)
        abort(500)

@book.route("/4_3_1")
def get4_3_1():
    """
    List with all books (Search criteria: title/category/author), ability to select a book and create 
    a reservation request.
    """
    form = BookForm()
    UserSchoolID = request.args.get("UserSchoolID")

    Title = request.args.get("Title")
    Author = request.args.get("Author")
    Category = request.args.get("Category")

    Title_str=f"AND Book.Title = '{Title}'"
    Author_str=f"AND Author.AuthorName = '{Author}'"
    Category_str=f"AND Category.CategoryName = '{Category}'"

    #insert only if not defalut or empty value
    if Title=='' or Title=='__Title__':
        Title_str=''
    if Author=='' or Author=='__Author__':
        Author_str=''
    if Category=='' or Category=='__Category__':
        Category_str=''

    exec_str=f"SELECT Book.Title, Book.ISBN, COUNT(*) as BookCount, \
                GROUP_CONCAT(IF(Book.Inventory = True, Book.BookID, NULL)) as BookIDs\
                FROM Book\
                JOIN Author ON Book.BookID = Author.BookID\
                JOIN Category ON Book.BookID = Category.BookID\
                WHERE Book.SchoolID='{UserSchoolID}'\
                {Title_str}\
                {Author_str}\
                {Category_str}\
                group by Book.ISBN\
                order by Book.Title\
                ;"

    try:
        cur = db.connection.cursor()
        cur.execute(exec_str)
        column_names = [i[0] for i in cur.description]
        data = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("4_3_1.html", data = data,UserSchoolID= UserSchoolID,pageTitle = "4.3.1", form = form)
    except Exception as e:
        print(e)
        abort(500)



@book.route("/4_3_1/ReservationRequest", methods = ["POST"])
def updateStudent():
    """
    Update a student in the database, by id
    """
    form = BookForm() ## see createStudent for explanation
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query=f"Insert into Reservation \
                (`SchoolID`,`UserID`,`BookID`,`ReservationDate`,\
                `ExpirationDate`,`Active`) \
                Values \
                ('{updateData['schoolID'].data}','{updateData['userID'].data}'\
                ,'{updateData['bookID'].data}',Null,Null,'Pending') ;"
        print(query)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Reservation posted successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("book.get4_3_1"))


@book.route("/4_3_2")
def get4_3_2():
    """
    List of all books borrowed by this user.
    """
    UserID = request.args.get("UserID")


    exec_str=f"SELECT User.UserID, Book.Title\
                FROM Book\
                JOIN Reservation ON Book.BookID = Reservation.BookID\
                JOIN User ON Reservation.UserID = User.UserID\
                WHERE User.UserID='{UserID}'\
                    and Reservation.Active != 'Declined'\
                    and Reservation.Active != 'Pending'\
                order by User.UserID;"

    try:
        cur = db.connection.cursor()
        cur.execute(exec_str)
        column_names = [i[0] for i in cur.description]
        data = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("4_3_2.html", data = data,pageTitle = "4.3.2")
    except Exception as e:
        print(e)
        abort(500)