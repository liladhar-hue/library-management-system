-- Drop tables to ensure a clean slate for running the script multiple times
DROP TABLE IF EXISTS Loans;
DROP TABLE IF EXISTS Books;
DROP TABLE IF EXISTS Members;
DROP TABLE IF EXISTS Authors;
DROP TABLE IF EXISTS Publishers;

--
-- Table structure for `Authors`
--
CREATE TABLE Authors (
    AuthorID INT PRIMARY KEY AUTO_INCREMENT,
    AuthorName VARCHAR(255) NOT NULL,
    Nationality VARCHAR(100)
);

--
-- Table structure for `Publishers`
--
CREATE TABLE Publishers (
    PublisherID INT PRIMARY KEY AUTO_INCREMENT,
    PublisherName VARCHAR(255) NOT NULL,
    City VARCHAR(100)
);

--
-- Table structure for `Books`
--
CREATE TABLE Books (
    BookID INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(255) NOT NULL,
    AuthorID INT,
    PublisherID INT,
    PublicationYear YEAR,
    ISBN VARCHAR(20) UNIQUE,
    Available BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (AuthorID) REFERENCES Authors(AuthorID),
    FOREIGN KEY (PublisherID) REFERENCES Publishers(PublisherID)
);

--
-- Table structure for `Members`
--
CREATE TABLE Members (
    MemberID INT PRIMARY KEY AUTO_INCREMENT,
    MemberName VARCHAR(255) NOT NULL,
    Address VARCHAR(255),
    PhoneNumber VARCHAR(20),
    Email VARCHAR(255) UNIQUE
);

--
-- Table structure for `Loans`
--
CREATE TABLE Loans (
    LoanID INT PRIMARY KEY AUTO_INCREMENT,
    BookID INT,
    MemberID INT,
    LoanDate DATE NOT NULL,
    DueDate DATE NOT NULL,
    ReturnDate DATE,
    FOREIGN KEY (BookID) REFERENCES Books(BookID),
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);

--
-- Insert sample data into `Authors` (Indian Writers)
--
INSERT INTO Authors (AuthorName, Nationality) VALUES
('Arundhati Roy', 'Indian'),
('Chetan Bhagat', 'Indian'),
('R.K. Narayan', 'Indian'),
('Rabindranath Tagore', 'Indian'),
('Amrita Pritam', 'Indian');

--
-- Insert sample data into `Publishers` (kept same as previous version)
--
INSERT INTO Publishers (PublisherName, City) VALUES
('Bloomsbury', 'London'),
('Penguin Books', 'New York'),
('Scribner', 'New York'),
('HarperCollins', 'New York'),
('Vintage Books', 'London');

--
-- Insert sample data into `Books` (Indian Writers' books)
--
INSERT INTO Books (Title, AuthorID, PublisherID, PublicationYear, ISBN, Available) VALUES
('The God of Small Things', 1, 4, 1997, '9780060931206', TRUE),
('Five Point Someone', 2, 2, 2005, '9788129107931', TRUE),
('The Guide', 3, 2, 1958, '9780143099953', TRUE),
('Gitanjali', 4, 5, 1910, '9780486296182', FALSE),
('Pinjar', 5, 1, 1950, '9788170281691', TRUE),
('The Guide (Abridged)', 3, 2, 1965, '9780143099960', FALSE);

--
-- Insert sample data into `Members` (Indian names)
--
INSERT INTO Members (MemberName, Address, PhoneNumber, Email) VALUES
('Rohan Sharma', '456 Park Street', '987-654-3210', 'rohan.s@example.com'),
('Priya Singh', '789 Defence Colony', '999-888-7777', 'priya.s@example.com'),
('Sameer Khan', '101 MG Road', '981-234-5678', 'sameer.k@example.com');

--
-- Insert sample data into `Loans`
--
INSERT INTO Loans (BookID, MemberID, LoanDate, DueDate, ReturnDate) VALUES
(4, 1, '2024-09-10', '2024-10-10', NULL), -- 'Gitanjali' loaned to Member 1 (Rohan Sharma)
(6, 2, '2024-09-05', '2024-10-05', NULL); -- 'The Guide (Abridged)' loaned to Member 2 (Priya Singh)

--
-- Queries to demonstrate library management tasks
--

-- 1. Get a list of all books with author and publisher names
SELECT
    B.Title,
    A.AuthorName,
    P.PublisherName,
    B.PublicationYear,
    B.Available
FROM
    Books AS B
JOIN
    Authors AS A ON B.AuthorID = A.AuthorID
JOIN
    Publishers AS P ON B.PublisherID = P.PublisherID;

-- 2. Find all books currently available for loan
SELECT
    Title
FROM
    Books
WHERE
    Available = TRUE;

-- 3. Show all books currently on loan, including the member's name and due date
SELECT
    B.Title,
    M.MemberName,
    L.LoanDate,
    L.DueDate
FROM
    Loans AS L
JOIN
    Books AS B ON L.BookID = B.BookID
JOIN
    Members AS M ON L.MemberID = M.MemberID
WHERE
    L.ReturnDate IS NULL;

-- 4. Find all books written by 'R.K. Narayan'
SELECT
    B.Title
FROM
    Books AS B
JOIN
    Authors AS A ON B.AuthorID = A.AuthorID
WHERE
    A.AuthorName = 'R.K. Narayan';

-- 5. Show the loan history for a specific member ('Rohan Sharma')
SELECT
    B.Title,
    L.LoanDate,
    L.DueDate,
    L.ReturnDate
FROM
    Loans AS L
JOIN
    Books AS B ON L.BookID = B.BookID
JOIN
    Members AS M ON L.MemberID = M.MemberID
WHERE
    M.MemberName = 'Rohan Sharma';

-- 6. Count how many books each member has on loan
SELECT
    M.MemberName,
    COUNT(L.LoanID) AS BooksOnLoan
FROM
    Members AS M
JOIN
    Loans AS L ON M.MemberID = L.MemberID
WHERE
    L.ReturnDate IS NULL
GROUP BY
    M.MemberName;

--
-- Examples of DML (Data Manipulation Language) operations
--

-- 7. Record a new loan (e.g., Priya Singh borrowing 'Five Point Someone')
-- First, find an available book
SELECT BookID FROM Books WHERE Title = 'Five Point Someone';

-- Then, find Priya Singh's MemberID
SELECT MemberID FROM Members WHERE MemberName = 'Priya Singh';

-- Then, insert the new loan and update the book's availability
INSERT INTO Loans (BookID, MemberID, LoanDate, DueDate, ReturnDate) VALUES
(2, 2, '2024-09-20', '2024-10-20', NULL);

UPDATE Books SET Available = FALSE WHERE BookID = 2;

-- 8. Record the return of a book (e.g., Rohan Sharma returning 'Gitanjali')
UPDATE Loans SET ReturnDate = '2024-09-21' WHERE BookID = 4 AND MemberID = 1;

UPDATE Books SET Available = TRUE WHERE BookID = 4;
