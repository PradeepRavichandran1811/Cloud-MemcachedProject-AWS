#Name:PRADEEP RAVICHANDRAN
#ID:1001553352
#CSE 6331-Cloud Computing
#Assignment 6

import os
from flask import Flask, render_template, request
import sqlite3 as sql
import pandas as pd
import random
import time
import redis
import sqlite3, csv, base64

application = Flask(__name__)
con=sqlite3.connect('eq.db')

#creating cursor to perform database operations
cursor = con.cursor()
con.commit()

#@application.route are decorators in Flask
@application.route('/')
def index():
    return render_template('home.html')

@application.route('/netid')
def netid():
    return render_template('netid.html')

@application.route('/randr')
def randr():
    return render_template('random.html')

#Function using Amazon Elasticache-memcache
@application.route('/randomqueries',methods=['GET','POST'])
def randomqueries():
    red = redis.StrictRedis(host='memcachedcloud-001.y2bx3p.0001.use2.cache.amazonaws.com', port=6379, db=0)
    print("flushing")
    con = sql.connect("eq.db")
    first = request.form['netid']
    loop = request.form['number']
    letter = first + '%'
    print(letter)
    query = "select * from earthquake where net LIKE '%s' " % letter
    cursor = con.cursor()
    cursor.execute(str(query))
    ran = cursor.fetchall()
    li= list(ran)
    print(li)
    start = time.time()
    for i in range(0,int(loop)):
        r = random.choice(li)
        key = str(i)
        value = red.get(key)
        rows = []
        rows1 = []
        cursor.execute("select time from earthquake where net LIKE '%s' " % r)
        rows = cursor.fetchone()
        cursor.execute("select locationSource from earthquake where net LIKE '%s' " % r)
        rows1 = cursor.fetchone()
        if not value:
            cursor = con.cursor()
            cursor.execute("select net from earthquake where net LIKE '%s' " % r)
            count = cursor.rowcount
            cursor.close()
            red.set(key, count)
        if i == 0:
            ending = time.time()
            tot = ending - start
    end = time.time()
    total = end-start

    return render_template('randomresult.html',loop=loop,total=total,tot=tot,rows=rows,rows1=rows1)

#Random queries generating function without memcache
@application.route('/randomwithoutmemcache',methods=['GET','POST'])
def randomwithoutmemcache():
    con = sql.connect("eq.db")
    Number = request.form['number']
    triplets = int(Number)/3
    cursor = con.cursor()
    quer = "select * from earthquake"
    cursor.execute(str(quer))
    list1= []
    ran = cursor.fetchall()
    dic= list(ran)
    print(dic)
    start = time.time()
    for i in range(0, int(Number)):
        r = random.choice(dic)
        print(r)
    for i in range(0,int(triplets)):
        cursor = con.cursor()
        cursor.execute("Insert into earthquake (time,latitude,longitude) Values (2018-06-07 , 13 , 14)")
        rows = cursor.fetchall()
        cursor.execute("select Count(time) from earthquake")
        row = cursor.fetchone()
    end = time.time()
    total = end-start

    return render_template('randomresult1.html',total=total,rows=rows,row=row,Number=Number)

#function to generate random restricted queries without using memcache
@application.route('/randomrestrictedwithoutmemcache',methods=['GET','POST'])
def randomrestrictedwithoutmemcache():
    con = sql.connect("eq.db")
    con.row_factory = sql.Row
    count = request.form['number']
    query = 'select * from earthquake where place LIKE "%CA" AND mag <'
    lis=[]
    start = time.time()
    for i in range(0,int(count)):
        r = random.random()
        a = str((r * 5.5) + 0.5001)
        b = query + a
        cursor = con.cursor()
        cursor.execute(b)
        rows = cursor.fetchall()
        lis.append(rows)
        print(i)
        #print(rows)

    end = time.time()
    total = end-start

    return render_template('randomresresult.html',count=count,total=total,lis=lis)

#to get the size of the current working directory
@application.route('/getsize')
def getsize():
    cwd = os.getcwd()
    total_size = os.path.getsize(cwd)

    return render_template('size.html',size=total_size)

#to read CSV and to create a Table
@application.route('/csv', methods=['GET','POST'])
def csv():
    if request.method == 'POST':
        try:
            #converting csv file into table with values
            if request.method == 'POST':
                 file = request.files['myfile']
                 con = sqlite3.connect('eq.db')
                 con.row_factory = sql.Row
            csv = pd.read_csv(file)
            csv.to_sql(name="earthquake", con=con, if_exists="replace", index=False)
            cursor = con.cursor()
            cursor.execute("select * from earthquake")
            row = cursor.fetchall()
            con.close()

        except:
                con.rollback()
        finally:
            return render_template("home.html")
            con.close()
            print(msg)

#function to list the table
@application.route('/lists')
def lists():
    if request.method == 'POST':
        file = request.files['myfile']
    con = sqlite3.connect('eq.db')
    con.row_factory = sql.Row
    cursor = con.cursor()
    cursor.execute("select * from earthquake")
    row = cursor.fetchall()
    cursor.execute("select Count(mag) from earthquake")
    count = cursor.fetchall()

    return render_template("list.html", row=row,count=count)

if __name__ == '__main__':
    application.run(debug=True)

