import pymysql

class database: 
    
    def __init__(self):
        self.con = None
        self.cursor = None
    
    def connectDb(self):
        self.con = pymysql.connect(
            host="localhost",
            user="root",
            password="Harsha@#6988",
            database="todoDb"
        )
        self.cursor = self.con.cursor()
        # self.cursor.execute("drop table tasks")
        # self.cursor.execute("describe tasks")
    
    def createRows(self , data):
        task , status = data
        self.cursor.execute("insert into tasks (task , status) values (%s,%s) " , (task, status))
        self.con.commit()
    
    def readRows(self):
        self.cursor.execute("select * from tasks")
        records = self.cursor.fetchall()
        return records
    
    def updateRows(self , data):
        id , task , status = data
        self.cursor.execute("update tasks set task = %s , status=%s where id = %s " , (task,status , id))
        self.con.commit()
    
    def deleteRows(self , id):
        self.cursor.execute("delete from tasks where id = %s" , id)
        self.con.commit()
        
    def createTable(self):
        self.cursor.execute("create table tasks (id INT primary key auto_increment , task varchar(255) , status varchar(255) )")
        self.con.commit()
    
testing = database()
testing.connectDb()
# testing.createTable()

print("Done")