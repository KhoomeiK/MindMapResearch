import praw
import csv
import time
from os import listdir

# use users who post on sad subreddits' text to classify as depressed
subs, users = set(), set()

subs.add('depression')
# with open('subreddits.txt', 'r') as txt:
#     for line in txt:
#         if line[0] != '*' and 'r/' in line:
#             sub = line.split('r/')[1].strip()
#             subs.add(sub)
print(subs)

r = praw.Reddit(username = "WebsterBot",
    password = "G*c-+#6d^8V%$_6=",
    client_id = "_fRmFVzOM5jYHQ",
    client_secret = "o_jPN2Mou9UbAJzN5I3zybCaKjo",
    user_agent = "actualsnek wtwbot test 0.0")

def commentData(c):
    return (c.subreddit.display_name, c.id, c.parent_id, c.created_utc, c.body)

for sub in subs:
    print(sub)
    for p in r.subreddit(sub).top(time_filter='day'): # CHANGE: year?
        if p.score > 100 and p.author:
            users.add(p.author)
            for c in p.comments:
                if isinstance(c, praw.models.Comment) and c.author and c.score > 0:
                    users.add(c.author)
                    if len(c.replies) > 0:
                        for child in c.replies.list():
                            if isinstance(child, praw.models.Comment) and child.author and child.score > 0:
                                users.add(child.author)
    # print(users) # users who've commented on sub in past day

# users = [praw.models.Redditor(reddit=r, name='imhereforthepuppies')] # CHANGE: remove

print(users)

for user in users:
    if '%s.csv' % user.name not in listdir('./users'):
        print(user)
        count = {}
        saved = []
        comments = user.comments.new()
        for comment in comments:
            print(comment.subreddit.display_name, comment.created_utc)
            saved.append(comment)
            if time.time() - comment.created_utc > 2592000: # past 30 days
                break
            if comment.subreddit.display_name in subs:
                if comment.subreddit.display_name in count:
                    count[comment.subreddit.display_name] = count[comment.subreddit.display_name] + 1  
                else: 
                    count[comment.subreddit.display_name] = 1
        print(count)
        if any(True if ct >= 3 else False for ct in count.values()):
            writer = csv.writer(open('./users/%s.csv' % user.name, 'w'))
            writer.writerow(('subreddit', 'self ID', 'parent ID', 'time', 'text'))
            for comment in saved:
                # print(commentData(comment))
                writer.writerow(commentData(comment))