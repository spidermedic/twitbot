from logging import raiseExceptions
from get_auth import get_auth
import tweepy
import sys


def main():

    if len(sys.argv) > 1:
        block_em(sys.argv[1])

    else:
        block_list = []
        block_em(block_list)


def block_em(block_list):

    # Create the client with rate-limiting enabled
    client = tweepy.Client(
        get_auth(),
        wait_on_rate_limit=True,
    )

    for user in block_list:
        try:
            client.block(user, user_auth=False).data["blocking"] == True
            print(f"{user} was successfully blocked")
        except:
            print(f"Error: {user} was not blocked")


if __name__ == "__main__":
    main()
