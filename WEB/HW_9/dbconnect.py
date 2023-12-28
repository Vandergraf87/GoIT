from mongoengine import connect

def connectdb():
    database_name = 'testdb.collone'
    uri = f'mongodb+srv://komarovdmytro:YdEjWalBjoLF4ouP@goit.uzix2dv.mongodb.net/{database_name}?retryWrites=true&w=majority'
    connect(host=uri)