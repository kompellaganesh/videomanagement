import psycopg2
from config import  config
from routes.uploadvideo_handler import cursor
def listvideos():
    cursor.execute("select videoname,videopath,thumbnailpath,language,leadcast from videos")
    allrows=cursor.fetchall()
    responsedict=[]
    for row in allrows:
        if row[1]!=None:
            if len(row[1])>0:
                mydict={
                    "videoname":row[0],
                    "videopath":row[1],
                    "thumbnailpath":row[2],
                    "language":row[3],
                    "cast":row[4]
                }
                responsedict.append(mydict)
    return {
        "Movies":responsedict
    }