__author__ = "JewsOfHazard"

import traceback
import praw
import OAuth2Util
import jewsql
import time

if __name__ == "__main__":
	try:
		database = jewsql.Database('YOUR_DATABASE')
		
		r = praw.Reddit(user_agent='DatabaseManager for /u/________ UpdateMe Script')
		o = OAuth2Util.OAuth2Util(r)
		while True:
			try:
				o.refresh()
				read_messages = list()
				unread_messages = r.get_unread()

				for message in unread_messages:
					split_message = str(message).split(' ')[1:3]
					print(split_message)
					if split_message[0].lower() in ['add','follow','subscribe']:
						database.insert_values(str(message.author),split_message[1])
						message.reply("{}, you have added {} to your followed subreddits list.".format(str(message.author),split_message[1]))
					elif split_message[0].lower() in ['del','delete','remove']:				
						database.delete_user_subreddit(str(message.author),split_message[1])
						message.reply("{}, you have successfully unfollowed /r/{}.".format(str(message.author),split_message[1]))
					elif split_message[0].lower() == 'list':
						temp_list = list()
						data = database.get_user_values('users')
						for row in data:
							if str(row[0]).lower() == str(message.author).lower():
								temp = row[1].split(',')
								for item in temp:
									temp_list.append(item)
						temp[0] = "\n \n * " + temp[0]
						formatted_temp_list = "\n * ".join([str(item) for item in temp])
						r.send_message(str(message.author), 'The subreddits you asked for sir.', '{}, you are following the following subreddits: {}'.format(str(message.author),formatted_temp_list))
						message.reply('I have sent you a message regarding your followed subreddits.')
					else:
						message.reply("Commands|Function \n :--|:-- \n /u/JewBot9K add subreddit|Add a subreddit to your list. \n /u/JewBot9K del subreddit|Remove subreddit from your list. \n /u/JewBot9K list|Sends you a private message of your followed subreddits.")
					read_messages.append(message)
					message.mark_as_read()
				time.sleep(5)
			except praw.errors.HTTPException:
				traceback.print_exc()
				time.sleep(600)
	except:
		traceback.print_exc()