import logging
import json
import pymssql
import datetime
from decimal import Decimal


def lambda_handler(event, context):
    # Configure logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info('GetProductionSheets Lambda execution started')

    # Reading data from config file
    with open('config.json', 'r') as f:
        config = json.load(f)
    server = config["server"]
    database = config["database"]
    user = config["user"]
    password = config["password"]

    # validate payload
    if not validate_response[0]:
        response_json = {'statusCode': 400,
                        'message': validate_response[1],
                        'success': False}
        return response_json

    try:
        # connecting mysql database
        conn = pymssql.connect(server=server, user=user, password=password, database=database)
        cursor = conn.cursor()

        production_sheet_query_with_join = '''SELECT * from users'''
        production_sheet_data = execute_query(cursor, production_sheet_query)
        for record in production_sheet_data:
               print("For Loop:", record);
 
    except Exception as e:
        response_json = {'statusCode': 500,
                         'message': str(e),
                         'success': False}
        logger.error('An error occurred: %s', str(e), exc_info=True)
    finally:
        cursor.close()
        conn.close()
    logger.info('GetProductionSheets Lambda execution completed')
    return response_json
        

def execute_query(cursor, query):
    cursor.execute(query)
    column_names = [col[0] for col in cursor.description]
    response_json = cursor.fetchall()
    data = [dict(zip(column_names, [(float(value) if type(value) is Decimal else 
                                    (str(value) if type(value) is datetime.datetime else 
                                     (str(value) if type(value) is datetime.date else value))) 
                                     for value in record])) for record in response_json]
    return data


#payload to run lambda function
with open('payload.json', 'r') as f:
    payload = json.load(f)
print(lambda_handler(payload,""))
