import pymysql 

class database:
    con = None
    cursor = None

    def connectDb(self):
        self.con = pymysql.connect(
            host = "localhost",
            user="root",
            password="Harsha@#6988",
            database="users"
        )
        self.cursor = self.con.cursor()

    def register(self , data):
        name , password = data
        self.cursor.execute("insert into userdata (name,password) values (%s,%s) " , (name,password))
        self.con.commit()

    def login(self , data):
        id , password = data
        self.cursor.execute("select * from userdata where id = %s" , (id,))
        user = self.cursor.fetchall()
        for i in user:
            id , nameDB , passwordDB = i
            if password == passwordDB:
                return 1
        return 0


