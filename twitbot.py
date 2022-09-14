import sys
import tweepy
import config
from get_auth import get_auth
from datetime import datetime, timedelta


def main():

    if len(sys.argv) > 1 and sys.argv[1] in ["u", "f", "t", "l", "a"]:

        client = tweepy.Client(get_auth(), wait_on_rate_limit=True)

        match sys.argv[1]:
            case "u":
                purge_no_followback(client)
            case "f":
                follow_back(client)
            case "t":
                purge_old_tweets(client)
            case "l":
                unlike_old_tweets(client)
            case "a":
                follow_back(client)
                purge_no_followback(client)
                purge_old_tweets(client)
                unlike_old_tweets(client)

        print()

    else:
        print()
        show_usage()


def show_usage():
    print("\nUsage: python twitbot.py [f|l|t|u]")
    print("    f: Follow users who follow you")
    print("    l: Unlike tweets over XX days")
    print("    u: Unfollow users who haven't followed back")
    print("    t: Purge tweets older than XX days\n")
    logger("Error: Invalid command line parameters.")
    sys.exit(1)


def logger(log_data):
    try:
        with open("twitbot.log", "a+") as f:
            print(log_data)
            f.write(f"{datetime.now().strftime('%m-%d-%Y, %H:%m')}: {log_data}\n")
    except:
        print("Unable to write to log file")


def unlike_old_tweets(client):

    # Unlike tweets that are older than XX days
    liked = tweepy.Paginator(
        client.get_liked_tweets,
        config.USER_ID,
        tweet_fields="created_at",
        max_results=100,
    ).flatten(limit=1000)

    total = 0
    unliked = 0

    for like in liked:
        total += 1
        if (datetime.now().date() - like.created_at.date()) > timedelta(days=21):
            print(like.created_at.date(), like.id)
            client.unlike(like.id, user_auth=False)
            unliked += 1

    logger(f"Unlike Old Tweets:   {total} liked tweets found. {unliked} tweets unliked")


def purge_no_followback(client):
    # Get rid of follows who haven't followed back.
    good = 0
    bad = 0

    followers = get_followers(client)
    following = get_following(client)

    for s in following:
        if s not in followers:
            print(f"{s[0]} id={s[1]}")
            try:
                client.unfollow_user(s[1], user_auth=False)
                good += 1
            except:
                bad += 1

    # log summary
    logger(
        f"Purge Non-Followers: {good + bad} non-following accounts found. {good} unfollowed. {bad} errors."
    )


def purge_old_tweets(client):
    # Get rid of tweets older than specified in "days_to_keep"

    today = datetime.now()
    days_to_keep = 5
    total = 0
    good = 0
    bad = 0

    # Grab 1000 tweets
    tweet_list = tweepy.Paginator(
        client.get_users_tweets,
        config.USER_ID,
        tweet_fields="created_at",
        max_results=100,
    ).flatten(limit=1000)

    # Get rid of the old tweets
    for tweet in tweet_list:
        total += 1
        if (today.date() - tweet.created_at.date()) > timedelta(days=days_to_keep):

            print(tweet.created_at.date(), tweet.id, end="")
            try:
                client.delete_tweet(tweet.id, user_auth=False)
                print(" - Tweet Deleted")
                good += 1
            except:
                print(" - Delete Failed")
                bad += 1

    # log summary
    logger(
        f"Purge Old Tweets:    {total} total tweets found. {good} deleted. {bad} errors."
    )


def follow_back(client):
    total = 0
    good = 0
    bad = 0

    followers = get_followers(client)
    following = get_following(client)

    for s in followers:
        if s not in following:
            total += 1
            print(f"{s[0]} id={s[1]}")
            try:
                client.follow_user(s[1], user_auth=False)
                good += 1
            except:
                bad += 1

    # log summary
    logger(
        f"Follow Back:         {total} new followers. {good} followed. {bad} errors."
    )


def get_following(client):
    # Returns a list of people currently being followed, up to 500

    following = []

    for f in tweepy.Paginator(
        client.get_users_following, config.USER_ID, max_results=500
    ):
        for follower in f.data:
            following.append((follower.username, follower.id))

    return following


def get_followers(client):
    # Returns a list of people who are following me, up to 500

    # PROTECTED_FOLLOWS are those you want to keep, but don't expect them to follow back
    followers = config.PROTECTED_FOLLOWS

    for f in tweepy.Paginator(
        client.get_users_followers, config.USER_ID, max_results=500
    ):
        for follower in f.data:
            followers.append((follower.username, follower.id))

    return followers


if __name__ == "__main__":
    main()
