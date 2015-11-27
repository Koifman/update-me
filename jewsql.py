__author__ = "JewsOfHazard"
__date__ = "$Nov 23, 2015 12:03:42 AM$"

import sqlite3
import sys

class Database:
	def __init__(self,database):
		try:
			self.con = sqlite3.connect('{}.db'.format(database))
			self.cur = self.con.cursor()
		except:
			print('There is no database with that name.')
	def create_table(self):
		try:
			self.cur.execute("CREATE TABLE users(Username VARCHAR(30), Subreddits VARCHAR(500))")
			self.con.commit()
		except sqlite3.OperationalError:
			print('Table already exists.')
	def get_user_values(self,table):
		self.cur.execute('SELECT Username, Subreddits FROM {}'.format(table))
		return self.cur.fetchall()
	def user_has_subreddit(self, username, subreddit):
		data = self.get_user_values('users')
		for row in data:
			if str(row[0]).lower() == username.lower():
				temp = row[1].split(',')
				for item in temp:
					if subreddit.lower() == item.lower():
						return True
		return False
	def user_in_database(self, username):
		self.cur.execute("SELECT * FROM users WHERE Username='{}'".format(username))
		if self.cur.rowcount != 0:
			return True
		return False
	def add_user_subreddit(self, username, subreddit): #ONLY EVEN USE INSERT_VALUES
		self.cur.execute("SELECT Subreddits FROM users WHERE Username='{}'".format(username))
		temp = self.cur.fetchone()
		self.cur.execute("UPDATE users SET Subreddits='{}' WHERE Username='{}'".format(temp[0] + ',' + subreddit,  username))
		self.con.commit()
	def delete_user_subreddit(self, username, subreddit):
		data = self.get_user_values('users')
		for row in data:
			if str(row[0]).lower() == username.lower():
				subreddits = row[1].split(',')
				temp = list()
				for sub in subreddits:
					if sub != subreddit:
						temp.append(sub)
				temp_string = ",".join([str(item) for item in temp])
				self.cur.execute("SELECT Subreddits FROM users WHERE Username='{}'".format(username))
				temp = self.cur.fetchone()
				self.cur.execute("UPDATE users SET Subreddits='{}' WHERE Username='{}'".format(temp_string,  username))
		self.con.commit()
	def insert_values(self, username, subreddit):
		if not self.user_in_database(username):
			self.cur.execute("INSERT INTO users VALUES('{}', '{}')".format(username,subreddit))
		elif not self.user_has_subreddit(username, subreddit):
			self.add_user_subreddit(username, subreddit)
		self.con.commit()
		
	def close_connection(self):
		self.cur.close()
		self.con.close()
		

		
if __name__ == '__main__':
	database = Database('NAME_OF_YOUR_DATABASE')
	#database.create_table()
	#database.insert_values('YOUR_USERNAME','YOUR_SUBREDDIT')
	#data = database.get_user_values('users')
	
	#for row in data:
		#print(row[0],row[1])