def custom_sql(querry):
    from django.db import connection
    cursor = connection.cursor()
    # Data retrieval operation - no commit required
    cursor.execute(querry)
    row = cursor.fetchall()

    return row  