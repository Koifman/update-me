__author__ = "JewsOfHazard"
__date__ = "$Nov 21, 2015 10:42:38 PM$"

import traceback
import praw
import time
import OAuth2Util
import jewsql
import sqlite3

if __name__ == "__main__":
	try:
		database = jewsql.Database('YOUR_DATABASE')
		data = database.get_user_values('users')
		subreddits = list()
		users = list()
		for row in data:
			subreddits.append(row[1])
			users.append(row[0])
		print (users)
		print (subreddits)
		checked_posts = list()
		
		r = praw.Reddit(user_agent='/u/JewsOfHazard made UpdateMe Script')
		o = OAuth2Util.OAuth2Util(r)
		while True:
			try:
				temp_checked_posts = list()
				o.refresh()
				for user in users:
					subreddit_list = subreddits[users.index(user)].split(',')
					for sub in subreddit_list:
						subreddit = r.get_subreddit('{}'.format(sub))
						submissions = subreddit.get_new(limit=2)
						for post in submissions:
							if post.id not in checked_posts:
								try:
									if post.id not in checked_posts:
										temp_checked_posts.append(post.id)
										print(post.id, "was added to checked posts.")
									r.send_message(user,'New Post in /r/{}'.format(sub), '[{}](https://reddit.com/u/{})'.format(post.author,post.author) + ' submitted ' + '[\"{}\"]({})'.format(post.title, post.url))
									print('Message sent to {} from the subreddit {} about the post titled: {}'.format(user, sub, post.title))
								except:
									print("A post has a character not supported.")
									traceback.print_exc()
				checked_posts = checked_posts + temp_checked_posts
				time.sleep(60)
			except praw.errors.HTTPException:
				print('There was a problem connecting to reddit.')
				time.sleep(600)

	except sqlite3.OperationalError:
		print('Something went wrong connecting to the database.')
		traceback.print_exc()
		exit()
	except:
		print('Something went wrong, notifying JewsOfHazard.')
		traceback.print_exc()
		time.sleep(600)
