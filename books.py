import pandas as pd

# import data, encoding=utf-8 as default so don't need to change
books = pd.read_csv('books.csv') # book_id, isbn, isbn13, authors, language_code, title, original_title, orginal_publication_year
# only look at relevant columns
books = books[['book_id', 'isbn', 'isbn13', 'authors', 'language_code', 'title', 'original_title', 'original_publication_year']]
# drop records with incomplete data
books = books.dropna()
# format isbn13 to proper specification: ***-*-*****-***-*
books['isbn13'] = books['isbn13'].astype(str)
books['isbn13'] = books['isbn13'].map(lambda x: f'{x[:3]}-{x[3]}-{x[4:9]}-{x[9:12]}-{x[12]}' if len(x)==15 else None)
# add a column to show where title and original_title differ
books['updated_title'] = [0 if books['title'][x] == books['original_title'][x] else 1 for x in books.index]
# break up authors into separate columns
books[['author1', 'author2', 'author3', 'author4', 'author5']] = books['authors'].str.split(',', n=4, expand=True) 
# Store each publication by its publication year by century in its own worksheet. So 1800-1899, 1900-1999, 2000-2099, etc.
books['original_publication_year'] = books['original_publication_year'].astype(int)
centuries = []
for century in range(-1000, 2000, 100):
    data = books[books['original_publication_year'] > century]
    data = data[books['original_publication_year'] < century+100]
    centuries.append(data)
with pd.ExcelWriter('books_by_century.xlsx') as xlsxWriter:
    year = -1000
    for hundred in centuries:
        hundred.to_excel(xlsxWriter,sheet_name=str(year))
        year += 100

