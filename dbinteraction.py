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
            return result
    except psycopg2.OperationalError as e:
        print(f"The error '{e}' occurred")
        raise Exception
