import praw
import csv
import time
from os import listdir

subs = set() # Load in list of subs
with open('data/sadboi/subs.txt', 'r') as txt:
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
for sub in subs: # Fetch users from subs
    users = set()
    print('SUB:', sub)
    writer = csv.writer(open('data/sadboi/users.csv', 'a'))
    for p in r.subreddit(sub).top(time_filter='year'): 
        if p.score > 20 and p.author:
            print(p.author)
            users.add(p.author)
            for c in p.comments:
                if isinstance(c, praw.models.Comment) and c.author and c.score >= 1:
                    users.add(c.author)
                    if len(c.replies) > 0:
                        for child in c.replies.list():
                            if isinstance(child, praw.models.Comment) and child.author and child.score >= 1:
                                users.add(child.author)
    for user in users:
        writer.writerow([user.name])
    print('LEN:', len(users))
'''

users = set() # Load list of users into mem and remove duplicates
with open('data/sadboi/users.csv', 'r') as userList:
	for u in userList:
		users.add(praw.models.Redditor(reddit=r, name=u.strip()))
print('TOTAL LEN:', len(users))

def commentData(c):
    return (c.subreddit.display_name, c.id, c.parent_id, c.created_utc, c.body)

worked, errored = 0, 0

for user in users: # generate comment csv's for users
    if '%s.csv' % user.name not in listdir('data/sadboi/users'):
        print(user)
        comments = user.comments.new()
        try:
            writer = csv.writer(open('data/sadboi/users/%s.csv' % user.name, 'w'))
            for comment in comments:
                if time.time() - comment.created_utc > 31556952: # past year
                    break
                writer.writerow(commentData(comment))
            worked += 1
        except:
        	errored += 1
        	continue

print(worked, errored, worked + errored)
# '''