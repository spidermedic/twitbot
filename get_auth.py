import time
import tweepy
import config
import webbrowser
from datetime import datetime


def main():

    get_auth()


def get_auth():

    # User information and scope
    oauth2_user_handler = tweepy.OAuth2UserHandler(
        client_id=config.CLIENT_ID,
        client_secret=config.CLIENT_SECRET,
        redirect_uri=config.URL,
        scope=config.SCOPE[0],
    )

    # See if there is an authorization in place
    try:
        import auth
    except:
        get_new_token(oauth2_user_handler)

    try:
        # Then check if the token is expired or will expire in the next 5 minutes
        auth.expires
        if (time.time() + 300) < auth.expires:

            # Token has not expired
            print(
                f"\nAuth token is valid and expires at {datetime.fromtimestamp(auth.expires).strftime('%b %d, %H:%m')}"
            )
            return auth.access_token

        else:
            # Token is expired. Get a new token using the refresh.token method
            new_token = oauth2_user_handler.refresh_token(
                token_url="https://api.twitter.com/2/oauth2/token",
                client=config.CLIENT_ID,
                refresh_token=auth.refresh_token,
            )
            print(f"\nNew Token = {new_token}")

            # write the new token information
            save_token(new_token)

            # return the new token
            return new_token["access_token"]

    # No token found. Authorize the app and get a token.
    except:
        get_new_token(oauth2_user_handler)


def get_new_token(oauth2_user_handler):

    webbrowser.open_new(oauth2_user_handler.get_authorization_url())
    authorization_response = input("Paste Return URL Here: ")
    print()

    access_token = oauth2_user_handler.fetch_token(authorization_response)
    print(access_token)
    print()

    save_token(access_token)

    return access_token["access_token"]


def save_token(token):

    try:
        with open("auth.py", "w") as f:
            f.write(
                f"""access_token = "{token['access_token']}"\nrefresh_token = "{token['refresh_token']}"\nexpires = {token['expires_at']}"""
            )
    except:
        print("Could not update auth.py")


if __name__ == "__main__":
    main()
