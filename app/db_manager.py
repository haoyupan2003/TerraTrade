from flask import g, current_app
import flask
import pymysql




def get_db():
    if '_database' not in g:
        try:
            g._database = pymysql.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                db=current_app.config['MYSQL_DB']
            )
        except pymysql.MySQLError as e:
            current_app.logger.error(f"Database connection failed: {e}")
            raise
    return g._database

def executeCommit(sql, args):
    db = get_db()
    with db.cursor() as cursor:
        result = cursor.execute(sql, args)
    db.commit()
    return result


def fetchone(sql, args=None):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(sql, args)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result
    # with get_db().cursor() as cursor:
    #     cursor.execute(sql, args)
    #     return cursor.fetchone()

def fetchall(sql, args=()):
    """Fetch all rows from a SQL query."""
    with get_db().cursor() as cursor:
        cursor.execute(sql, args)
        return cursor.fetchall()

 
# def fetchall(sql, args=None):
#     with get_db().cursor() as cursor:
#         cursor.execute(sql, args)
#         return cursor.fetchall()