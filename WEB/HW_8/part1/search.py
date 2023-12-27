from models import Author, Quote
from dbconnect import connectdb

connectdb()

def search_quotes(query_type, query_value):
    if query_type == 'name':
        author = Author.objects(fullname=query_value).first()
        if author:
            quotes = Quote.objects(author=author)
            return quotes
    elif query_type == 'tag':
        quotes = Quote.objects(tags=query_value)
        return quotes
    elif query_type == 'tags':
        tags = query_value.split(',')
        quotes = Quote.objects(tags__in=tags)
        return quotes
    else:
        return []

if __name__ == "__main__":
    while True:
        user_input = input("Enter your request: ")
        if user_input.startswith('name:'):
            query_value = user_input.split(':')[1].strip()
            result = search_quotes('name', query_value)
            for quote in result:
                print(quote.quote)
        elif user_input.startswith('tag:'):
            query_value = user_input.split(':')[1].strip()
            result = search_quotes('tag', query_value)
            for quote in result:
                print(quote.quote)
        elif user_input.startswith('tags:'):
            query_value = user_input.split(':')[1].strip()
            result = search_quotes('tags', query_value)
            for quote in result:
                print(quote.quote)
        elif user_input == 'exit':
            break
        else:
            print("Invalid format")
