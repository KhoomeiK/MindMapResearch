import praw
import csv
from os import listdir

# use users who post on sad subreddits' text to classify as depressed
subs = set()

with open('subreddits.txt', 'r') as txt:
    for line in txt:
        if line[0] != '*' and 'r/' in line: # AND NOT IN ./data/
            sub = line.split('r/')[1].strip()
            if '%s.csv' % sub not in listdir('./data'):
                subs.add(sub)
print(subs)

r = praw.Reddit(username = "WebsterBot",
    password = "G*c-+#6d^8V%$_6=",
    client_id = "_fRmFVzOM5jYHQ",
    client_secret = "o_jPN2Mou9UbAJzN5I3zybCaKjo",
    user_agent = "actualsnek wtwbot test 0.0")

def commentData(c):
    return (c.author.name, c.id, c.parent_id, c.body)

for sub in subs:
    print(sub)
    with open('./data/%s.csv' % sub, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(('author', 'self ID', 'parent ID', 'text'))
        for p in r.subreddit(sub).top(time_filter='week'): # year?
            if p.score > 100 and p.author:
                writer.writerow((p.author.name, p.id, 'top_level', p.selftext))
                tc = []
                for c in p.comments:
                    if isinstance(c, praw.models.Comment) and c.author and c.score > 0:
                        tc.append(commentData(c))
                        if len(c.replies) > 0:
                            for child in c.replies.list():
                                if isinstance(child, praw.models.Comment) and child.author and child.score > 0:
                                    tc.append(commentData(child))
                for c in tc:
                    # print('writing', c)
                    writer.writerow(c)