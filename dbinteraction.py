import psycopg2
import logging


def create_connection():

    """
    :return: функция возвращает подключение к БД.
    """

    connection = None
    try:
        connection = psycopg2.connect(
            database='dcbf9oc5sjf6tk',
            user='xrbyfsrojzmfhn',
            password='f56a0cbb91deacb8bdef571b6a76323a104f63f72cb2cd2d11d6a6bed14ef3a8',
            host='ec2-54-73-90-195.eu-west-1.compute.amazonaws.com',
            port='5432',
        )
        logging.info("Connection to PostgreSQL DB successful")
    except psycopg2.OperationalError as e:
        logging.error(f"The error '{e}' occurred")
        raise Exception
    return connection


def execute_query(connection, query, mode="select"):

    """
    :param connection: подключение к БД
    :param query: запрос к БД в виде строки
    :param mode: режим работы с БД - select или insert(или что-то другое)
    :return: если режим - select, то возвращается кортеж с результатами запроса к БД,
        иначе ничего не возвращается.
    """

    connection.autocommit = True
    cursor = connection.cursor()
    if mode == "select":
        result = None
    try:
        cursor.execute(query)
        logging.info("Query executed successfully")
        if mode == "select":
            result = cursor.fetchall()
            cursor.close()
            return result
    except psycopg2.OperationalError as e:
        logging.error(f"The error '{e}' occurred")
        cursor.close()
        raise Exception



if __name__ == "__main__":
    logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)
    conn = create_connection()
    query = "SELECT * FROM tests ORDER BY id"
    q = execute_query(conn, query)
    for line in q:
        print(line)
