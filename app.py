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
                  \rPress ENTER to try again
                    ''')

def sub_menu():
    while True:   
        print('''
            \r1) Edit
            \r2) Delete
            \r3) Return to main menu\r
            ''')
        choice = input('What would you like to do? ')
        if choice in ['1', '2', '3']:
            return choice
        
        else:
            input('''
                  \rPlease choose 1-3.
                  \rPress ENTER to try again
                    ''')
            
            
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


def clean_id(id_str, options):
    try:
        book_id = int(id_str)
    except ValueError:
        input(''' 
            \r*** ID Error ***
            \rThe id should be a number
            \rPress ENTER to try again ''')
        return
    else:
        if book_id in options:
            return book_id
        else:
            input(f''' 
                \r*** ID Error ***
                \rOptions: {options}
                \rPress ENTER to try again ''')
            return


def edit_check(column_name, current_value):
    print(f'\n     Edit {column_name}')
    if column_name == 'Price':
        print(f'Current Value: ${current_value/100}')
    elif column_name == 'Date':
        print(f'Current Value: {current_value.strftime("%B %d, %Y")}')
    else:
        print(f'Current Value: {current_value}')
    
    if column_name == 'Date' or column_name == 'Price':
        while True:
            changes = input('What would you like to change the value to? ')
            if column_name == 'Date':
                cleaned_change = clean_date(changes)
                if type(cleaned_change) == datetime.date:
                    return cleaned_change
            elif column_name == 'Price':
                cleaned_change = clean_price(changes)
                if type(cleaned_change) == int:
                    return cleaned_change
    else:
        return input('What would you like to change the value to? ')


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
            id_options = []
            for book in session.query(Book):
                id_options.append(book.id)
            id_error = True
            while id_error:
                id_choice =input(f'''
                        \rId Options: {id_options}
                        \rBook id: ''')
                cleaned_id_choice = clean_id(id_choice, id_options) 
                if type(cleaned_id_choice) == int:
                    id_error = False 
            the_book = session.query(Book).filter(Book.id == cleaned_id_choice).first()
            print(f'''
                \r{the_book.title} by {the_book.author}
                \rPublished: {the_book.published_date}
                \rPrice: ${the_book.price / 100}''')
            sub_choice = sub_menu()
            if sub_choice == '1':
                # edit
                the_book.title = edit_check('Title', the_book.title)
                the_book.author = edit_check('Author', the_book.author)
                the_book.published_date = edit_check('Date', the_book.published_date)
                the_book.price = edit_check('Price', the_book.price)
                session.commit()
                print('Book Updated!')
                time.sleep(1.5)

            elif sub_choice == '2':
                # delete
                session.delete(the_book)
                session.commit()
                print('Book Deleted!')
                time.sleep(1.5)

        elif choice == '4':
            # book analysis            
            oldest_book = session.query(Book).order_by(Book.published_date).first()
            newest_book = session.query(Book).order_by(Book.published_date.desc()).first()
            total_books = session.query(Book).count()
            python_books = session.query(Book).filter(Book.title.like('%Python%')).count()
            print(f'''
            \n**** Book Analysis ****
            \rOldest Book: {oldest_book}
            \rNewest Book: {newest_book}
            \rTotal Books: {total_books}
            \rNumber of Python Books: {python_books} ''')
            input('\nPress ENTER to continue ')
        
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
    
    