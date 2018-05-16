import praw
import config
import time
import os

def bot_login():
    print("Logging in...")
    login = praw.Reddit(username = config.username,
            password = config.password,
            client_id = config.client_id,
            client_secret = config.client_secret,
            user_agent = config.user_agent)
    print("Logged in!")

    return login    

def run_bot(r, comments_replied_to):
    print("Obtaining comments...")

    for comment in r.subreddit('all').stream.comments():
        if "keikaku" in comment.body and comment.id not in comments_replied_to and comment.author != r.user.me:
            print("String with \"keikaku\" found in comment " + comment.id)
            comment.reply("*Translator's note: Keikaku means plan*")  
            print("Replied to comment " + comment.id)  

            comments_replied_to.append(comment.id)    

            with open("comments_replied_to.txt", "a") as f:
                f.write(comment.id + "\n")
            
            print("Obtaining comments...")
    
    #Sleep for 10s
    time.sleep(10)

def get_saved_comments(): 
    if not os.path.isfile("comments_replied_to.txt"):
        comments_replied_to = []
    else:    
        with open("comments_replied_to.txt", "r") as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
            comments_replied_to = list(filter(None, comments_replied_to))
        
    return comments_replied_to    

keikaku = bot_login()
comments_replied_to = get_saved_comments()

while True:
    run_bot(keikaku, comments_replied_to)