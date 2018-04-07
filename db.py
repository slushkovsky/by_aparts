from peewee import Model, SqliteDatabase, CharField


db = SqliteDatabase('.search_history.sqlite3')

class SearchResult(Model):
    class Meta:
        database = db
        table_name = 'search_result'

    url = CharField(unique=True)

db.connect()
db.create_tables([SearchResult])
