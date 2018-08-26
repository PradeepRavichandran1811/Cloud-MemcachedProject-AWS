from pandas import read_csv
import sqlite3

con = sqlite3.connect('eq.db')

data = read_csv('all_month.csv')
data.to_sql('earthquake',con, if_exists='append', index=False )

cur=con.cursor()
cur.execute('SELECT * FROM \'all\'')
d = cur.fetchall()
for d_ in d:
    print(d_)