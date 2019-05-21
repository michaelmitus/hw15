import sqlite3 as lite
import sys
import pprint

def first():
    # Вывести покупателей (полное имя, номер телефона) которые что либо покупали,
    # проживающих в одном городе, если их кол-во в городе больше 1
    try:
        con = None
        con = lite.connect('Chinook_Sqlite.sqlite')
        query_invoice = '''
              SELECT DISTINCT C.FirstName || " " || C.LastName, C.Phone 
              FROM Customer as C   
              INNER JOIN Invoice as I ON C.CustomerID = I.CustomerID
              WHERE 
                  (SELECT COUNT(*) FROM Customer AS CC 
                   WHERE C.CustomerID = I.CustomerID AND CC.City=C.City ) > 1
              ORDER BY C.City              
            '''
        curID = con.cursor()
        curID.execute(query_invoice)
        pprint.pprint(curID.fetchall())
    except Exception as e:
        print(e)
        sys.exit(1)
    finally:
        if con is not None:
            con.close()

def second():
    # 'Вывести топ 3 самых платежеспособных города за все время.'
    try:
        con = None
        con = lite.connect('Chinook_Sqlite.sqlite')
        query_invoice = '''
              SELECT DISTINCT C.City, sum(Total) 
              FROM Customer as C   
              INNER JOIN Invoice as I ON C.CustomerID = I.CustomerID
              GROUP BY C.City
              ORDER BY sum(Total) DESC
              LIMIT 3             
            '''
        curID = con.cursor()
        curID.execute(query_invoice)
        pprint.pprint(curID.fetchall())
    except Exception as e:
      print(e)
      sys.exit(1)
    finally:
      if con is not None:
        con.close()

def third():
    # Вывести самый популярный, на основании кол-ва продаж, жанр (название) и все треки в нем (название, альбом, исполнитель).
    try:
        con = None
        con = lite.connect('Chinook_Sqlite.sqlite')
        query_qenre = '''
              SELECT DISTINCT G.Name 
              FROM Genre as G   
              INNER JOIN Track as T ON T.GenreID = G.GenreID
              INNER JOIN InvoiceLine as I ON I.TrackID = T.TrackID
              GROUP BY G.Name
              ORDER BY sum(Quantity) DESC
              LIMIT 1
            '''
        curID = con.cursor()
        curID.execute(query_qenre)
        max_genre = curID.fetchone()[0]
        print(max_genre)
        query_track = '''
              SELECT T.Name, Album.Title, Artist.Name
              FROM Track as T   
              INNER JOIN Genre as G ON T.GenreID = G.GenreID
              INNER JOIN Album ON Album.AlbumID = T.AlbumID
              INNER JOIN Artist ON Album.ArtistID = Artist.ArtistID
              WHERE G.Name Like "'''+str(max_genre)+'''"          
            '''
        curID = con.cursor()
        curID.execute(query_track)
        pprint.pprint(curID.fetchall())

    except Exception as e:
      print(e)
      sys.exit(1)
    finally:
      if con is not None:
        con.close()

#Вывести покупателей (полное имя, номер телефона) которые что либо покупали, проживающих в одном городе, если их кол-во в городе больше 1.
first()

#Вывести топ 3 самых платежеспособных города за все время.
#second()

#Вывести самый популярный, на основании кол-ва продаж, жанр (название) и все треки в нем (название, альбом, исполнитель).
#third()

