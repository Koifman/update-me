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
		database = jewsql.Database('jewsofhazard')
		
		r = praw.Reddit(user_agent='/u/JewsOfHazard made UpdateMe Script')
		o = OAuth2Util.OAuth2Util(r)
		while True:
			try:
				user_values = database.get_user_values()
				read_posts = database.get_post_values()
				subreddits = list()
				users = list()
				checked_posts = list()
				for row in user_values:
					subreddits.append(row[1])
					users.append(row[0])
				for row in read_posts:
					checked_posts.append(row[0])
				print (users)
				print (subreddits)
				print (checked_posts)
				temp_checked_posts = list()
				o.refresh()
				for user in users:
					subreddit_list = subreddits[users.index(user)].split(',')
					for sub in subreddit_list:
						try:
							try:
								subreddit = r.get_subreddit('{}'.format(sub))
							except:
								print(user, "has no followed subreddits.")
							submissions = subreddit.get_new(limit=10)
							for post in submissions:
								if post.id not in checked_posts:
									try:
										if post.id not in checked_posts:
											temp_checked_posts.append(post.id)
											
										r.send_message(user,'New Post in /r/{}'.format(sub), '[{}](https://reddit.com/u/{})'.format(post.author,post.author) + ' submitted ' + '[\"{}\"]({})'.format(post.title, post.url))
										print('Message sent to {} from the subreddit {} about the post titled: {}'.format(user, sub, post.title))
									except:
										print("A post has a character not supported.")
										traceback.print_exc()
						except praw.errors.Forbidden:
							r.send_message(user, "I'm sorry, but I can't view posts from {}".format(sub), "For the time being, I have removed {0} from your list of followed subreddits. Please contact the moderators of {0} to allow me to view their subreddit.".format(sub))
							database.delete_user_subreddit(user,sub)
							print(sub, 'forbidden')
			except praw.errors.RateLimitExceeded:
				print('Rate limit exceeded, sleeping 10 minutes.')
				time.sleep(300)
			except praw.errors.HTTPException:
				print('There was a problem connecting to reddit.')
				traceback.print_exc()
				time.sleep(300)
			for post in temp_checked_posts:
				if post not in checked_posts:
					checked_posts.append(post)
					database.insert_post(post)
					print(post, 'was added to the database')
			print('Sleep 300')
			time.sleep(300)
			
	except sqlite3.OperationalError:
		print('Something went wrong connecting to the database.')
		traceback.print_exc()
		exit()
	except:
		print('Something went wrong, notifying JewsOfHazard.')
		traceback.print_exc()
		time.sleep(600)
