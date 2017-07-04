'''
THE FOLLOWING CODE IS A SCRIPT WHICH CHECKS A SUBREDDITS LATEST POSTS FOR A CERTAIN AMOUNT OF VOTES
IF A POST HAS GATHERED X MANY UPVOTES, A PM IS SENT TO A USER WITH LINKS TO SAID POSTS

THIS SCRIPT WAS CODED BY /U/ZICHO
'''

import praw # reddit API
import time # time stuff

# avoid encoding errors

import sys

reload(sys)
sys.setdefaultencoding('utf8')

# open the link list file. create it if not present.

try:

    with open('link_list', 'r') as link_list_file:
        link_list = [line.strip() for line in link_list_file]

except IOError:
    
    print "Link list not found! Creating..."
    link_list_file = open('link_list', 'w+')

    link_list_file.close ()

    # read it. create the link list

    with open('link_list', 'r') as link_list_file:
        link_list = [line.strip() for line in link_list_file]


# close file when it has been read

link_list_file.close()

# load reddit settings from PRAW

reddit = praw.Reddit('botname')

# store days date in variable for readability

days_date = time.strftime("%d/%m/%Y")

# list of variables

subreddits_to_check = "subreddit" # the subreddit(s) to monitor. to use several, do "subreddit+subreddit"
 
redditors = ['user'] # list of usernames which will get PMs. may switch this to a file instead, but it does nicely for small usage

score_limit = 20 # you will be notified of posts equal to or above this value

subreddit = reddit.subreddit(subreddits_to_check) # store the subreddit(s) in a variable

new_link = False # a boolean which will become true if new links are found, to trigger some events

new_link_list = [] # links will get stored here and then written to our link file

message_list = [] # messages append to this list
 
for submission in subreddit.top('day'):

    # if post has more or equal to score_limit, and is not yet added to our list, we add it

    link = submission.permalink 
   
    if submission.score >= score_limit and link not in link_list:

        message = "**" + submission.title + "**\n" + "  \n" + "URL: " + submission.url + " \n" + " \n" + "View on reddit: " + submission.permalink + " \n"

        message_list.append(message + "\n")

        new_link_list.append(link)

        new_link = True # a new link is found

    time.sleep(2) # sleep two seconds as a courtesy to reddit servers         

if new_link: # if a new link was found when script ran, open up link file to append the new links to it.
    
    try:
        
        link_list_file = open('link_list', 'a')
    
    except IOError:
        print "Error opening link file. Aborting..."
        sys.exit()

    for link in new_link_list:

        link_list_file.write(link + "\n")


link_list_file.close()

# Send the actual PM

if new_link:

   subject = "Links gathered on " + days_date                                                                                                                                                                     
   message = ""

   for m in message_list:
                                                                                                                                                                                         
       message += m

   for redditor in redditors:

       reddit.redditor(redditor).message(subject, message)
       time.sleep(2)

sys.exit() # bye
