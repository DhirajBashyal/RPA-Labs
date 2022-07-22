from flask import Flask, request, jsonify
from random import randint
from moviepy.editor import VideoFileClip
import os
import getdata

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "uploads/"
app.config['MAX_CONTENT_LENGTH'] = 1024*1024*1024
ALLOWED_EXTENSIONS = set(['mp4', 'mkv'])


def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def getData():
  ObjectData = getdata.getDatas()
  aData = ObjectData.getAllData()
  if len(aData):
    response = jsonify({
      "result" : aData,
      "status" : 200,
    })
  else:
    response = jsonify({
      "result" : [],
      "status" : 400,
    })
  return response

@app.route("/calculate",methods =["POST"])
def calculatePrice():
  videoSize = int(request.form.get('videoSize', type=int) or 0) #in mb
  videoType = request.form.get('videoType') #type
  videoLength = int(request.form.get('videoLength', type=int) or 0) #in seconds
  priceD = 5.99
  priceForLen = 12.5
  if videoSize > 500:
    priceD = 12.50
  if videoLength > 6*60+18: #6min 18sec
    priceForLen = 20

  priceFinal = priceD + priceForLen
  response = jsonify({
    "result": ["Price Calculated: $" + str(round(priceFinal, 2))],
    "status": 501,
  })
  return response

@app.route("/insertData",methods =["POST"])
def insertData():
  file_ = request.files['video_file']
  if allowed_file(file_.filename):
    fileName = str(randint(100000, 9999999))
    fileExt = '.' in file_.filename and file_.filename.rsplit('.', 1)[1].lower() #get extension from filename
    file_.save("upload/"+str(fileName)+"."+fileExt) #give a random name to file
    fileSize = os.stat("upload/"+str(fileName)+"."+fileExt).st_size #for size
    clip = VideoFileClip("upload/"+str(fileName)+"."+fileExt) #get Video Details from File
    #validation starts
    if fileSize > 1024*1024*1024:
      response = jsonify({
        "result": ["File Size is Greater than 1GB"],
        "status": 501,
      })
    else:
      if clip.duration < 10*60:
        data = {'nameVideo': request.form.get('name'), 'fileSize': fileSize, 'fileDuration': clip.duration, 'fileName': fileName+"."+fileExt}
        ObjectData = getdata.getDatas()
        insertedCount = ObjectData.insertData(data)
        response = jsonify({
          "result": ["Data Inserted"],
          "status": 501,
        })
      else:
        response = jsonify({
          "result": ["File Size is Greater than 1GB"],
          "status": 501,
        })
  else:
    response = jsonify({
      "result": "File Extension not Valid MP4 or MKV",
      "status": 501,
    })
  return response
app.run("0.0.0.0",debug = True)