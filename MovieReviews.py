import sqlite3
from sqlite3 import Error


def openConnection(_dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Open database: ", _dbFile)

    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        print(" success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

    return conn

def closeConnection(_conn, _dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Close database: ", _dbFile)

    try:
        _conn.close()
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def userInteraction(_conn):
    out = "Enter 1 if you are a user, and enter 2 if you are managing information: "
    print(out)
    choice = input()

    if (choice == '1'):
        user(_conn)
    elif (choice == '2'):
        infoManager(_conn)
    else:
        print("Please try again with a valid response")
        
def user(_conn):
    print("""What would you like to search for?
    1: Cast, id and crew that contains cast members named Alan Parrish and George Banks
    2: The collection, budget and original titles of the movies in the action genre
    3: Movies containing links with a rating of 3.5 or higher
    4: All small movie ratings
    5: All the movies under the adult section containing a budget of over $15,000
    6: The movies that contain an overview but not a homepage
    7: The average budget of a movie that stars Jessie Caldwell
    8: The keywords from movies with ratings of at most 4.5 and timestamps greater than 1425942435
    9: The movie titles of movies that are identical in staring 3 or more crew members
    10: Movies that have starred both Happy Gilmore and Francesca Johnson
    11: Movies with the highest ratings
    12: Movies producing at least four distinct imdb links
    13: The crews of adult movies in the database that include the overview table
    14: The id and cast for crews in the credits table that have at least 7 collections
    15: The movies with the lowest and cheapest rated adult movies
    16: The crew, and id number of cast members named William Wallace and Francis Bergeade
    17: The average budget of the movies with an original language of french
    18: Small movie ratings that are identical for 12 or more movies
    19: The names of all the movies that are in the adventure genre
    20: The movie with the most keywords""")
    choice = int(input())

    if (choice == 1):
        parrishBanks(_conn)
    elif (choice == 2):
        origTitles(_conn)
    elif (choice == 3):
        tLinks(_conn)
    elif (choice == 4):
        smallRatings(_conn)
    elif (choice == 5):
        adultSection(_conn)
    elif (choice == 6):
        overviewHomepage(_conn)
    elif (choice == 7):
        avgBudget(_conn)
    elif (choice == 8):
        movKeywords(_conn)
    elif (choice == 9):
        identicalMembers(_conn)
    elif (choice == 10):
        gilmoreJohnson(_conn)
    elif (choice == 11):
        highestRatings(_conn)
    elif (choice == 12):
        fourDistinct(_conn)
    elif (choice == 13):
        adultOverview(_conn)
    elif (choice == 14):
        sevenCollections(_conn)
    elif (choice == 15):
        lowestMovies(_conn)
    elif (choice == 16):
        wallaceBergeade(_conn)
    elif (choice == 17):
        frenchLang(_conn)
    elif (choice == 18):
        twelveMovies(_conn)
    elif (choice == 19):
        adventureGenre(_conn)
    elif (choice == 20):
        mostKeywords(_conn)
    else:
        print("Please try again with a valid entry")

#1
def parrishBanks(_conn):
    try:
        sql = """SELECT c_cast, c_id, c_crew
                FROM credits
                WHERE c_cast = 'Alan Parrish' AND c_cast = 'George Banks'"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "|" + str(row[1]) + "\n"
        print(l)

    except Error as e:
        print(e)

#2
def origTitles(_conn):
    try:
        sql = """SELECT m_belongs_to_collection, m_budget, m_original_title
                    FROM movies_metadata
                    WHERE m_genre = 'Action'"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "\n"
        print(l)

    except Error as e:
        print(e)

#3
def tLinks(_conn):
    try:
        sql = """SELECT DISTINCT l_imdbid, r_rating
                    FROM links
                    JOIN ratings 
                    ON l_imdbid = r_rating
                    WHERE r_rating >= 3.5
                    ORDER BY r_timestamp"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "\n"
        print(l)

    except Error as e:
        print(e)

#4
def smallRatings(_conn):
    try:
        sql = """SELECT DISTINCT rs_rating
                    FROM ratings_small
                    WHERE type = 'ratings'"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "\n"
        print(l)

    except Error as e:
        print(e)

#5
def adultSection(_conn):
    try:
        sql = """SELECT * 
                    FROM movies_metadata
                    WHERE m_adult != NULL AND m_budget > 15000"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "|" + str(row[1]) + "\n"
        print(l)

    except Error as e:
        print(e)

#6
def overviewHomepage(_conn):
    try:
        sql = """SELECT m_id
                    FROM movies_metadata
                    WHERE m_overview != NULL
                    GROUP BY m_id
                    EXCEPT
                    SELECT m_id
                    FROM movies_metadata
                    WHERE m_homepage != NULL
                    GROUP BY m_id"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "|" + str(row[1]) + "\n"
        print(l)

    except Error as e:
        print(e)

#7
def avgBudget(_conn):
    try:
        sql = """SELECT AVG(m_budget)
                    FROM movies_metadata, credits
                    WHERE c_cast = 'Jessie Caldwell'"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "|" + str(row[1]) + "\n"
        print(l)

    except Error as e:
        print(e)

#8
def movKeywords(_conn):
    try:
        sql = """SELECT k_keywords
                    FROM keyword, ratings
                    WHERE r_rating <= 4.5 AND r_timestamp > 1425942435"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "|" + str(row[1]) + "\n"
        print(l)

    except Error as e:
        print(e)

#9
def identicalMembers(_conn):
    try:
        sql = """SELECT m_original_titles
                    FROM movies_metadata, credits 
                    GROUP BY m_original_titles
                    HAVING COUNT(c_crew) >= 3"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "\n"
        print(l)

    except Error as e:
        print(e)

#10
def gilmoreJohnson(_conn):
    try:
        sql = """SELECT m_original_title
                    FROM movies_metadata, credits
                    WHERE c_cast = 'Happy Gilmore'
                    INTERSECT
                    SELECT m_original_title 
                    FROM movies_metadata, credit
                    WHERE c_cast = 'Francesca Johnson'"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "|" + str(row[1]) + "\n"
        print(l)

    except Error as e:
        print(e)

#11
def highestRatings(_conn):
    try:
        sql = """SELECT m_original_title, r_ratings
                    FROM movies_metadata, ratings
                    WHERE r_ratings = (SELECT MAX(r_ratings) FROM m_original_title)"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "\n"
        print(l)

    except Error as e:
        print(e)

#12
def fourDistinct(_conn):
    try:
        sql = """SELECT m_original_title, COUNT (DISTINCT l_imdbid) AS imdb_type
                    FROM movies_metadata
                    WHERE l_imdbid != NULL
                    GROUP BY movies_metadata
                    HAVING COUNT(DISTINCT l_imdbid) >= 4"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "|" + str(row[1]) + "|" + str(row[2]) + "|" + str(row[3]) + "|" + str(row[4]) + "|" + str(row[5]) + "\n"
        print(l)

    except Error as e:
        print(e)

#13
def adultOverview(_conn):
    try:
        sql = """SELECT DISTINCT c_crew
                    FROM (SELECT c_crew
                        FROM credits, movies_metadata
                        WHERE m_adult = m_original_title
                        UNION
                        SELECT credits AS c_crew
                        FROM m_overview
                        WHERE credits IN (SELECT m_adult FROM m_original_title)
                        ) movie"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "|" + str(row[1]) + "|" + str(row[2]) + "\n"
        print(l)

    except Error as e:
        print(e)
        
#14
def sevenCollections(_conn):
    try:
        sql = """SELECT c_id, c_cast
                    FROM credits c
                    JOIN movies_metadata m
                    ON c_id = m_cast
                    WHERE m_belongs_to_collection >= 7"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "|" + str(row[1]) + "|" + str(row[2]) + "\n"
        print(l)

    except Error as e:
        print(e)

#15
def lowestMovies(_conn):
    try:
        sql = """SELECT DISTINCT m_original_title
                    FROM movies_metadata
                    INNER JOIN ratings
                    ON original_title.kind = r_ratings.kind
                    AND m_adult != NULL
                    WHERE m_budget = (SELECT MIN(r_ratings) FROM ratings WHERE m_adult != NULL)"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "|" + str(row[1]) + "|" + str(row[2]) + "\n"
        print(l)

    except Error as e:
        print(e)
        
#16
def wallaceBergeade(_conn):
    try:
        sql = """SELECT c_crew, c_id
                    FROM credits
                    WHERE c_cast = 'William Wallace' AND c_cast = 'Francis Bergeade'"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "|" + str(row[1]) + "|" + str(row[2]) + "\n"
        print(l)

    except Error as e:
        print(e)

#17
def frenchLang(_conn):
    try:
        sql = """SELECT AVG(m_budget)
                    FROM movies_metadata
                    WHERE m_original_language = 'French'"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "|" + str(row[1]) + "|" + str(row[2]) + "\n"
        print(l)

    except Error as e:
        print(e)
        
#18
def twelveMovies(_conn):
    try:
        sql = """SELECT rs_ratings
                    FROM ratings_small 
                    GROUP BY rs_ratings
                    HAVING COUNT(rs_ratings) >= 12"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "|" + str(row[1]) + "|" + str(row[2]) + "\n"
        print(l)

    except Error as e:
        print(e)

#19
def adventureGenre(_conn):
    try:
        sql = """SELECT m_original_title 
                    FROM movies_metadata 
                    WHERE m_genres = 'Adventure'"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "|" + str(row[1]) + "|" + str(row[2]) + "\n"
        print(l)

    except Error as e:
        print(e)

#20
def mostKeywords(_conn):
    try:
        sql = """SELECT m_original_title
                    FROM movies_metadata
                    WHERE m_id =
                    (SELECT m_id
                    FROM keywords
                    WHERE k_keywords >= ALL (SELECT k_keywords FROM keywords)
                    );"""
        cursor = _conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        l = ""
        for row in rows:
            l += str(row[0]) + "|" + str(row[1]) + "|" + str(row[2]) + "\n"
        print(l)

    except Error as e:
        print(e)
        
### Modification Operations        
        
def infoManager(_conn):
    out = """Enter the modification you would like to perform:
    1. Insert Information
    2. Update Information
    3. Delete Information"""

    print(out)
    choice = input()
    
    if (choice == '1'):
        insert(_conn)
    elif (choice == '2'):
        update(_conn)
    elif (choice == '3'):
        delete(_conn)
    else:
        print("Please try again with a valid choice")
        
### Insert Operation 

def insert(_conn):
    out = """Which table would you like to insert into?
    1. credits
    2. keywords
    3. links
    4. links_small
    5. movies_metadata
    6. ratings
    7. ratings_small"""

    print(out)
    choice = input()

    if (choice == '1'):
        print("Inserting into credits: ")
        _ccast = int(input("Enter in the c_cast: "))
        _m_belongs_to_collection = int(input("Enter in the c_id: "))
        _mbudget = int(input("Enter in the c_crew: "))

        try:
            sql = """insert into credits (c_cast, c_id, c_crew) values(?, ?, ?)"""
            args = [_ccast, _m_belongs_to_collection, _mbudget]
            _conn.execute(sql, args)
            print("Successfully inserted")
        except Error as e:
            print(e)

    elif(choice == '2'):
        print("Inserting into keywords: ")
        _kid = int(input("Enter in the k_id: "))
        _kkeywords = int(input("Enter in the k_keywords: "))

        try:
            sql = """insert into keywords(k_id, k_keywords)"""
            args = [_kid, _kkeywords]
            _conn.execute(sql, args)
            print("Inserted successfully")
        except Error as e:
            print(e)

    elif (choice == '3'):
        print("Inserting into links: ")
        _lmovieid = int(input("Enter in the l_movieID: "))
        _limdbid = int(input("Enter in the l_imdbID: "))
        _ltmdid = int(input("Enter in the l_tmdID: "))

        try:
            sql = "insert into links values(?, ?, ?)"
            args = [_lmovieid, _limdbid, _ltmdid]
            _conn.execute(sql, args)
            print("Inserted into interceptions successfully")
        except Error as e:
            print(e)

    elif (choice == '4'):
        print("Inserting into links_small: ")
        _lsmovieid = int(input("Enter in the ls_movieID: "))
        _lsimdbid = int(input("Enter in the ls_imdbID: "))
        _lstmdid = int(input("Enter in the ls_tmdID: "))

        try:
            sql = "insert into links values(?, ?, ?)"
            args = [_lsmovieid, _lsimdbid, _lstmdid]
            _conn.execute(sql, args)
            print("Inserted into interceptions successfully")
        except Error as e:
            print(e)

    elif (choice == '5'):
        print("Inserting into movies_metadata: ")
        _madult = int(input("Enter in the m_adult: "))
        _mbelongstocollection = int(input("Enter in the m_belongs_to_collection: "))
        _mbudget = int(input("Enter in the m_budget: "))
        _ruserid = int(input("Enter in the m_genres: "))
        _mhomepage = input("Enter in the m_homepage: ")
        _mid = input("Enter in the m_id: ")
        _mimdbid = input("Enter in the m_imdbID: ")
        _moriginallanguage = input("Enter in the m_original_language: ")
        _moriginaltitle = int(input("Enter in the m_original_title: "))
        _moverview = int(input("Enter in the m_overview: "))

        try:
            sql = "insert into movies_metadata values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            args = [_madult, _mbelongstocollection, _mbudget, _ruserid, _mhomepage, _mid, _mimdbid, _moriginallanguage, _moriginaltitle, _moverview]
            _conn.execute(sql, args)
        except Error as e:
            print(e)

    elif (choice == '6'):
        print("Inserting into ratings: ")
        _ruserid = int(input("Enter in the r_userId: "))
        _rmovieid = input("Enter in the r_movieId: ")
        _rrating = input("Enter in the r_rating: ")
        _rtimestamp = input("Enter in the r_timestamp: ")

        try:
            sql = "insert into ratings values(?, ?, ?, ?)"
            args = [_ruserid, _rmovieid, _rrating, _rtimestamp]
            _conn.execute(sql, args)
        except Error as e:
            print(e)
            
    elif (choice == '7'):
        print("Inserting into ratings_small: ")
        _rsuserid = int(input("Enter in the rs_userId: "))
        _rsmovieid = input("Enter in the rs_movieId: ")
        _rsrating = input("Enter in the rs_rating: ")
        _rstimestamp = input("Enter in the rs_timestamp: ")

        try:
            sql = "insert into ratings values(?, ?, ?, ?)"
            args = [_rsuserid, _rsmovieid, _rsrating, _rstimestamp]
            _conn.execute(sql, args)
        except Error as e:
            print(e)

## Update Operations

def update(_conn):
    out = """Which table would you like to insert into?
    1. credits
    2. keywords
    3. links
    4. links_small
    5. movies_metadata
    6. ratings
    7. ratings_small"""

    print(out)
    choice = input()

    if (choice == "1"):
        updateCredits(_conn)
    elif (choice == '2'):
        updateKeywords(_conn)
    elif (choice == '3'):
        updateLinks(_conn)
    elif (choice == '4'):
        updateLinksSmall(_conn)
    elif (choice == '5'):
        updateMoviesMetadata(_conn)
    elif (choice == '6'):
        updateRatings(_conn)
    elif (choice == '7'):
        updateRatingsSmall(_conn)
    else:
        print("Please try again with a valid choice")

def updateCredits(_conn):
    _ccast = int(input("Enter the credit information you want to update: "))

    out = """What do you want to update? 
    1. c_cast
    2. c_id
    3. c_crew"""

    print(out)
    choice = input()

    if (choice == "1"):
        _m_belongs_to_collection = int(input("Enter the updated c_cast: "))

        try:
            sql = """update credits 
                        set c_cast = ? 
                        where credits = ?"""
            args = [_m_belongs_to_collection, _ccast]

            _conn.execute(sql, args)
            print("c_cast updated successfully")

        except Error as e:
            print(e)
    elif (choice == '2'):
        _mbudget = int(input("Enter the updated c_id: "))

        try:
            sql = """update credits 
                        set c_id = ? 
                        where credits = ?"""
            args = [_mbudget, _ccast]

            _conn.execute(sql, args)
            print("c_id updated successfully")

        except Error as e:
            print(e)

    elif (choice == '3'):
        _ruserid = int(input("Enter the updated c_crew: "))

        try:
            sql = """update credits 
                        set c_crew = ? 
                        where credits = ?"""
            args = [_ruserid, _ccast]

            _conn.execute(sql, args)
            print("c_crew updated successfully")

        except Error as e:
            print(e)
    else:
        print("Please try again with a valid choice")

def updateKeywords(_conn):
    _kid = int(input("Enter the keyword information you want to update: "))

    out = """What do you want to update? 
    1. k_id
    2. k_keywords"""

    print(out)
    choice = input()

    if (choice == "1"):
        _kkeywords = int(input("Enter the updated k_id: "))
        try:
            sql = """update keywords 
                        set k_id = ? 
                        where keywords = ?"""
            args = [_kkeywords, _kid]
            _conn.execute(sql, args)
            print("k_id updated successfully")

        except Error as e:
            print(e)
    elif (choice == '2'):
        _kid = int(input("Enter the updated k_keywords: "))
        try:
            sql = """update keywords 
                        set k_keywords = ? 
                        where keywords = ?"""
            args = [_kkeywords, _kid]
            _conn.execute(sql, args)
            print("k_keywords updated successfully")

        except Error as e:
            print(e)

def updateLinks(_conn):
    _l_movieID = int(input("Enter the links information you want to update: "))

    out = """What do you want to update? 
    1. l_movieID
    2. l_imdbID
    3. l_tmdID"""

    print(out)
    choice = input()

    if (choice == "1"):
        l_imdbID = int(input("Enter the updated l_movieID: "))

        try:
            sql = """update links 
                        set l_movieID = ? 
                        where links = ?"""
            args = [l_imdbID, _l_movieID]

            _conn.execute(sql, args)
            print("l_imdbID updated successfully")

        except Error as e:
            print(e)
    elif (choice == '2'):
        _l_movieID = int(input("Enter the updated l_tmdID: "))

        try:
            sql = """update links 
                        set l_tmdID = ? 
                        where links = ?"""
            args = [_l_tmdID, _l_movieID]

            _conn.execute(sql, args)
            print("l_tmdID updated successfully")

        except Error as e:
            print(e)

    elif (choice == '3'):
        _l_tmdID = int(input("Enter the updated l_imdbID: "))

        try:
            sql = """update links 
                        set l_imdbID = ? 
                        where links = ?"""
            args = [_l_tmdID, _l_movieID]

            _conn.execute(sql, args)
            print("l_imdbID updated successfully")

        except Error as e:
            print(e)
            
def updateLinksSmall(_conn):
    _l_movieID = int(input("Enter the links_small information you want to update: "))

    out = """What do you want to update? 
    1. ls_movieID
    2. ls_imdbID
    3. ls_tmdID"""

    print(out)
    choice = input()

    if (choice == "1"):
        ls_imdbID = int(input("Enter the updated ls_movieID: "))

        try:
            sql = """update links_small
                        set ls_movieID = ? 
                        where links_small = ?"""
            args = [ls_imdbID, _ls_movieID]

            _conn.execute(sql, args)
            print("ls_imdbID updated successfully")

        except Error as e:
            print(e)
    elif (choice == '2'):
        _ls_movieID = int(input("Enter the updated ls_tmdID: "))

        try:
            sql = """update links_small 
                        set ls_tmdID = ? 
                        where links_small = ?"""
            args = [_ls_tmdID, _ls_movieID]

            _conn.execute(sql, args)
            print("ls_tmdID updated successfully")

        except Error as e:
            print(e)

    elif (choice == '3'):
        _ls_tmdID = int(input("Enter the updated ls_imdbID: "))

        try:
            sql = """update links_small 
                        set ls_imdbID = ? 
                        where links_small = ?"""
            args = [_ls_tmdID, _l_movieID]

            _conn.execute(sql, args)
            print("ls_imdbID updated successfully")

        except Error as e:
            print(e)

def updateMoviesMetadata(_conn):
    _madult = int(input("Enter the movies_metadata information you want to update: "))
    
    out = """What do you want to update? 
    1. m_adult                     
    2. m_belongs_to_collection     
    3. m_budget                   
    4. m_genres                    
    5. m_homepage                  
    6. m_id                        
    7. m_imdbID                    
    8. m_original_language        
    9. m_original_title          
    10. m_overview"""

    print(out)
    choice = input()

    if (choice == "1"):
        _m_belongs_to_collection = int(input("Enter the updated m_adult: "))

        try:
            sql = """update movies_metadata 
                        set m_adult = ? 
                        where movies_metadata = ?"""
            args = [_m_belongs_to_collection, _madult]

            _conn.execute(sql, args)
            print("m_adult updated successfully")

        except Error as e:
            print(e)
    elif (choice == '2'):
        _mbudget = int(input("Enter the updated m_belongs_to_collection: "))

        try:
            sql = """update movies_metadata 
                        set m_belongs_to_collection = ? 
                        where movies_metadata = ?"""
            args = [_mbudget, _madult]

            _conn.execute(sql, args)
            print("m_belongs_to_collection updated successfully")

        except Error as e:
            print(e)
    elif (choice == '3'):
        _m_genres = int(input("Enter the updated m_budget: "))

        try:
            sql = """update movies_metadata 
                        set m_budget = ? 
                        where movies_metadata = ?"""
            args = [_m_genres, _madult]

            _conn.execute(sql, args)
            print("m_budget updated successfully")

        except Error as e:
            print(e)
    elif (choice == '4'):
        _mhomepage = input("Enter the updated m_genres: ")

        try:
            sql = """update movies_metadata 
                        set m_genres = ? 
                        where movies_metadata = ?"""
            args = [_mhomepage, _madult]

            _conn.execute(sql, args)
            print("m_genres updated successfully")

        except Error as e:
            print(e)
    elif (choice == '5'):
        _mid = input("Enter the updated m_homepage: ")

        try:
            sql = """update movies_metadata 
                        set m_homepage = ? 
                        where movies_metadata = ?"""
            args = [_mid, _madult]

            _conn.execute(sql, args)
            print("m_homepage updated successfully")
        except Error as e:
            print(e)
    elif (choice == '6'):
        _mimdbid = input("Enter the updated m_id: ")

        try:
            sql = """update movies_metadata 
                        set m_id = ? 
                        where movies_metadata = ?"""
            args = [_mimdbid, _madult]

            _conn.execute(sql, args)
            print("m_id updated successfully")
        except Error as e:
            print(e)
    elif (choice == '7'):
        _moriginallanguage = input("Enter the updated m_imdbID: ")

        try:
            sql = """update movies_metadata 
                        set m_imdbID = ? 
                        where movies_metadata = ?"""
            args = [_moriginallanguage, _madult]

            _conn.execute(sql, args)
            print("m_imdbID updated successfully")
        except Error as e:
            print(e)
    elif (choice == '8'):
        _moriginaltitle = int(input("Enter the updated m_original_language: "))

        try:
            sql = """update movies_metadata 
                        set m_original_language = ? 
                        where movies_metadata = ?"""
            args = [_moriginaltitle, _madult]

            _conn.execute(sql, args)
            print("m_original_language updated successfully")
        except Error as e:
            print(e)
    elif (choice == '9'):
        _moverview = int(input("Enter the updated m_original_title: "))

        try:
            sql = """update movies_metadata 
                        set m_original_title = ? 
                        where movies_metadata = ?"""
            args = [_moriginaltitle, _madult]

            _conn.execute(sql, args)
            print("m_original_title updated successfully")
        except Error as e:
            print(e)
    elif (choice == '10'):
        _passNull = int(input("Enter the updated m_overview: "))

        try:
            sql = """update movies_metadata 
                        set m_overview = ? 
                        where movies_metadata = ?"""
            args = [_moverview, _madult]

            _conn.execute(sql, args)
            print("m_overview updated successfully")
        except Error as e:
            print(e)
    else:
        print("Please try again with a valid choice")     

def updateRatings(_conn):
    _ruserid = int(input("Enter the ratings information you want to update: "))
    
    out = """What do you want to update? 
    1. r_userId
    2. r_movieId
    3. r_rating
    4. r_timestamp"""

    print(out)
    choice = input()

    if (choice == "1"):
        _rmovieid = input("Enter the updated r_userId: ")

        try:
            sql = """update ratings 
                        set r_userId = ? 
                        where ratings = ?"""
            args = [_rmovieid, _ruserid]

            _conn.execute(sql, args)
            print("r_userId updated successfully")

        except Error as e:
            print(e)
            
    elif (choice == '2'):
        _rrating = input("Enter the updated r_movieId: ")

        try:
            sql = """update ratings 
                        set r_movieId = ? 
                        where ratings = ?"""
            args = [_rrating, _ruserid]

            _conn.execute(sql, args)
            print("r_movieId updated successfully")

        except Error as e:
            print(e)
            
    elif (choice == '3'):
        _rtimestamp = int(input("Enter the updated r_rating: "))

        try:
            sql = """update ratings 
                        set r_rating = ? 
                        where ratings = ?"""
            args = [_rtimestamp, _ruserid]

            _conn.execute(sql, args)
            print("r_rating updated successfully")

        except Error as e:
            print(e)
            
    elif (choice == '4'):
        r_userId = int(input("Enter the updated r_timestamp: "))

        try:
            sql = """update ratings 
                        set r_timestamp = ? 
                        where ratings = ?"""
            args = [r_userId, _ruserid]

            _conn.execute(sql, args)
            print("r_timestamp updated successfully")

        except Error as e:
            print(e)
    else:
        print("Please try again with a valid choice")

def updateRatingsSmall(_conn):
    _rsuserid = int(input("Enter the ratings_small information you want to update: "))
    
    out = """What do you want to update? 
    1. rs_userId
    2. rs_movieId
    3. rs_rating
    4. rs_timestamp"""

    print(out)
    choice = input()

    if (choice == "1"):
        _rsmovieid = input("Enter the updated rs_userId: ")

        try:
            sql = """update ratings_small 
                        set rs_userId = ? 
                        where ratings_small = ?"""
            args = [_rsmovieid, _rsuserid]

            _conn.execute(sql, args)
            print("rs_userId updated successfully")

        except Error as e:
            print(e)
            
    elif (choice == '2'):
        _rsrating = input("Enter the updated rs_movieId: ")

        try:
            sql = """update ratings_small 
                        set rs_movieId = ? 
                        where ratings_small = ?"""
            args = [_rsrating, _rsuserid]

            _conn.execute(sql, args)
            print("rs_movieId updated successfully")

        except Error as e:
            print(e)
            
    elif (choice == '3'):
        _rstimestamp = int(input("Enter the updated rs_rating: "))

        try:
            sql = """update ratings_small 
                        set rs_rating = ? 
                        where ratings_small = ?"""
            args = [_rstimestamp, _rsuserid]

            _conn.execute(sql, args)
            print("rs_rating updated successfully")

        except Error as e:
            print(e)
            
    elif (choice == '4'):
        r_userId = int(input("Enter the updated r_timestamp: "))

        try:
            sql = """update ratings_small 
                        set r_timestamp = ? 
                        where ratings_small = ?"""
            args = [r_userId, _rstimestamp]

            _conn.execute(sql, args)
            print("r_timestamp updated successfully")

        except Error as e:
            print(e)
    else:
        print("Please try again with a valid choice")

## Delete Operations

def delete(_conn):
    out = """Which table would you like to insert into?
    1. credits
    2. keywords
    3. links
    4. links_small
    5. movies_metadata
    6. ratings
    7. ratings_small"""

    print(out)
    choice = input()

    if (choice == "1"):
        deleteCredits(_conn)
    elif (choice == '2'):
        deleteKeywords(_conn)
    elif (choice == '3'):
        deleteLinks(_conn)
    elif (choice == '4'):
        deleteLinksSmall(_conn)
    elif (choice == '5'):
        deleteMoviesMetadata(_conn)
    elif (choice == '6'):
        deleteRatings(_conn)
    elif (choice == '7'):
        deleteRatingsSmall(_conn)
    else:
        print("Please try again with a valid choice")

def deleteCredits(_conn):
    _ccast = int(input("Enter in the c_cast: "))
    try:
        sql = "Delete from credits where c_cast = ?"
        _conn.execute(sql, [_ccast])
        print("Successfully deleted from credits")
    
    except Error as e:
        print(e)

def deleteKeywords(_conn):
    _kid = int(input("Enter in the k_id: "))
    try:
        sql = "Delete from keywords where k_id = ?"
        _conn.execute(sql, [_kid])
        print("Successfully deleted from keywords")
    
    except Error as e:
        print(e)
        
def deleteLinks(_conn):
    _lmovieID = int(input("Enter in the l_movieID: "))
    try:
        sql = "Delete from keywords where l_movieID = ?"
        _conn.execute(sql, [_lmovieID])
        print("Successfully deleted from links")
    
    except Error as e:
        print(e)
        
def deleteLinksSmall(_conn):
    _lsimdbID = int(input("Enter in the ls_imdbID: "))
    try:
        sql = "Delete from keywords where ls_imdbID = ?"
        _conn.execute(sql, [_lsimdbID])
        print("Successfully deleted from links_small")
    
    except Error as e:
        print(e)

def deleteMoviesMetadata(_conn):
    _madult = int(input("Enter in the m_adult: "))
    try:
        sql = "Delete from movies_metadata where m_adult = ?"
        _conn.execute(sql, [_madult])
        print("Successfully deleted from movies_metadata")
    
    except Error as e:
        print(e)
        
def deleteRatings(_conn):
    _ruserid = input("Enter in the r_userID: ")

    try:
        sql = "Delete from ratings where r_userID = ?"
        _conn.execute(sql, [_ruserid])
        print("Successfully deleted from ratings")

    except Error as e:
        print(e)

def deleteRatingsSmall(_conn):
    _m_belongs_to_collection = int(input("Enter in the m_belongs_to_collection: "))
    try:
        sql = "Delete from ratings where m_belongs_to_collection = ?"
        _conn.execute(sql, [_m_belongs_to_collection])
        print("Successfully deleted from ratings_small")
    
    except Error as e:
        print(e)

def main():
    database = r"MovieReviews.sqlite"
    print("MovieReviews")
    # create a database connection
    conn = openConnection(database)
    with conn:
        userInteraction(conn)

    closeConnection(conn, database)

if __name__ == '__main__':
    main()