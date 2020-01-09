import praw

r = praw.Reddit(username="WebsterBot",
                password="G*c-+#6d^8V%$_6=",
                client_id="_fRmFVzOM5jYHQ",
                client_secret="o_jPN2Mou9UbAJzN5I3zybCaKjo",
                user_agent="actualsnek wtwbot test 0.0")

for p in r.subreddit("depression").top(time_filter='week'):
    if p.score > 1000:
        tc = []
        for c in p.comments:
        	tc.append(c.body)
        print(tc)