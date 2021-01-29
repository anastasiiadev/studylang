import psycopg2

def create_connection():
    connection = None
    try:
        connection = psycopg2.connect(
            database='dcbf9oc5sjf6tk',
            user='xrbyfsrojzmfhn',
            password='f56a0cbb91deacb8bdef571b6a76323a104f63f72cb2cd2d11d6a6bed14ef3a8',
            host='ec2-54-73-90-195.eu-west-1.compute.amazonaws.com',
            port='5432',
        )
        print("Connection to PostgreSQL DB successful")
    except psycopg2.OperationalError as e:
        print(f"The error '{e}' occurred")
        raise Exception
    return connection

def execute_query(connection, query, mode="select"):
    connection.autocommit = True
    cursor = connection.cursor()
    if mode == "select":
        result = None
    try:
        cursor.execute(query)
        print("Query executed successfully")
        if mode == "select":
            result = cursor.fetchall()
            cursor.close()
            return result
    except psycopg2.OperationalError as e:
        print(f"The error '{e}' occurred")
        cursor.close()
        raise Exception

if __name__ == "__main__":
    conn = create_connection()
    query = "SELECT * FROM images"
    #query = "SELECT * FROM pg_catalog.pg_tables;"
    #query = "select column_name from information_schema.columns where information_schema.columns.table_name='tests';"
    #query = "INSERT INTO images (id, filename, fileid) VALUES (2, 'question.jpg', '1jgRj4273tHow-e8JJ8btM4jl6rG20t1U')"
    q = execute_query(conn, query)
    print(q)
