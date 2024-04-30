# A program to manage stock for a bookstore, using an SQLite database backend.

import sqlite3

#===========Database Interacting Layer===========
def init_table(column_info):
    # Dynamically create table based on column/type pairs in column_info
    create_table_query = "CREATE TABLE IF NOT EXISTS book ("
    column_defs = []
    for column_name, data_type in column_info:
        column_defs.append(f"{column_name} "
                            f"{get_sqlite_type(column_name, column_info)}")
    create_table_query += ", ".join(column_defs)
    create_table_query += ");"
    
    try:
        # creates or opens a file called ebookstore
        db = sqlite3.connect(ebookstore_db)
        # get a cursor object
        cursor = db.cursor()

        # check if the table python_programming exists and if not creates it
        cursor.execute(create_table_query)
        # commit the change
        db.commit()
    
    # Catch the exception
    except Exception as e:
        # Roll back any change
        db.rollback()
        raise e

    finally:
        # Close the db connection
        db.close()

def insert_in_table(new_book_entry):
    insert_query = "INSERT INTO book ("
    insert_query += ", ".join([column[0] for column in column_info])
    insert_query += ") VALUES ("
    insert_query += ", ".join(["?" for vals in range(len(column_info))])
    insert_query += ");"
    
    try:
        # creates or opens a file called ebookstore
        db = sqlite3.connect(ebookstore_db)
        # get a cursor object
        cursor = db.cursor()
        # check if the table python_programming exists and if not creates it
        cursor.execute(insert_query, new_book_entry)

        # commit the change
        db.commit()
    
    # Catch the exception
    except Exception as e:
        # Roll back any change
        db.rollback()
        raise e

    finally:
        # Close the db connection
        db.close()

def update_table_entry(row):
    id_value = row[0]
    update_query = "UPDATE book SET "
    update_query += ", ".join([f"{column[0]} = ?" for column in column_info])
    update_query += " WHERE id = ?;"
     
    try:
        # Connect to the SQLite database
        db = sqlite3.connect(ebookstore_db)
        cursor = db.cursor()

        cursor.execute(update_query, row + [id_value,])

        # commit the change
        db.commit()
    
    # Catch the exception
    except Exception as e:
        # Roll back any change
        db.rollback()
        raise e

    finally:
        # Close the db connection
        db.close()

def delete_from_table(row):
    try:
        # creates or opens a file called ebookstore
        db = sqlite3.connect(ebookstore_db)
        # get a cursor object
        cursor = db.cursor()
        
        delete_query = f"DELETE FROM book WHERE id = ?;"

        cursor.execute(delete_query, (row[0],))

        # commit the change
        db.commit()
    
    # Catch the exception
    except Exception as e:
        # Roll back any change
        db.rollback()
        raise e

    finally:
        # Close the db connection
        db.close()
    pass

def search_table(column_name, search_term):
    # creates or opens a file called ebookstore
    db = sqlite3.connect(ebookstore_db)
    # get a cursor object
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM book WHERE {column_name} LIKE ?",
                   ('%' + search_term + '%',) )
    results = cursor.fetchall()

    cursor.close()
    db.close()

    return results
    
def get_all_books():
    # creates or opens a file called ebookstore
    db = sqlite3.connect(ebookstore_db)
    # get a cursor object
    cursor = db.cursor()

    # Query to return all rows from table "book"
    cursor.execute("SELECT * FROM book")

    results = cursor.fetchall()
    cursor.close()
    db.close()
    
    return results

def id_is_unique(input_id):
    # creates or opens a file called ebookstore
    db = sqlite3.connect(ebookstore_db)
    # get a cursor object
    cursor = db.cursor()

    cursor.execute('''SELECT COUNT (*) FROM book WHERE id = ?''', (input_id,))
    count = cursor.fetchone()[0]

    cursor.close()
    db.close()

    return count == 0

#========Generic Type/Validation Methods=========
def validate_attr_input(column_index:int, allow_blank:bool):
    attribute_name = column_info[column_index][0]
    attribute_type = column_info[column_index][1]
    attribute_valid = False
    while attribute_valid is False:
        attribute_input = input(f"Please enter book "
                                f"{attribute_name}: ").strip()
        
        # Early check on id validity
        if column_index == 0 and not id_is_unique(attribute_input):
            print("id already in use! Id must be unique!")
            continue

        # Handle blank input case
        if not allow_blank and attribute_input == '':
            print(f"{attribute_name} "
                  "must not be blank.")
            continue
        elif allow_blank and attribute_input == '':
            return attribute_input

        # Handle int cast if necessary
        if attribute_type == int:
            try:
                attribute_input = int(attribute_input)
                return attribute_input
            except:
                print("Value must be a whole number!")
                continue
        
        # Handle float cast if necessary
        if attribute_type == float:
            try:
                attribute_input = float(attribute_input)
                return attribute_input
            except:
                print("Value must be a number!")
                continue
        
        return attribute_input

def get_sqlite_type(column_header, column_info):
    # Get the SQLite type string for a given column header.

    for header, data_type in column_info:
        if header == column_header:
            if data_type == int:
                return "INTEGER"
            elif data_type == float:
                return "REAL"
            elif data_type == str:
                return "TEXT"
            else:
                return "TEXT"

#======User Interface Layer/Display Records======
def search_book():
    while True:
        search_by = input('''Search by:
1 - Book ID
2 - Book Title
3 - Author
0 - Return
: ''').strip()
        
        # Early out if user wants to go up a level.
        if search_by == '0':
            return
        # Try cast to int        
        try:
            search_by = int(search_by)
        except:
            print("Value entered must be a number!")
            continue

        # Use search_by int to dynamically populate input prompt and
        # avoid branching - will be easier to expand and manage as more
        # searchable fields added.    
        search_term = input(f"Searching by {column_headers[search_by - 1]}: ")
        results = search_table(column_headers[search_by - 1], search_term)
        if len(results) == 0:
            print("No matches found!")
            search_again = input("Would you like to search again? (y/n): "
                                 ).strip().lower()
            if search_again == 'y':
                continue
            else:
                return
        return results


def select_book_from_table(matched_books):
    # Initialise new list of selected records outside of loop,
    # can later expand into a multi-select tool
    selected_records = []
    while True:
        results_count = len(matched_books)
        book_selection = input(f"Enter 0 to return or 1-{results_count} "
                            "to select record to edit: ").strip()
        # As list length is dynamic, use try-except to validate that
        # input is int, rather than testing dynamically generated strings
        # in another loop
        try:
            book_selection = int(book_selection)
        except:
            print("Value entered must be a number!")
            continue
        # Test for "back" condition
        if book_selection == 0:
            return
        # Test that input is in range
        elif book_selection > results_count:
            print(f"Selection must be in range 1-{results_count}")
        # Print selected record to terminal, then return selected
        # record to pass to edit/delete method.
        else:
            max_col_widths = calc_max_col_widths(matched_books)
            selected_record = matched_books[book_selection - 1]
            print_row(" ", selected_record, max_col_widths)
            
            selected_records.append(selected_record)
            return selected_records

def show_books_list(matched_books):
    # Get values required for proper spacing of table
    max_col_widths = calc_max_col_widths(matched_books)
    results_count = len(matched_books)    
    count_col_width = len(str(results_count))

    # construct and print the table header with appropriate spacing
    table_header_str = construct_table_header(count_col_width, max_col_widths)   
    print(table_header_str)

    # prefix result row with index number, then print row
    for result_index, matched_book in enumerate(matched_books, 1):
            index_as_string = (str(result_index) + 
                               (' ' * (count_col_width - 
                                len(str(result_index))+ 1)))
            print_row(index_as_string, matched_book, max_col_widths)
    
def print_row(index_as_string, matched_book, max_col_widths):
    # construct string from tuple with appropriate spacing and print
    row_string = index_as_string
    for col_index, column in enumerate(matched_book):
        row_string += (str(column) + (' ' * (max_col_widths[col_index] - 
                        len(str(column)) + 1)))
    print(row_string)

def calc_max_col_widths(matched_books):
    max_col_widths = [0] * len(matched_books[0])
    for row in matched_books:
        # Iterate over each element in the tuple
        for col_index, column in enumerate(row):
        # Update the maximum length for each column
            max_col_widths[col_index] = max(max_col_widths[col_index],
                                             len(str(column)))
    return max_col_widths

def construct_table_header(count_col_width, max_col_widths):
    table_header_str = ' ' * (count_col_width + 1)
    for col_index, header in enumerate(column_headers):
        table_header_str += header + (' ' * 
                                      (max_col_widths[col_index] - 
                                       len(header) + 1))
    return table_header_str

#=User Interface Layer/Data Manipulation Methods=
def add_book():
    adding_books = True
    print("\nAdding new database entry:\n")
    while adding_books:
        new_book_entry = [''] * len(column_headers)
        # iterate through each column, validating input and adding to the
        # new db entry as appropriate.  
        for col_index in range(0,len(column_headers)):
            new_book_entry[col_index] = validate_attr_input(col_index, False)

        # Take the input values and pass to function to insert in table
        insert_in_table(new_book_entry)

        # Print name of book to terminal
        print(f"Book {new_book_entry[1]} added to stock database.")

        # Provide option to add more books or return to previous menu
        add_more = input("Enter 'b' to add more books, "
                         "or any other value to return to main menu.")
        if add_more == 'b':
            continue
        else:
            return

def edit_delete(row):
    # Branching dialogue for edit/delete methods
    while True:
        edit_delete_input = input('''\nSelect operation to perform:
1 - Edit Record
2 - Delete Record
0 - Cancel
    : ''')
        if edit_delete_input == "1":
            edit_row_values(row)
        elif edit_delete_input == "2":
            if confirm_row_delete(row):
                return
        elif edit_delete_input == "0":
            return
        else:
            print("Invalid selection!")
            continue

def edit_row_values(row):
    new_row_values = [''] * len(column_headers)
    # Row id cannot be edited as it is the primary key
    new_row_values[0] = row[0]
    print("Leave input blank and press Enter to "
          "skip value without changing it.")
    for column_index in range(1,len(column_headers)):
        new_row_values[column_index] = validate_attr_input(column_index, True)
        if(new_row_values[column_index] == ''):
            new_row_values[column_index] = row[column_index]

    print(new_row_values)
    update_table_entry(new_row_values)
    
def confirm_row_delete(row):
    print(f"Deleting {row[1]}")
    confirmation_input = input("Enter DELETE to confirm record deletion\n"
                               "or any other value to return\n"
                               ": ").strip().lower()
    if confirmation_input == "delete":
        delete_from_table(row)
        print("Record deleted from database.")
        return True
    else:
        return False

# 2D List to store corresponding column headers and types
# New column/type pairs can be added here and tables will update
# dynamically.
column_info = [('id', int),
               ('title', str),
               ('author', str),
               ('quantity', int)
               ]

column_headers = [column[0] for column in column_info]
column_types = [column[1] for column in column_info]

# Initialise Database
ebookstore_db = 'ebookstore.db'
init_table(column_info)

# Main menu loop
main_menu = True
while main_menu:
    main_menu_input = input('''
Please select a number from the following options:
1 - Add book to database
2 - Edit/Remove book in database
3 - Search Books
4 - Show all books
0 - Exit
: ''')
    if main_menu_input == '1':
        add_book()
        
    elif main_menu_input == '2':
        # Go to search function and return/display
        matched_books = search_book()
        if not matched_books:
            continue
        show_books_list(matched_books)
        # If search returns more than one book, selection method
        if len(matched_books) > 1:
            matched_books = select_book_from_table(matched_books)

        # Handle list of 1 result
        edit_delete(matched_books[0])        
        
    elif main_menu_input == '3':
        # Go to search function
        matched_books = search_book()
        if not matched_books:
            continue
        # Display results
        show_books_list(matched_books)

    elif main_menu_input == '4':
        # Get all books in db
        all_books = get_all_books()

        # Check that all_books has entries
        if len(all_books) == 0:
            print("No books in database!")
            continue
        
        # pass all_books to show_books method
        show_books_list(all_books)

        if len(all_books) > 1:
            all_books = select_book_from_table(all_books)


        # Continue back to menu if no book selected
        if all_books is None:
            continue

        # Handle list of 1 result
        edit_delete(all_books[0])
        

    elif main_menu_input == '0':
        print("Goodbye!!!")
        exit()
    else:
        print("Invalid input, please enter a number from the menu.")