#!/usr/bin/env python

from goodreads import client
from sys import exit
import psycopg2


NUM_BOOKS = 10 
OFFSET = 121

def load_book(title, isbn, year, pages, counter):
    '''
        Load a specific book into DB.

    '''
    cur.execute("""INSERT INTO books (title, isbn, year, pages) VALUES (
            %s,
            %s,
            %s,
            %s
            )
            """, (title, isbn, year, pages))
    print 'Loaded book No. {0}'.format(counter + 1)

def load_author(author):
    '''
        Load a specific author into DB

    '''
    cur.execute("""INSERT INTO authors (name, origin, born) VALUES (
            %s,
            %s,
            %s
            ) 
            """, (author.name, author.hometown, author.born_at))


# Connect to the database.
try:
    # Change 'xbaremenos' to your specific username and database name.
    conn = psycopg2.connect("dbname = 'xbaremenos' user = 'xbaremenos'")
except:
    print('Could not connect to DB... exiting...')
    exit(1)


# Try to connect to GoodReads DB through their API
try:
    gc = client.GoodreadsClient('eNOeZpRWitrj0rqo8B9Zg', 'EWTD4TLkL7VNnHjDsdh13JFvk7xkcT6P6CWFg6EJhc')
except:
    print 'Could not connect to goodReads API!'
    print 'exiting ./insert'
    exit(1)


# Create a cursor.
cur = conn.cursor()


loaded_books = 0
counter = 0
# Create some entries to books.
while loaded_books < NUM_BOOKS: 
    print 'Into book No. {0}'.format(counter + 1)
    try:
        book = gc.book((counter + 1) * OFFSET)
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except:
        # An error occured, move on to the next book.
        counter += 1
        continue

    title = book.title
    isbn = book.isbn
    year = book.publication_date[2]
    pages = book.num_pages
    if year != None:
        year = int(year)
    if pages != None:
        pages = int(pages)
    
    # Try to load book into DB. If title is too long, just ignore the book
    # and move on to the next one. 
    if len(title) > 100:
        counter += 1
        continue
    
    load_book(title, isbn, year, pages, counter)
    loaded_books += 1
    counter += 1

    # Load associated author.
    try:
        author = gc.find_author(book.authors[0])
    except:
        print 'Could not associate an author with this book, moving on'
        continue
    
    load_author(author)
        

print 'Tried to load {0} books'.format(counter)
print 'Added a total of {0} books.'.format(loaded_books)


# Insert 4 admin users (ourselves)
cur.execute("""INSERT INTO users (kind, username, password, email) VALUES 
            (
                'admin',
                'xbaremenos',
                'l337H@ck4R!!1!',
                'charkops@auth.gr'
            )
        """)

cur.execute("""INSERT INTO users (kind, username, password, email) VALUES 
            (
                'admin',
                'maylo',
                'YoUCaNtF1nDTh1S',
                'antonodn@ece.auth.gr'
            )
        """)


cur.execute("""INSERT INTO users (kind, username, password, email) VALUES 
            (
                'admin',
                'Z4R0',
                'Th1S1SR4GuL@R',
                'ialevras@ece.auth.gr'
            )
        """)


cur.execute("""INSERT INTO users (kind, username, password, email) VALUES 
            (
                'admin',
                'No0Ne!1',
                'S3cR37P@ssw0RD',
                'dimivars@ece.auth.gr'
            )
        """)

# Commit changes and close connection, exit programm.
try:
    conn.commit()
except:
    conn.rollback()
    print('Could not commint changes... rolling back...')
    exit(1)
finally:
    conn.close()




