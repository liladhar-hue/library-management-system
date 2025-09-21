Library Management System SQL
This repository contains a simple, self-contained SQL script to set up a basic library management system database. The script creates the necessary tables, populates them with sample data, and includes various queries to demonstrate common library management tasks.

Key Features
Database Schema: A well-structured schema for managing Authors, Publishers, Books, Members, and Loans.

Sample Data: The database is pre-populated with data featuring Indian authors and members.

Demonstration Queries: A set of commented queries is included to showcase how to perform operations like fetching book lists, checking available books, and tracking loans.

DML Examples: The script also provides examples of Data Manipulation Language (DML) operations, such as recording new loans and book returns.

Database Schema
The script creates the following tables:

Authors: Stores information about book authors, including their nationality.

Publishers: Contains details about book publishers.

Books: The core table, linking books to their authors and publishers. It also includes an Available status.

Members: Holds information about library members.

Loans: Records all book borrowing transactions, including loan dates, due dates, and return dates.

How to Use
To use this script, simply run the entire file in a SQL client for a relational database like MySQL or PostgreSQL. The script will:

Drop tables (if they exist) to ensure a clean setup.

Create all five tables with their respective columns and constraints.

Insert sample data into each table.

Execute a series of demonstration queries.

You can modify the INSERT statements to add your own data or change the SELECT and UPDATE statements to perform different queries on the database.
