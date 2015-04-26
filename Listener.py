# -*- coding: utf-8 -*-
# userAccount.py
"""
Version: 4.26.2015
@author: Luke_Wortsmann
"""

from userAccount import *
import MySQLdb

connection = MySQLdb.connect(host = "stockforecast.ga", user = "root", passwd = "plywood", db = "forecast")

cursor = connection.cursor()
cursor.execute("select id, name, user_login, user_password, email from users")
data = cursor.fetchall()


users = {}
for row in data:
    newUser = userAccount(row[2],row[4],row[1],row[3],row[0])
    users[row[2]] = newUser

cursor.close ()
connection.close ()
