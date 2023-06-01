from datetime import date, timedelta
from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import db ## initially created by __init__.py, needs to be used here
from dbdemo.book import book

@book.route("/books")
def getBooks():
    """
    Retrieve books from database
    """
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM Book")
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










# @grade.route("/grades/delete/<int:gradeID>", methods = ["POST"])
# def deleteGrade(gradeID):
#     """
#     Delete grade by id from database
#     """
#     query = f"DELETE FROM grades WHERE id = {gradeID};"
#     try:
#         cur = db.connection.cursor()
#         cur.execute(query)
#         db.connection.commit()
#         cur.close()
#         flash("Grade deleted successfully", "primary")
#     except Exception as e:
#         flash(str(e), "danger")
#     return redirect(url_for("grade.getGrades"))

# @grade.route("/grades/create", methods = ["GET", "POST"]) ## "GET" by default
# def createGrade():
#     """
#     Create new grade in the database
#     """
#     form = GradeForm() ## This is an object of a class that inherits FlaskForm
#     ## which in turn inherits Form from wtforms
#     ## https://flask-wtf.readthedocs.io/en/0.15.x/api/#flask_wtf.FlaskForm
#     ## https://wtforms.readthedocs.io/en/2.3.x/forms/#wtforms.form.Form
#     ## If no form data is specified via the formdata parameter of Form
#     ## (it isn't here) it will implicitly use flask.request.form and flask.request.files.
#     ## So when this method is called because of a GET request, the request
#     ## object's form field will not contain user input, whereas if the HTTP
#     ## request type is POST, it will implicitly retrieve the data.
#     ## https://flask-wtf.readthedocs.io/en/0.15.x/form/
#     ## Alternatively, in the case of a POST request, the data could have between
#     ## retrieved directly from the request object: request.form.get("key name")

#     ## when the form is submitted
#     if(request.method == "POST"):
#         newGrade = form.__dict__

#         query = "INSERT INTO grades(course_name, grade, student_id) VALUES ('{}', '{}', '{}');".format(
#             newGrade['course_name'].data,
#             newGrade['grade'].data,
#             newGrade['student_id'].data
#         )

#         try:
#             cur = db.connection.cursor()
#             cur.execute(query)
#             db.connection.commit()
#             cur.close()
#             flash("Grade inserted successfully", "success")
#             return redirect(url_for("index"))
#         except Exception as e: ## OperationalError
#             flash(str(e), "danger")
#             print(str(e))
#     ## else, response for GET request
#     else:
#         try:
#             cur = db.connection.cursor()
#             cur.execute('SELECT id, CONCAT(last_name, ", ", first_name) FROM students;')
#             form.student_id.choices = list(cur.fetchall())
#             ## each tuple in the above list is in the format (id, full name),
#             ## and will be rendered in html as an <option> of the <select>
#             ## element, with value = id and content = full_name
#             cur.close()
#             return render_template("create_grade.html", pageTitle = "Create Grade", form = form)
#         except Exception as e: ## OperationalError
#             flash(str(e), "danger")
