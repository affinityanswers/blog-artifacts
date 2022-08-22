from configparser import ConfigParser
import pymysql as mysql
from argparse import ArgumentParser
from tabulate import tabulate


def connect_to_db(db_config, autocommit=True):
    config = ConfigParser()
    with open(db_config) as dbh:
         config.read_string(dbh.read())
    section_config = config["mysql"]
    host = section_config["host"]
    db = section_config["db"]
    user = section_config["user"]
    password = section_config["password"]
    port = int(section_config["port"])
    return mysql.connect(host=host,
                        user=user,
                        password=password,
                        db=db, autocommit = autocommit,
                        port=port)


def get_data_from_mysql(mysql_config):
    connection = connect_to_db(mysql_config)
    cursor = connection.cursor()
    cursor.execute("select author, description FROM clan LIMIT 10")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data


def main():
    parser = ArgumentParser(description="This scripts connects mysql to print some data")
    parser.add_argument("mysql_config", help="Path to the file containing mysql config")
    args = parser.parse_args()
    data = get_data_from_mysql(args.mysql_config)
    print(tabulate(data, ["author", "description"], tablefmt="grid"))


if __name__ == "__main__":
    main()
