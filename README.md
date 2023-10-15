# Online Book Store

Welcome to the Online Book Store project, a simple console-based application for managing an online book store. This README provides an overview of this mini project, features, how to use the application, and database schema details.

## Project Overview

- Project Name: Online Book Store

## Description

The Online Book Store is a Python-based application that simulates the functionality of an online book store. It allows users to perform various tasks, including member registration, browsing books by subject, searching for books by author or title, and checking out items from their cart. This project was developed as part of a course to demonstrate practical skills in working with databases and user interfaces.

## Features

The application provides the following features:

1. **Member Registration:** Users can register as members by providing their personal information, including name, address, email, and password.

2. **Member Login:** Registered members can log in using their email and password.

3. **Browse by Subject:** Users can browse books by subject, and the application displays details like author, title, ISBN, price, and subject.

4. **Search by Author/Title:** Users can search for books by author or title, and the application provides search results with book details.

5. **Cart Management:** Members can add books to their cart, specify quantities, and proceed to checkout.

6. **Checkout Process:** The application allows users to review their cart contents, provides an estimated delivery date, and allows them to confirm and complete the purchase.
## How to Use

To use the Online Book Store application, follow these steps:

1. **Clone the Repository:** Start by cloning the repository to your local device.

2. **Install Required Dependencies:** Ensure you have Python installed, as this application is Python-based. Additionally, make sure you have the required Python packages installed. You can install these packages using pip:

```shell
   pip install mysql-connector-python getpasslib
```

3. **Database Setup:** 
- You'll need to set up a MySQL database. Ensure you have a running MySQL server and create a database named `book_store`.
- Modify the database connection settings in the code to match your MySQL server's host, username, password, and database name (update the `host`, `user`, `password`, and `database` variables in the code).
- You can use the provided schema file and books file to create the tables and populate them.

4. **Run the Application:** Execute the Python script to run the application.

```shell
    python online_book_store.py
```

5. **Main Menu:** The application will present a main menu with options for member login, new member registration, and quitting the application.

6. **Member Registration:** If you're a new member, choose the registration option and provide your details.

7. **Member Login:** Registered members can log in with their email and password.

8. **Browse and Shop:** After logging in, you can browse books by subject, search for books by author or title, add books to your cart, and proceed to checkout.

9. **Checkout:** Review your cart contents, confirm the purchase, and complete the checkout process.

By following these steps, you can explore and interact with the Online Book Store application.
