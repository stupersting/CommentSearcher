import praw
import pdb
import re
import os
import time
import sys
import codecs as codex



if(len(sys.argv) < 2):
	keywordArray = ["default"]
else:
	keywords = sys.argv[1]
	keywordArray = keywords.split("~:~")


if(len(sys.argv) > 2):
	if(sys.argv[2].lower() == "context"):
		includeContext = True
	else:
		includeContext = False
else:
	includeContext = False
	

if(len(keywordArray) > 30):
	secureKeywords1 = keywordArray[:30]
elif(len(keywordArray) < 1):
	secureKeywords1 = ["default"]
else:
	secureKeywords1 = keywordArray
	
secureKeywords = []
for words in secureKeywords1:
	if("&" in words):
		if re.search('[a-zA-Z0-9]', words):
			words = words.replace("&", ")(?=.*")
			words = "(?=.*"+words+")"
		else:
			words = ""
	secureKeywords.append(words)
secureKeywords = list(filter(None, secureKeywords))
print(secureKeywords)


# Create the Reddit instance
reddit = praw.Reddit('bot')

store = False

# Have we run this code before? If not, create an empty list
if not os.path.isfile("posts_replied_to.txt"):
	posts_replied_to = []
else: # If we have run the code before, load the list of posts we have replied to
    # Read the file into a list and remove any empty values
	with open("posts_replied_to.txt", "r") as f:
		posts_replied_to = f.read()
		posts_replied_to = posts_replied_to.split("\n")
		posts_replied_to = list(filter(None, posts_replied_to))

		
# Have we run this code before? If not, create an empty list
if not os.path.isfile("lastPosted.txt"):
	lastPosted = [0,0,0]
else: # If we have run the code before, load the list of previous posts
    #Read the file into a list and remove any empty values
	with open("lastPosted.txt", "r") as lastPost:
		lastPosted = lastPost.read()
		lastPosted = lastPosted.split("\n")
		lastPosted = list(filter(None, lastPosted))

# Have we run this code before? If not, create an empty list
if not os.path.isfile("lastID.txt"):
	lastID = []
else: # If we have run the code before, load the list of previous posts
    #Read the file into a list and remove any empty values
	with open("lastID.txt", "r") as lastPostID:
		lastID = lastPostID.read()
		lastID = lastID.split("\n")
		lastID = list(filter(None, lastID))

if(len(lastID) == 0):
	lastCommentID = 0
else:
	lastCommentID = lastID[-1]
		
		
		
listOfTimes = []
mostRecentID = 0;
num = 0
masterString = ""

subredditToSearch = "all"
'''
for sub in removeSubs:
	subredditToSearch = subredditToSearch + "-" + sub
'''
# Get the top 5 values from our subreddit
for comment in reddit.subreddit(subredditToSearch).comments(limit=500):
	num = num + 1
	listOfTimes.append(comment.created_utc)
	if(mostRecentID == 0):
		mostRecentID = comment.id
	if(str(comment.id) == str(lastCommentID)):
		break
	
	#if(len(lastPosted) == 0):
	#	TimeSinceLastPost = 10000
	#else:
	#	TimeSinceLastPost = int(round(time.time())) - int(lastPosted[-1])
	
	#create our Regex
	if(len(secureKeywords) > 1):
		regExpress = secureKeywords[0]
		for keyw in secureKeywords[1:]:
			regExpress = regExpress + "|" + keyw
	else:
		regExpress = secureKeywords[0]
	
	if re.search(regExpress, comment.body, re.IGNORECASE):
		fullstringmeta = "\n<><><>-------------- POST INFO --------------<><><>\n"
		fullstringmeta = fullstringmeta + "SUBREDDIT: " + str(comment.subreddit)
		fullstringmeta = fullstringmeta + "\n" + "POST: " + str(comment.submission.title)
		fullstringmeta = fullstringmeta + "\n" + "POST AUTHOR: " + str(comment.submission.author)
		fullstringmeta = fullstringmeta + "\n" + "POST CREATED: " + str(comment.submission.created_utc)
		if(len(str(comment.submission.selftext)) != 0):
			fullstringmeta = fullstringmeta + "\n\n" + "POST SELF TEXT: \n" + str(comment.submission.selftext)	
		fullstring =  "\n<><><>------------- COMMENT INFO -------------<><><>\n"
		fullstring = fullstring + "\n" + "AUTHOR: " + str(comment.author)
		fullstring = fullstring + "\n" +""
		fullstring = fullstring + "\n" + str(comment.body)
		fullstring = fullstring + "\n" +""
		fullstring = fullstring + "\n" + "UNIX TIME POSTED: " + str(comment.created_utc)
		fullstring = fullstring + "\n" +"comment ID: " + str(comment.id)
		fullstring = fullstring + "\n\n" +"<><><>-------<><><>-------<><><>-------<><><>-------<><><>-------<><><>-------<><><>-------<><><>-------<><><>-------<><><>\n" 
		fullstring = fullstring +"<><><>-------<><><>-------<><><>-------<><><>-------<><><>-------<><><>-------<><><>-------<><><>-------<><><>-------<><><>\n" 
		fullstring = fullstring +"<><><>-------<><><>-------<><><>-------<><><>-------<><><>-------<><><>-------<><><>-------<><><>-------<><><>-------<><><>\n" 
		fullstring = fullstring +"<><><>-------<><><>-------<><><>-------<><><>-------<><><>-------<><><>-------<><><>-------<><><>-------<><><>-------<><><>\n" 
		fullstring = fullstring +"<><><>-------<><><>-------<><><>-------<><><>-------<><><>-------<><><>-------<><><>-------<><><>-------<><><>-------<><><>\n" 
		print(fullstringmeta)
		print(fullstring)
		masterString = masterString + fullstringmeta
		if(includeContext):
			parent = comment.parent()
			parentTexth = ""
			parentText = ""
			parentTexth = parentTexth +"\n<><><>-------------- PARENT COMMENTS --------------<><><>\n"
			topLevel = True
			while parent != comment.submission:
				if(topLevel):
					topLevel = False
				parentText = "\n\n<><><>---------------------------------------------------<><><>\n" + parentText
				parentText = str(parent.body) + parentText
				parentText = "UNIX TIMESTAMP: " + str(parent.created_utc) + "\n\n" + parentText
				parentText = "\nAUTHOR: " + str(parent.author) + "\n" + parentText
				parent = parent.parent()
			if(topLevel):
				parentText = parentText + "\n------- This comment is a top level comment! -------"
			masterString = masterString +"\n"+ parentTexth+parentText
			
		masterString = masterString +"\n"+fullstring
		
	'''
    #If we haven't replied to this post before
	if TimeSinceLastPost > 600000 and submission.id not in posts_replied_to:
        # Do a case insensitive search
		if re.search("i love python", submission.title, re.IGNORECASE):
            # Reply to the post
           # submission.reply("991882test991882")
			print("Bot replying to : ", submission.title)

            # Store the current id into our list
			posts_replied_to.append(submission.id)
			lastPosted.append(round(time.time()))
			print(lastPosted)
			store = True
			break
	else:
		if TimeSinceLastPost < 600000:
			print("Not time to post yet.")
			break
		else:
			print("No posts to comment on.")
		'''

		
print("Time interval between the oldest and newest comment scanned: " + str(listOfTimes[1] - listOfTimes[-1]))
print("\n\n             =~=~= Retrieved " + str(num)+ "/500 maxmimum comments. =~=~=  \n\n\nIf this number is 500/500, the bot is unable to keep up with the new comments being submitted.\nIt is likely that some comments are going to be missed.\n")
# Write our updated list back to the file
with open("posts_replied_to.txt", "w") as f:
	for post_id in posts_replied_to:
		f.write(post_id + "\n")
		
with open("lastPosted.txt", "w") as lastPostUpdate:
		lastPostUpdate.write(str(lastPosted[-1]) + "\n")
		
with open("lastID.txt", "w") as lastPostUpdate:
	lastPostUpdate.write(str(mostRecentID) + "\n")
	
	
fileTooBig = False
if os.path.isfile("chatlog.txt"):
	sizeOfFile = os.path.getsize("chatlog.txt")
	if sizeOfFile > 100000000:
		fileTooBig = True
		print("\n          <><><><><><><><><><> COULD NOT SAVE RESULTS! LOG FILE SIZE HAS GROWN TOO LARGE! <><><><><><><><><><>\n")

if fileTooBig == False and (num == 500):
	with codex.open("chatlog.txt", "a", "utf-8") as log:
		log.write("\n\n\n<><><> UNABLE TO READ ALL COMMENTS AT UNIX TIME: "+str(round(time.time()))+" <><><>\n\n")		
		

if masterString != "" and fileTooBig == False:
	regexToShow = regExpress.replace("|", "~:~")
	regexToShow = regexToShow.replace(")(?=.*","&")
	regexToShow = regexToShow.replace("(?=.*","")
	regexToShow = regexToShow.replace(")","")
	regexToShow = regexToShow.replace("(","")
	'''
	avoidedSubs = ""
	for subred in removeSubs:
		avoidedSubs = avoidedSubs + ", " + str(subred)
	if avoidedSubs == "":
		avoidedSubs = "<> No subreddits were excluded! <>"
	else:
		avoidedSubs = avoidedSubs[1:]
	'''
	masterString = " \n<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\nSEARCH EXPRESSION: \"" + regexToShow +"\" INCLUDE-CONTEXT: "+str(includeContext)+"\n<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n" + masterString
	masterString = bytes(masterString, 'utf-8').decode('utf-8','ignore')
	with codex.open("chatlog.txt", "a", "utf-8") as log:
		log.write("\n" + masterString + "\n")
