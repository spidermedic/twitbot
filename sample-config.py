# Fill in all of the information below and rename this file to config.py

# Twitter developer keys
API_KEY = "YOUR API KEY"
API_KEY_SECRET = "YOUR API SECRET"
BEARER_TOKEN = "YOUR BEARER TOKEN"
ACCESS_TOKEN = "YOUR ACCESS TOKEN"
ACCESS_TOKEN_SECRET = "YOUR ACCESS TOKEN SECRET"
CLIENT_ID = "YOUR CLIENT ID"
CLIENT_SECRET = "YOUR CLIENT SECRET"

# Your actuall twitter user ID
USER_ID = "1234567890000000000"
# Redirect URL
URL = "https://example.com"

# Removing any of the scope items will break the program.
SCOPE = (
    [
        "tweet.read",
        "tweet.write",
        "block.read",
        "block.write",
        "users.read",
        "follows.read",
        "follows.write",
        "mute.read",
        "mute.write",
        "like.read",
        "like.write",
        "offline.access",
    ],
)

# This list containts accounts that will never be purged. The two accounts listed are samples and can be changed or deleted.
# Each line is a tuple using the format: (account_name, account_id)
PROTECTED_FOLLOWS = [
    ("BetteMidler", 139823781),
    ("SteveMartinToGo", 14824849),
]
