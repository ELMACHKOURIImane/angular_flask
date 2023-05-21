# from flask import Flask  , render_template ,request

# from flask_mysqldb import MySQL 

# app = Flask(__name__, template_folder='./template')

# app.config['MYSQL_HOST'] = "localhost"
# app.config['MYSQL_USER']  = "root"
# app.config['MYSQL_PASSWORD'] = ""
# app.config['MYSQL_DB'] = "users"


# mysql = MySQL(app)

# @app.route('/', methods=['GET' , 'POST'])
# def hello():

#     if request.method == 'POST':
#         username = request.form['email']
#         password = request.form['password']
#         cur = mysql.connection.cursor()
#         cur.execute("INSERT INTO user (email,password) VALUES (%s , %s) " , (username , password))
#         mysql.connection.commit()
#         cur.close()

#         return "Succes"


#     return render_template("index.html")
# @app.route('/users')
# def users():
#     cur = mysql.connection.cursor()
#     users = cur.execute("SELECT * FROM user ")

#     if users > 0 :
#         userDetails = cur.fetchall()
#         return render_template('users.html' , userDetails=userDetails)



# if __name__ == "__main__":
#     app.run(debug=True)

import os
from flask import Flask, redirect, request  , jsonify
import myCar as car
import json
from flask_mysqldb import MySQL 
from flask_cors import CORS, cross_origin
import mysql.connector 
import user  as myuser
from flask_jwt_extended import JWTManager, create_access_token
from flask_jwt_extended import jwt_required
import bcrypt

app = Flask(__name__)
cors = CORS(app)
app.config['JWT_SECRET_KEY']="super-secret"
app.config['JWT_TOKEN_LOCATION'] = ['headers']
jwt = JWTManager(app)
mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="carsdb"
        )
   
# les web methods 
@app.route('/savecar' , methods = ['POST'])

@jwt_required()
def saveCar():
    args = request.json
    id_car = args.get('id')
    model = args.get('model')
    hp = args.get('hp')
    marque = args.get('marque')

    myCursor = mydb.cursor()

    mycar = car.Car(0 , model ,hp , marque )
    req = "insert into cars (model , hp , marque ) values (%s , %s , %s)"
    val = (mycar.model , mycar.hp , mycar.marque)
    myCursor.execute(req , val)
    mydb.commit()
    print(myCursor.rowcount, "record ins")

  
    return "Saved : "


@app.route('/cars' , methods = ['GET'])
@jwt_required()
def getCars():
    mylist = []
    req = "select * from cars"
    
    myCursor = mydb.cursor()
    myCursor.execute(req)
    myresult = myCursor.fetchall()
    for x in myresult:
        mylist.append(car.Car(x[0] ,x[1], x[2] , x[3]).__dict__)

    return json.dumps(mylist)




@app.route('/delete/<int:id_car>' , methods=['DELETE' , 'GET' , 'POST'])
@jwt_required()
def delete(id_car):
    req = "DELETE FROM cars WHERE  id_car = {0}".format(id_car)
    cur = mydb.cursor()
    cur.execute(req)
    mydb.commit()
    return "Deleted succefully"




@app.route('/update/<int:id>' , methods=['POST' , 'GET'])
@jwt_required()
def update(id):
    args = request.json
    model = args.get('model')
    hp = args.get('hp')
    marque = args.get('marque')


    req = "UPDATE cars SET model = %s ,  hp = %s , marque = %s   WHERE id_car = %s"
    value = (model , hp , marque , id)
    cur = mydb.cursor()
    cur.execute(req , value)
    mydb.commit()
    
    return "Success" 


@app.route('/car/<int:id>' , methods=['GET'])
def getOne(id):
    req = "SELECT * FROM cars WHERE id_car = {0}".format(id)
    cur = mydb.cursor()
    cur.execute(req)
    resultat = cur.fetchone()

    return json.dumps(resultat)

@app.route('/adduser' , methods=['POST'])
def saveUser():
    args = request.json
    id = args.get('id')
    username = args.get('username')
    password = args.get('password')

    myCursor = mydb.cursor()
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf8'), salt)
    user = myuser.User(0 , username , hashed_password)
    req = "insert into users (username, password) values (%s , %s )"
    val = (user.username , user.password) 
    myCursor.execute(req , val)
    mydb.commit()
    access_token = create_access_token(identity=username)
    return jsonify({"status": "success", "data": {"token": access_token}}), 201

@app.route("/login" , methods=['POST'])
def login():
   try:
        username = request.json.get("username", None)
        password = request.json.get("password", None)

        if not username or not password or len(username) < 3 or len(password) < 3:
            return jsonify({"data": "Bad username or password"}), 401

        cursor = mydb.cursor()
        req = "SELECT * FROM users WHERE username = %s"
        val = (username,)
        cursor.execute(req, val)
        result = cursor.fetchone()
        if result is None:
            return jsonify({"status": "error", "data": "Bad username or password"}), 401
        user = myuser.User(0,result[1], result[2])
        compare_passwords = bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8'))
        if not compare_passwords:
            return jsonify({"status": "error", "data": "Bad username or password"}), 401
        access_token = create_access_token(identity=username)
        return jsonify({"status": "success", "data": {"token": access_token}}), 201
   except Exception as e:
        print(e)
        return jsonify({"status": "error", "data": "An error has occurred"}), 401
    
    

    



if __name__ == '__main__':
   app.run(debug=True)
