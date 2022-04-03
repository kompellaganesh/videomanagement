from config import  config
from flask import request,make_response,copy_current_request_context
from services.videouploadservice import uploadvideoservice
import threading
import time
import boto3
import psycopg2

#Establishing the connection
conn = psycopg2.connect(
   database=config.configurations['database']['database'], 
   user=config.configurations['database']['user'], 
   password=config.configurations['database']['password'], 
   host=config.configurations['database']['host'], 
   port= config.configurations['database']['port']
)
#Setting auto commit false
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()
def uploadvideo():
    @copy_current_request_context
    def save_file(closeAfterWrite,closeAfterWrite1,videoID):
        videoname = request.form['videoname']
        cast = request.form['cast']
        video = request.files['video']
        thumbnail = request.files['thumbnail']
        status = uploadvideoservice(videoname,cast,video,thumbnail)
        if status:
            print(videoname,"-uploaded succesfully",time.localtime())
            sqlquery = "UPDATE Videos SET VideoPath = "+"'"+config.configurations['aws']['cdnlink']+"/"+video.filename+"'"+"WHERE VideoID = {}".format(videoID)
            updateInDB(sqlquery)
            sqlquery = "UPDATE Videos SET ThumbnailPath = "+"'"+config.configurations['aws']['cdnlink']+"/"+thumbnail.filename+"'"+"WHERE VideoID = {}".format(videoID)
            updateInDB(sqlquery)
        closeAfterWrite()
        closeAfterWrite1()
    def passExit():
        pass
    videoname = request.form['videoname']
    language = request.form['language']
    cast = request.form['cast']
    video = request.files['video']
    thumbnail = request.files['thumbnail']
    sqlquery = "INSERT INTO Videos (VideoName,LeadCast,Language) Values ('"+videoname+"','"+cast+"','"+language+"') RETURNING videoid"
    normalExit = video.stream.close
    normalExit1 = thumbnail.stream.close
    video.stream.close = passExit
    thumbnail.stream.close = passExit
    videoID = insertInDB(sqlquery)
    t = threading.Thread(target=save_file,args=(normalExit,normalExit1,videoID,))
    t.start()
    mydict={
        "status":"success"
    }
    return mydict

def insertInDB(sql):
    print(sql)
    cursor.execute(sql)
    id_of_new_row = cursor.fetchone()[0]
    print(id_of_new_row)
    return id_of_new_row

def updateInDB(sql):
    cursor.execute(sql)
