import praw
import csv
import time
from os import listdir

# use users who post on sad subreddits' text to classify as depressed
subs = set()

# subs.add('depression')
with open('src/ucSubs.txt', 'r') as txt:
    for line in txt:
        if line[0] != '*' and 'r/' in line:
            sub = line.split('r/')[1].strip()
            subs.add(sub)
print(subs)

r = praw.Reddit(username = "WebsterBot",
    password = "G*c-+#6d^8V%$_6=",
    client_id = "_fRmFVzOM5jYHQ",
    client_secret = "o_jPN2Mou9UbAJzN5I3zybCaKjo",
    user_agent = "actualsnek wtwbot test 0.0")
'''
for sub in subs:
    users = set()
    print('SUB:', sub)
    writer = csv.writer(open('src/ucUsers.csv', 'a'))
    for p in r.subreddit(sub).top(time_filter='month'): # CHANGE: year?
        if p.score > 100 and p.author:
            print(p.author)
            users.add(p.author)
            for c in p.comments:
                if isinstance(c, praw.models.Comment) and c.author and c.score > 0:
                    users.add(c.author)
                    if len(c.replies) > 0:
                        for child in c.replies.list():
                            if isinstance(child, praw.models.Comment) and child.author and child.score > 0:
                                users.add(child.author)
    for user in users:
        writer.writerow([user.name])
    print('LEN:', len(users)) # users who've commented on sub in past day

'''
users = set()
with open('src/ucUsers.csv', 'r') as userList:
	for u in userList:
		users.add(praw.models.Redditor(reddit=r, name=u.strip()))
print('TOTAL LEN:', len(users))

def commentData(c):
    return (c.subreddit.display_name, c.id, c.parent_id, c.created_utc, c.body)

worked, errored = 0, 0

for user in users:
    if '%s.csv' % user.name not in listdir('src/ucUsers'):
        print(user)
        # count = {}
        saved = []
        comments = user.comments.new()
        try:
            worked += 1
            for comment in comments:
                saved.append(comment)
                if time.time() - comment.created_utc > 2592000: # past 30 days
                    break
            writer = csv.writer(open('src/ucUsers/%s.csv' % user.name, 'w'))
            writer.writerow(('subreddit', 'self ID', 'parent ID', 'time', 'text'))
            for comment in saved:
                # print(commentData(comment))
                writer.writerow(commentData(comment))
        except:
        	errored += 1
        	continue

print(worked, errored, worked + errored)
#'''