import mysql.connector
from getpass import getpass
import re
import hashlib
import datetime

# Esatblish a connection to the database

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="book_store"
    )
    if mydb.is_connected():
        print("Connected to the database")
except mysql.connector.Error as err:
    print("Connection error: ", err)
    host = input("Enter the host: ")
    user = input("Enter the username: ")
    password = input("Enter the password: ")
    database = input("Enter the database name: ")
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    if mydb.is_connected():
        print("Connected to the database")

# Cart object
lcl_cart = {
    "userid":   0,
    "isbn":     0,
    "qty":      0
}

# user object we will save everything here not sure if we need all fields
user = {
    "fname":            "",
    "lname":            "",
    "address":          "",
    "city":             "",
    "state":            "",
    "zip":              0,
    "phone":            0,
    "email":            "",
    "userid":           0,
    "password":         "",
    "creditcardtype":   "",
    "creditcardnumber": 0
}
# functions for each menus option


def new_member_registration():
    cursor = mydb.cursor()

    #Regix safe guards
    regex_email = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    regex_phone = "^[0-9]+$"
    regex_zip = "^[0-9]{5}$"

    fname = input("Enter First name: ")
    lname = input("Enter last name: ")
    address = input("Enter the street address: ")
    city = input("Enter the city: ")
    state = input("Enter the state: ")
    zip_code = input("Enter zip code: ")
    phone = input("Enter the phone: ")
    email = input("Enter your email: ")
    pwd = getpass("Enter your password: ")

    if not fname.isalpha():
        print("Invalid first name format. Please enter alphabetic characters only.")
        return

    if not lname.isalpha():
        print("Invalid last name format. Please enter alphabetic characters only.")
        return

    if not address:
        print("Please enter a valid street address.")
        return

    if not city.isalpha():
        print("Invalid city format. Please enter alphabetic characters only.")
        return

    if not state.isalpha():
        print("Invalid state format. Please enter alphabetic characters only.")
        return

    if not re.match(regex_zip, zip_code):
        print("Invalid zip code format. Please enter a valid 5-digit zip code.")
        return

    if not re.match(regex_phone, phone):
        print("Invalid phone number format. Please enter numbers only.")
        return

    if not re.search(regex_email, email):
        print("Invalid email format. Please enter a valid email address.")
        return

    # Check if email is already in use
    cursor.execute("SELECT * FROM members WHERE email = %s", (email,))
    existing_member = cursor.fetchone()
    if existing_member:
        print("The email belongs to another user. Please use a different email.")
        return

    # Hash the password
    hashed_pwd = hashlib.sha256(pwd.encode()).hexdigest()

    # Insert the new member into the member table
    try:
        cursor.execute("INSERT INTO members (fname, lname, address, city, state, zip, phone, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (fname, lname, address, city, state, zip_code, phone, email, hashed_pwd))
        mydb.commit()
        print("You have successfully registered!")
    except mysql.connector.Error as e:
        print("Something went wrong with the registration:", e)
        mydb.rollback()
        return




def new_member_registration():
    cursor = mydb.cursor()
    regex_email = "^[a-z0-9]+[\._]?[ a-z0-9]+[@]\w+[. ]\w{2,3}$"

    fname = input("Enter First name: ")
    lname = input("Enter last name: ")
    address = input("Enter the street address: ")
    city = input("Enter the city: ")
    state = input("Enter the state: ")
    zip = input("Enter zip: ")
    phone = input("Enter the phone: ")
    email = input("Enter your email: ")
    pwd = getpass("Enter your password: ")
    if not re.search(regex_email, email):
        print("Invalid format, please enter a valid email: email@email.email")
        return

    # Check if email is alread in use
    cursor.execute("SELECT * FROM members WHERE email = %s", (email,))
    existing_member = cursor.fetchone()
    if existing_member:
        print("The email belongs to a another user.Please use differnet email")
        return

    # hashing the password
    hashed_pwd = hashlib.sha256(pwd.encode()).hexdigest()

    # insert the new member into the member table
    try:
        cursor.execute("INSERT INTO members (fname, lname, address, city, state, zip, phone, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (fname, lname, address, city, state, zip, phone, email, hashed_pwd))
        mydb.commit()
        print("You have successfully registered! ")
    except mysql.connector.Error as err1 :
        print("something went wrong with the regestration" + err1)
        return


def member_login(user):
    email = input("Enter you email: ")
    pwd = getpass("Enter your password")
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM members WHERE email=%s", (email,))
    result = cursor.fetchone()  # the tulpe

    if result is None:
        print("Invalid email/login credentials.")
    else:
        hashed_pwd = result[9]  # the password field is at index 9
        inputed_pwd = hashlib.sha256(pwd.encode()).hexdigest()  # to compare with the database hash
        if hashed_pwd == inputed_pwd:

            # overriding the user object
            i = 0
            for x, y in user.items():
                user[x] = result[i]
                i += 1
            print("Login successful!\n")
            while True:
                print("******************************************************")
                print("***")
                print("***       Welcome to the online book store ")
                print("***")
                print("******************************************************")
                print("1- Browse by subject")
                print("2- Search by Authro/Title")
                print("3- Check out")
                print("4- logout")
                choice = input("Type in your option: ")

                if choice == "1":
                    browse_by_subject()
                elif choice == "2":
                    search_by_author_or_title()
                elif choice == "3":
                    check_out()
                elif choice == "4":
                    mydb.close()
                    return
                else:
                    print("Invalid choice. Please try again.")


def browse_by_subject():
    cursor = mydb.cursor()
    cursor.execute("SELECT DISTINCT subject FROM books ORDER BY subject ASC")
    results = cursor.fetchall()
    for result in results:
        print(result[0])

    print("Type the subject you want to browse, or press ENTER to return to the main menu.\n")
    subject = input("Subject: ").upper()
    if subject:
        cursor.execute("SELECT * FROM books WHERE subject=%s", (subject,))
        results = cursor.fetchall()
        i = 0
        # while loop to display 3 books at a time
        while i < len(results):
            for j in range(2):
                if i + j < len(results):
                    print(f"""Author: {results[i+j][1]}\nTitle: {results[i+j][2]}\nISBN: {results[i+j][0]}\nPrice: ({results[i+j][3]})\nSubject: {results[i+j][4]}\n
                    """)
            i += 3  # setting our cout up by 3
            if i < len(results):
                print("Type the ISBN of the book you want to add to your cart, or press ENTER to continue browsing.")
                isbn = input("ISBN: ")
                if isbn:
                    cursor.execute("SELECT * FROM books WHERE isbn=%s", (isbn,))
                    book = cursor.fetchone()
                    if book:
                        qty = input("Enter quantity: ")
                        if qty.isdigit() and int(qty) > 0:
                            lcl_cart["userid"] = user["userid"]
                            lcl_cart["isbn"] = book[0]
                            lcl_cart["qty"] = qty
                            cursor.execute("INSERT INTO cart (userid, isbn, qty) VALUES (%s, %s, %s)", (lcl_cart["userid"], lcl_cart["isbn"], lcl_cart["qty"]))
                            mydb.commit()
                            print(f"{qty} of {book[1]} have been added to your cart.")
                    else:
                        print("Invalid ISBN.")
    else:
        return


def search_by_author_or_title():
    cursor = mydb.cursor()
    while True:
        print("***")
        print("***       Search by Author/Title")
        print("***")
        print("1- Author Search")
        print("2- Title Search")
        print("3- Go Back to Main Menu")
        choice = input("Type in your option: ")
        if choice == "1":
            author = input("Enter author's name or a part of it: ")
            cursor.execute("SELECT * FROM books WHERE author LIKE %s", (f"%{author}%",))
            results = cursor.fetchall()
            i = 0
            # while loop to display 3 books at a time
            while i < len(results):
                for j in range(3):
                    if i + j < len(results):
                        print(f"""Author: {results[i+j][1]}\nTitle: {results[i+j][2]}\nISBN: {results[i+j][0]}\nPrice: ({results[i+j][3]})\nSubject: {results[i+j][4]}\n
                        """)
                i += 3  # setting out cout up by 3
                if i < len(results):
                    print("Type the ISBN of the book you want to add to your cart, or press ENTER to continue browsing.")
                    isbn = input("ISBN: ")
                    if isbn:
                        cursor.execute("SELECT * FROM books WHERE isbn=%s", (isbn,))
                        book = cursor.fetchone()
                        if book:
                            qty = input("Enter quantity: ")
                            if qty.isdigit() and int(qty) > 0:
                                lcl_cart["userid"] = user["userid"]
                                lcl_cart["isbn"] = book[0]
                                lcl_cart["qty"] = qty
                                cursor.execute("INSERT INTO cart (userid, isbn, qty) VALUES (%s, %s, %s)", (lcl_cart["userid"], lcl_cart["isbn"], lcl_cart["qty"]))
                                mydb.commit()
                                print(f"{qty} of {book[1]} have been added to your cart.")
                            elif qty.isdigit() and int(qty) == 0:
                                cursor.execute("DELETE FROM cart WHERE userid=%s AND isbn=%s", (user["userid"], isbn))
                                mydb.commit()
                                print(f"{book[1]} has been removed from your cart.")
                        else:
                            print("Invalid ISBN.")
        # Title or part of title
        elif choice == "2":
            title = input("Enter book title or a part of it: ")
            cursor.execute("SELECT * FROM books WHERE title LIKE %s", (f"%{title}%",))
            results = cursor.fetchall()
            i = 0
            # while loop to display 3 books at a time
            while i < len(results):
                for j in range(3):
                    if i + j < len(results):
                        print(f"{results[i+j][1]} ({results[i+j][3]}) - {results[i+j][4]}")
                i += 3  # setting out cout up by 3
                if i < len(results):
                    print("Type the ISBN of the book you want to add to your cart, or press ENTER to continue browsing.")
                    isbn = input("ISBN: ")
                    if isbn:
                        cursor.execute("SELECT * FROM books WHERE isbn=%s", (isbn,))
                        book = cursor.fetchone()
                        if book:
                            qty = input("Enter quantity: ")
                            if qty.isdigit() and int(qty) > 0:
                                lcl_cart["userid"] = user["userid"]
                                lcl_cart["isbn"] = book[0]
                                lcl_cart["qty"] = qty
                                cursor.execute("INSERT INTO cart (userid, isbn, qty) VALUES (%s, %s, %s)", (lcl_cart["userid"], lcl_cart["isbn"], lcl_cart["qty"]))
                                mydb.commit()
                                print(f"{qty} of {book[1]} have been added to your cart.")
                            elif qty.isdigit() and int(qty) == 0:
                                cursor.execute("DELETE FROM cart WHERE userid=%s AND isbn=%s", (user["userid"], isbn))
                                mydb.commit()
                                print(f"{book[1]} has been removed from your cart.")
                            else:
                                print("Invalid ISBN.")
                        elif choice == "3":
                            break
                        else:
                            print("Invalid option. Please try again.")


def check_out():
    cursor = mydb.cursor()

    # Display cart contents
    cursor.execute("SELECT books.isbn, books.title, books.price, cart.qty FROM books INNER JOIN cart ON books.isbn=cart.isbn WHERE cart.userid=%s", (user["userid"],))
    results = cursor.fetchall()
    total_price = 0

    print("\n\t\t\tInvoice for Order no." + str(cursor.lastrowid))
    print("Shipping Address: \t\t\t\t Billing Address:")
    print(f"Name: {user['fname']} {user['lname']} \t\t\t\t Name: {user['fname']} {user['lname']}")
    print(f"Address: {user['address']} \t\t\t\t Address: {user['address']}")
    print(f"\t{user['city']}, {user['state']} {user['zip']} \t\t\t  {user['city']}, {user['state']} {user['zip']}")
    print("------------------------------------------------------------------")
    print("ISBN\t\tTitle\t\t\t\t\tPrice\tQty\tTotal")
    print("------------------------------------------------------------------")

    for row in results:
        book_isbn = row[0]
        book_title = row[1]
        book_price = row[2]
        qty = row[3]
        print(f"{book_isbn}\t{book_title[:40]:40s}\t{book_price}\t{qty}\t{book_price*qty}")
        total_price += book_price*qty

    print("------------------------------------------------------------------")
    print(f"Total = {total_price}\n")

    # Use user's current address for shipping
    shipping_address = user["address"]
    shipping_city = user["city"]
    shipping_state = user["state"]
    shipping_zip = user["zip"]

    # Display estimated delivery date
    today = datetime.datetime.now()
    estimated_delivery_date = today + datetime.timedelta(days=7)
    print(f"Estimated Delivery Date: {estimated_delivery_date.strftime('%A, %B %d, %Y')}\n")

    # Confirm checkout
    confirm_checkout = input("Proceed to checkout? (Y/N) ")
    if confirm_checkout.lower() == "y":
        # Save the order to the Order table
        cursor.execute("INSERT INTO orders (userid, received, shipAddress, shipCity, shipState, shipZip) VALUES (%s, %s, %s, %s, %s, %s)", (user["userid"], today, shipping_address, shipping_city, shipping_state, shipping_zip))
        mydb.commit()

        # Get the order ID of the newly inserted order
        order_id = cursor.lastrowid

        # Save order details to 'odetails' table
        for row in results:
            book_isbn = row[0]
            qty = row[3]
            book_price = row[2]
            cursor.execute("INSERT INTO odetails (ono, isbn, qty, price) VALUES (%s, %s, %s, %s)", (order_id, book_isbn, qty, book_price))
            mydb.commit()

        # Clear cart wasn't sure if we drop db cart or lcl or both so i
        # commented out the db one
        # cursor.execute("DELETE FROM cart WHERE userid=%s", (user["userid"],))
        lcl_cart.clear()

        print("\n\nYour order has been processed. Thank you for shopping with us!")
    else:
        print("\n\nYour order has been canceled.")


def main():
    while True:
        print("**********************************************************************")
        print("***")
        print("***       Welcome to the online book store ")
        print("***")
        print("**********************************************************************")
        print("1- Member Login")
        print("2- New Member Registration")
        print("3- Quit")
        choice = input("Type in your option: ")

        if choice == "1":
            member_login(user)
        elif choice == "2":
            new_member_registration()
        elif choice == "3":
            # TODO: close the connection to the database and exit the program
            exit()
        else:
            print("Invalid choice. Please try again.")


# call the main function to start the program
main()
