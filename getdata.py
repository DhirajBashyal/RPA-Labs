import connections as mysql1
class getDatas(object):
    def __init__(self):
        self.connection = mysql1.connectdb
        self.cursor = self.connection.cursor()
    def getAllData(self):
        self.cursor.execute("SELECT * from tbl_video_data WHERE 1;")
        aData = self.cursor.fetchall()
        return aData
    def insertData(self,aData):
        self.cursor.execute("INSERT INTO tbl_video_data(id, nameVideo, fileName, fileSize, fileDuration) VALUES(0,%s,%s,%s,%s)",(aData['nameVideo'],aData['fileName'],aData['fileSize'],aData['fileDuration']))
        self.connection.commit()
        return self.cursor.rowcount