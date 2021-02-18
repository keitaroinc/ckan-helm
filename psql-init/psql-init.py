import os
import sys
import subprocess
import re
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extensions import AsIs
from sqlalchemy.engine.url import make_url

ckan_conn_str = os.environ.get('CKAN_SQLALCHEMY_URL', '')
datastorerw_conn_str = os.environ.get('CKAN_DATASTORE_WRITE_URL', '')
datastorero_conn_str = os.environ.get('CKAN_DATASTORE_READ_URL', '')

master_user = os.environ.get('PSQL_MASTER', '')
master_passwd = os.environ.get('PSQL_PASSWD', '')
master_database = os.environ.get('PSQL_DB', '')


class DB_Params:
    def __init__(self, conn_str):
        self.db_user = make_url(conn_str).username
        self.db_passwd = make_url(conn_str).password
        self.db_host = make_url(conn_str).host
        self.db_name = make_url(conn_str).database


def check_db_connection(db_params, retry=None):

    print('Checking whether database is up...')

    if retry is None:
        retry = 20
    elif retry == 0:
        print('Giving up...')
        sys.exit(1)

    try:
        con = psycopg2.connect(user=master_user,
                               host=db_params.db_host,
                               password=master_passwd,
                               database=master_database)

    except psycopg2.Error as e:
        print((str(e)))
        print('Unable to connect to the database...try again in a while.')
        import time
        time.sleep(30)
        check_db_connection(db_params, retry=retry - 1)
    else:
        con.close()


def create_user(db_params):
    con = None
    try:
        con = psycopg2.connect(user=master_user,
                               host=db_params.db_host,
                               password=master_passwd,
                               database=master_database)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        print("Creating user " + db_params.db_user.split("@")[0])
        cur.execute('CREATE ROLE "%s" ' +
                    'WITH ' +
                    'LOGIN NOSUPERUSER INHERIT ' +
                    'CREATEDB NOCREATEROLE NOREPLICATION ' +
                    'PASSWORD %s',
                    (AsIs(db_params.db_user.split("@")[0]),
                     db_params.db_passwd,))
    except(Exception, psycopg2.DatabaseError) as error:
        print("ERROR DB: ", error)
    finally:
        cur.close()
        con.close()


def create_db(db_params):
    con = None
    try:
        con = psycopg2.connect(user=master_user,
                               host=db_params.db_host,
                               password=master_passwd,
                               database=master_database)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        cur.execute('GRANT "' + db_params.db_user.split("@")
                    [0] + '" TO "' + master_user.split("@")[0] + '"')

        print("Creating database " + db_params.db_name + " with owner " +
              db_params.db_user.split("@")[0])
        cur.execute('CREATE DATABASE ' + db_params.db_name + ' OWNER "' +
                    db_params.db_user.split("@")[0] + '"')
        cur.execute('GRANT CONNECT ON DATABASE ' +
                    db_params.db_name + ' TO "' +
                    db_params.db_user.split("@")[0] + '"')
    except(Exception, psycopg2.DatabaseError) as error:
        print("ERROR DB: ", error)
    finally:
        cur.close()
        con.close()


def set_db_permissions(db_params, sql):
    con = None
    try:
        con = psycopg2.connect(user=master_user,
                               host=db_params.db_host,
                               password=master_passwd,
                               database=db_params.db_name)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        print("Setting datastore permissions\n")
        print(sql)
        cur.execute(sql)
        print("Datastore permissions applied.")
    except Exception as error:
        print("ERROR DB: ", error)
    finally:
        cur.close()
        con.close()


if master_user == '' or master_passwd == '' or master_database == '':
    print("No master postgresql user provided.")
    print("Cannot initialize default CKAN db resources. Exiting!")
    sys.exit(1)

print("Master DB: " + master_database + " Master User: " + master_user)

ckan_db = DB_Params(ckan_conn_str)
datastorerw_db = DB_Params(datastorerw_conn_str)
datastorero_db = DB_Params(datastorero_conn_str)


def set_azure_db_permissions(db_params):
    con = None
    try:
        con = psycopg2.connect(user=master_user,
                               host=db_params.db_host,
                               password=master_passwd,
                               database=db_params.db_name)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        print("Setting privileges required by Azure")
        # GRANT ALL PRIVILEGES ON DATABASE <newdb> TO <db_user>;
        cur.execute('GRANT ALL PRIVILEGES ON DATABASE ' +
                    datastorerw_db.db_name +
                    ' TO ' + datastorero_db.db_user.split("@")[0])
        cur.execute('GRANT ALL PRIVILEGES ON DATABASE ' +
                    datastorerw_db.db_name +
                    ' TO ' + datastorerw_db.db_user.split("@")[0])
        cur.execute('GRANT ALL PRIVILEGES ON DATABASE ' +
                    datastorerw_db.db_name +
                    ' TO ' + ckan_db.db_user.split("@")[0])

        cur.execute('GRANT ALL PRIVILEGES ON TABLE pg_buffercache TO ' +
                    ckan_db.db_user.split("@")[0])
        cur.execute('GRANT ALL PRIVILEGES ON TABLE pg_buffercache TO ' +
                    datastorerw_db.db_user.split("@")[0])
        cur.execute('GRANT ALL PRIVILEGES ON TABLE pg_buffercache TO ' +
                    datastorero_db.db_user.split("@")[0])
    except Exception as error:
        print("ERROR DB: ", error)
    finally:
        cur.close()
        con.close()


# Check to see whether we can connect to the database, exit after 10 mins
check_db_connection(ckan_db)

try:
    create_user(ckan_db)
except(Exception, psycopg2.DatabaseError) as error:
    print("ERROR DB: ", error)

try:
    create_user(datastorerw_db)
except(Exception, psycopg2.DatabaseError) as error:
    print("ERROR DB: ", error)

try:
    create_user(datastorero_db)
except(Exception, psycopg2.DatabaseError) as error:
    print("ERROR DB: ", error)

try:
    create_db(ckan_db)
except(Exception, psycopg2.DatabaseError) as error:
    print("ERROR DB: ", error)

try:
    create_db(datastorerw_db)
except(Exception, psycopg2.DatabaseError) as error:
    print("ERROR DB: ", error)

try:
    set_azure_db_permissions(datastorerw_db)
except(Exception, psycopg2.DatabaseError) as error:
    print("ERROR DB: ", error)
# replace ckan.plugins so that ckan cli can run and apply datastore permissions
sed_string = "s/ckan.plugins =.*/ckan.plugins = envvars image_view text_view recline_view datastore/g"  # noqa
subprocess.Popen(["/bin/sed", sed_string, "-i", "/srv/app/production.ini"])
sql = subprocess.check_output(["/usr/bin/ckan",
                               "-c", "/srv/app/production.ini",
                               "datastore",
                               "set-permissions"],
                              stderr=subprocess.PIPE)
sql = sql.decode('utf-8')
sql = sql.replace("@"+datastorerw_db.db_host, "")

# Remove the connect clause from the output
sql = re.sub('\\\\connect \"(.*)\"', '', sql)

try:
    set_db_permissions(datastorerw_db, sql)
except(Exception, psycopg2.DatabaseError) as error:
    print("ERROR DB: ", error)
