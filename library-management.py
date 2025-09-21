import sqlite3
from datetime import date, timedelta

def create_tables(conn):
    """Creates the necessary tables for the library management system."""
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Authors (
            AuthorID INTEGER PRIMARY KEY AUTOINCREMENT,
            AuthorName TEXT NOT NULL,
            Nationality TEXT
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Publishers (
            PublisherID INTEGER PRIMARY KEY AUTOINCREMENT,
            PublisherName TEXT NOT NULL,
            City TEXT
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Books (
            BookID INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT NOT NULL,
            AuthorID INTEGER,
            PublisherID INTEGER,
            PublicationYear INTEGER,
            ISBN TEXT UNIQUE,
            Available INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (AuthorID) REFERENCES Authors(AuthorID),
            FOREIGN KEY (PublisherID) REFERENCES Publishers(PublisherID)
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Members (
            MemberID INTEGER PRIMARY KEY AUTOINCREMENT,
            MemberName TEXT NOT NULL,
            Address TEXT,
            PhoneNumber TEXT,
            Email TEXT UNIQUE
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Loans (
            LoanID INTEGER PRIMARY KEY AUTOINCREMENT,
            BookID INTEGER,
            MemberID INTEGER,
            LoanDate TEXT NOT NULL,
            DueDate TEXT NOT NULL,
            ReturnDate TEXT,
            FOREIGN KEY (BookID) REFERENCES Books(BookID),
            FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
        );
    ''')
    conn.commit()
    print("Database tables created successfully.")

def populate_data(conn):
    """Populates the tables with sample Indian data."""
    cursor = conn.cursor()
    
    # Check if data already exists to prevent duplicates
    cursor.execute("SELECT COUNT(*) FROM Authors")
    if cursor.fetchone()[0] > 0:
        return

    # Insert sample data into Authors
    authors = [
        ('Arundhati Roy', 'Indian'),
        ('Chetan Bhagat', 'Indian'),
        ('R.K. Narayan', 'Indian'),
        ('Rabindranath Tagore', 'Indian'),
        ('Amrita Pritam', 'Indian')
    ]
    cursor.executemany("INSERT INTO Authors (AuthorName, Nationality) VALUES (?, ?)", authors)

    # Insert sample data into Publishers
    publishers = [
        ('Bloomsbury', 'London'),
        ('Penguin Books', 'New York'),
        ('Scribner', 'New York'),
        ('HarperCollins', 'New York'),
        ('Vintage Books', 'London')
    ]
    cursor.executemany("INSERT INTO Publishers (PublisherName, City) VALUES (?, ?)", publishers)

    # Insert sample data into Books
    books = [
        ('The God of Small Things', 1, 4, 1997, '9780060931206'),
        ('Five Point Someone', 2, 2, 2005, '9788129107931'),
        ('The Guide', 3, 2, 1958, '9780143099953'),
        ('Gitanjali', 4, 5, 1910, '9780486296182'),
        ('Pinjar', 5, 1, 1950, '9788170281691')
    ]
    cursor.executemany("INSERT INTO Books (Title, AuthorID, PublisherID, PublicationYear, ISBN) VALUES (?, ?, ?, ?, ?)", books)

    # Insert sample data into Members
    members = [
        ('Rohan Sharma', '456 Park Street', '987-654-3210', 'rohan.s@example.com'),
        ('Priya Singh', '789 Defence Colony', '999-888-7777', 'priya.s@example.com'),
        ('Sameer Khan', '101 MG Road', '981-234-5678', 'sameer.k@example.com')
    ]
    cursor.executemany("INSERT INTO Members (MemberName, Address, PhoneNumber, Email) VALUES (?, ?, ?, ?, ?)", members)

    conn.commit()
    print("Sample data populated successfully.")

def view_all_books(conn):
    """Displays a list of all books with author and publisher names."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT B.Title, A.AuthorName, P.PublisherName, B.Available
        FROM Books AS B
        JOIN Authors AS A ON B.AuthorID = A.AuthorID
        JOIN Publishers AS P ON B.PublisherID = P.PublisherID
    ''')
    books = cursor.fetchall()
    print("\n--- All Books ---")
    if books:
        for book in books:
            availability = "Available" if book[3] == 1 else "On Loan"
            print(f"Title: {book[0]}, Author: {book[1]}, Publisher: {book[2]}, Status: {availability}")
    else:
        print("No books found.")
    print("-----------------\n")

def view_books_on_loan(conn):
    """Displays a list of all books currently on loan."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT B.Title, M.MemberName, L.LoanDate, L.DueDate
        FROM Loans AS L
        JOIN Books AS B ON L.BookID = B.BookID
        JOIN Members AS M ON L.MemberID = M.MemberID
        WHERE L.ReturnDate IS NULL
    ''')
    loans = cursor.fetchall()
    print("\n--- Books on Loan ---")
    if loans:
        for loan in loans:
            print(f"Title: {loan[0]}, Loaned to: {loan[1]}, Loan Date: {loan[2]}, Due Date: {loan[3]}")
    else:
        print("No books are currently on loan.")
    print("---------------------\n")

def loan_book(conn):
    """Records a new book loan."""
    try:
        book_title = input("Enter the title of the book to loan: ")
        member_name = input("Enter the name of the member: ")

        cursor = conn.cursor()
        cursor.execute("SELECT BookID, Available FROM Books WHERE Title = ?", (book_title,))
        book = cursor.fetchone()
        
        if not book:
            print("Error: Book not found.")
            return
        
        if book[1] == 0:
            print("Error: This book is currently on loan.")
            return

        cursor.execute("SELECT MemberID FROM Members WHERE MemberName = ?", (member_name,))
        member = cursor.fetchone()

        if not member:
            print("Error: Member not found.")
            return

        book_id = book[0]
        member_id = member[0]
        loan_date = date.today().isoformat()
        due_date = (date.today() + timedelta(days=30)).isoformat()

        cursor.execute("INSERT INTO Loans (BookID, MemberID, LoanDate, DueDate) VALUES (?, ?, ?, ?)", 
                       (book_id, member_id, loan_date, due_date))
        cursor.execute("UPDATE Books SET Available = 0 WHERE BookID = ?", (book_id,))
        conn.commit()
        print(f"Loan recorded successfully for {book_title} to {member_name}.")
    except Exception as e:
        print(f"An error occurred: {e}")

def return_book(conn):
    """Records the return of a book."""
    try:
        book_title = input("Enter the title of the book to return: ")
        member_name = input("Enter the name of the member who is returning the book: ")

        cursor = conn.cursor()
        cursor.execute("SELECT BookID FROM Books WHERE Title = ?", (book_title,))
        book = cursor.fetchone()

        cursor.execute("SELECT MemberID FROM Members WHERE MemberName = ?", (member_name,))
        member = cursor.fetchone()

        if not book or not member:
            print("Error: Book or member not found.")
            return

        book_id = book[0]
        member_id = member[0]
        return_date = date.today().isoformat()

        cursor.execute("UPDATE Loans SET ReturnDate = ? WHERE BookID = ? AND MemberID = ? AND ReturnDate IS NULL", 
                       (return_date, book_id, member_id))
        
        if cursor.rowcount == 0:
            print("Error: No active loan found for this book and member combination.")
            return

        cursor.execute("UPDATE Books SET Available = 1 WHERE BookID = ?", (book_id,))
        conn.commit()
        print(f"Book '{book_title}' returned successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    conn = None
    try:
        conn = sqlite3.connect('library.db')
        
        create_tables(conn)
        populate_data(conn)

        while True:
            print("\n--- Library Management System ---")
            print("1. View all books")
            print("2. View books on loan")
            print("3. Loan a book")
            print("4. Return a book")
            print("5. Exit")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                view_all_books(conn)
            elif choice == '2':
                view_books_on_loan(conn)
            elif choice == '3':
                loan_book(conn)
            elif choice == '4':
                return_book(conn)
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()
            
if __name__ == '__main__':
    main()
