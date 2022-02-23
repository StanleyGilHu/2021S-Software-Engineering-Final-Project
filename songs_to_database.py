from typing import Any, Tuple

from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
import billboard_copy


def insert_data(title, artist, position, year):
    query = "INSERT INTO songs(title, artist, position, year) " \
            "VALUES(%s, %s, %s, %s);"

    args: Tuple[Any, Any, Any, Any] = (title, artist, position, year)

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(query, args)

        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')

        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()


def main():
    # inc = 1
    for y in range(2006, 2021):
        chart = billboard_copy.ChartData('hot-100-songs', year=y)
        pos = 1
        for i in range(0, 100):
            if y == 2011:
                if i == 6:
                    pos += 1
                if i == 99:
                    continue
            if y == 2016:
                if i == 86:
                    pos += 1
                if i == 99:
                    continue
            song = chart[i]
            art = song.artist
            art_new = art.replace('Featuring', '+')
            if y == 2016 and i == 67:
                art_new = 'Lil Wayne, Wiz Khalifa, Imagine Dragons, Logic, ' \
                          'Ty Dolla $ign + X Ambassadors'
            insert_data(song.title, art_new, pos, y)
            pos += 1

    """chart = billboard_copy.ChartData('hot-100-songs', year=2016)
    song = chart[67]
    art = song.artist.replace('Featuring', '+')
    art = art.replace(' &', ',')
    art = art.replace('Feat.', '+')
    art = art.replace('With', 'w/')
    print(song)"""


if __name__ == '__main__':
    main()
