import psycopg2 as psql
import os

conn_pass = os.environ['ERICDB_PWD']
conn_user = 'ericdb'
conn_port = '59876'
conn_db = 'allowance'
conn_host = 'localhost'

def create_cursor():

    #create connection string variable
    conn_str = "dbname = {} user = {} host = {} password = {} port = {}".format(conn_db, conn_user, conn_host, conn_pass, conn_port)
    #create connection
    allow_conn = psql.connect(conn_str)

    #create cursor
    cursor = allow_conn.cursor()
    return allow_conn, cursor

def close_cursor(cursor, conn):

    try:
        #close the cursor
        cursor.close()
        #close the connection
        conn.close()
        return "connection and cursor closed successfully"
    except Exception as e:
        return "connection or cursor could not be closed.  Excption: {}".format(e)

def execute_query(sql_string):

    #create cursor
    allow_conn, cursor = create_cursor()

    #try and execute query
    try:
        cursor.execute(sql_string)
        #commit
        allow_conn.commit()
        #grab the data
        rows = cursor.fetchall()
        #close cursor and connection
        close_cursor(cursor, allow_conn)

        #return rows
        return rows

    except Exception as e:
        print("Failed to execute query. The exception was:")
        print(e)


def execute_statement(sql):

    #create cursor
    allow_conn, cursor = create_cursor()

    #try and execute query
    try:
        cursor.execute(sql)
        #commit
        allow_conn.commit()
        #close cursor and connection
        close_cursor(cursor, allow_conn)

        #return rows
        return "statement successful"

    except Exception as e:
        print("Failed to execute statement. The exception was:")
        print(e)


def execute_insert(table, data):

    #create cursor
    allow_conn, cursor = create_cursor()

#    print("database connection successful")


    #create the base insert statement using the table name
    base_insert = 'insert into {}'.format(table)
#    print('base insert is: {}'.format(base_insert))
    failed_rows = []
    failed_row_count = 0
    success_rows = []
    success_row_count = 0
    #iterate through the data and insert the data
#    print("reading data")
    for row in data:
        #initialize insert query
        cols = ''
        vals = ''
#        print("parsing row")
        for key,val in row.items():
            if cols == '':
                cols = '({}'.format(key)
                vals = '({}'.format(str(val))
            else:
                cols = cols + ', ' + key
                vals = vals + ', ' + str(val)
        cols = cols + ')'
        vals = vals + ');'
        
        try:
            insert_string = base_insert + cols + ' values' + vals
#            print(insert_string)
            cursor.execute(insert_string)
            
            success_rows.append(row)
            success_row_count += 1
        except Exception as e:
            failed_rows.append(row)
            failed_row_count += 1
            print("insert failed: exception: {}".format(e))

    allow_conn.commit()
    close_cursor(cursor, allow_conn)

    return {'success_row_count': success_row_count, 'failed_row_count':failed_row_count, 'failed_rows':failed_rows}


