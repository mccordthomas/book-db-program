from models import (Base, session, Book, engine)
import csv
import datetime
import time


def menu():
    while True:
        print('''
              \nPROGRAMMING BOOKS
              \r1) Add book
              \r2) View all books
              \r3) Search for book
              \r4) Book Analysis
              \r5) Exit
              \r''')
        choice = input('What would you like to do? ')
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        
        else:
            input('''
                  \rPlease choose 1-5.
                    ''')

# main menu - add, search, analysis, exit, view
# add books to db
# edit books
# delete books
# search books
# data cleaning
# loop runs program
            
def clean_date(date_str):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 
              'August', 'September', 'October', 'November', 'December']
    split_date = date_str.split(' ')
    try:
        month = int(months.index(split_date[0]) +1)
        day = int(split_date[1].split(',')[0])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        input(''' 
        \r*** Date Error ***
        \rThe date should be formatted exactly like January 21, 2001
        \rPress ENTER to try again\n''')
        return
    else:
        return return_date


def clean_price(price_str):
    try:
        price_float = float(price_str)
    except ValueError:
        input(''' 
        \r*** Price Error ***
        \rThe price should be formatted exactly like 25.67,
        \rwithout the currency symbol
        \rPress ENTER to try again ''')
        return
    else:
        return int(price_float * 100)
    

def add_csv():
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            book_in_db = session.query(Book).filter(Book.title==row[0]).one_or_none()
            if book_in_db == None:
                title = row[0]
                author = row[1]
                date = clean_date(row[2])
                price = clean_price(row[3])
                new_book = Book(title=title, author=author, published_date=date, price=price)
                session.add(new_book)
        session.commit()

def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == '1':
            # add book
            title = input('Title: ')
            author = input('Author: ')
            date_error = True
            while date_error:
                date = input('Published Date (ex. Janurary 21, 2001): ').capitalize() 
                date = clean_date(date)
                if type(date) == datetime.date:
                    date_error = False
            price_error = True
            while price_error:
                price = input('Price (ex. 25.99): ')
                cleaned_price = clean_price(price)
                if type(cleaned_price) == int:
                    price_error = False
            new_book = Book(title=title, author=author, published_date=date, price=cleaned_price)
            session.add(new_book)
            session.commit()
            print(f'\n{title} by {author} added!')
            time.sleep(2)
        
        elif choice == '2':
            # view all books
            print('\n')
            for book in session.query(Book):
                print(f'{book.id} | {book.title} | {book.author}')
            input('\nPress ENTER to continue ')
        
        elif choice == '3':
            # search book
            pass
        
        elif choice == '4':
            # book analysis            
            pass
        
        else:
            print('\nGoodbye\n')
            time.sleep(1.5)
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()

    # for book in session.query(Book):
    #     print(book)
    
    