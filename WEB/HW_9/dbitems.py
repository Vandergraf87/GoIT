
import json
from models import Author, Quote
from dbconnect import connectdb

connectdb()

# Loading data from authors.json
with open('authors.json', 'r', encoding='utf-8') as file:
    authors_data = json.load(file)

for author_data in authors_data:
    author = Author(**author_data)
    author.save()

# Loading data from quotes.json
with open('quotes.json', 'r', encoding='utf-8') as file:
    quotes_data = json.load(file)

for quote_data in quotes_data:
    author_fullname = quote_data['author']
    author = Author.objects(fullname=author_fullname).first()
    quote_data['author'] = author
    quote = Quote(**quote_data)
    quote.save()