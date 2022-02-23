import mysql.connector
import os
import directories
def get_lyrics(songid):
    """Returns song lyrics in their .txt form."""
    dirs = directories.dirs
    for d in dirs:
        for entry in os.scandir(d):
            if entry.is_file():
                if getid(entry) == songid:
                    return read_lyrics(entry)

def getid(path):
    """Retrieves songid from the last line of the song lyrics"""
    with open(path, "rb") as file:
        file.seek(-2, os.SEEK_END)
        while file.read(1) != b'\n':
            file.seek(-2, os.SEEK_CUR)
        lastline = str(file.readline().decode())
        ind = lastline.find(':')
        just_id = lastline[ind+2:]

    return just_id

def read_lyrics(file_path):
    with open(file_path, 'r') as file_obj:
        lyrics = file_obj.read()
    show_lyrics(lyrics, file_path.name)

def show_lyrics(lyrics, path_name):
    title = path_name[path_name.find(' ')+1 : path_name.find('txt')-1]
    print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print(f"{title}\n\n{lyrics}")

def build_query():
    names = ['title', 'artist']
    nums = ['id', 'position', 'year']
    val = 'no'
    while val == 'no':
        col = input("Would you like to search by ID, Title, Artist, Position, or Year? ")
        col = col.lower()
        if col in names:
            val = input("Enter the name here: ")
        elif col in nums:
            val = input('Enter the number here: ')
            val = int(val)
            if col == 'id':
                col = 'songid'
        else:
            val = 'no'
    send_query(col, val)

def send_query(col, val):
    query = ''

    if col == 'songid':
        query += "SELECT * FROM songs WHERE songid = %s;"
    elif col == 'position':
        query += "SELECT * FROM songs WHERE position = %s;"
    elif col == 'year':
        query += "SELECT * FROM songs WHERE year = %s;"
    elif col == 'title':
        query += "SELECT * FROM songs WHERE title LIKE %s;"
    else:
        query += "SELECT * FROM songs WHERE artist LIKE %s;"

    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='lakeshow9824',
        database='SWE_PROJECT'
    )

    mycursor = mydb.cursor()
    mycursor.execute(query, (val,))
    myresult = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    for row in myresult:
        print(row)

if __name__ == '__main__':
    """Main Method"""
    print(directories.dirs)
    action = ''
    while action != '3':
        action = input("Enter a value corresponding to the desired action (1 - Song Lookup, 2 - Lyrics Lookup, 3 - Quit)\nSelection: ")
        if action == '1':
            build_query()
        elif action == '2':
            songid = input("Enter the song id of the song lyrics you would like to view: ")
            get_lyrics(songid)
        print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print("\nGoodbye.")