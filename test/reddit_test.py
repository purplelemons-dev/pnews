import requests
import requests.auth

# Set your Reddit application credentials
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
username = "YOUR_REDDIT_USERNAME"
password = "YOUR_REDDIT_PASSWORD"

# Set user agent
user_agent = "YOUR_USER_AGENT"


def get_reddit_token(client_id, client_secret, username, password, user_agent):
    client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    post_data = {"grant_type": "password", "username": username, "password": password}
    headers = {"User-Agent": user_agent}
    response = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=client_auth,
        data=post_data,
        headers=headers,
    )
    return response.json()["access_token"]


# def get_newest_posts(token, subreddit, limit=100):
#     headers = {"Authorization": f"bearer {token}", "User-Agent": user_agent}
#     params = {'limit': limit}
#     response = requests.get(f"https://oauth.reddit.com/r/{subreddit}/new",
#                             headers=headers, params=params)
#     return response.json()
#
# # Get the access token
# token = get_reddit_token(client_id, client_secret, username, password, user_agent)
#
# # Fetch the newest posts from r/all
# newest_posts = get_newest_posts(token, 'all')
#
# # Process and print the post details
# for post in newest_posts['data']['children']:
#     title = post['data']['title']
#     score = post['data']['score']
#     url = post['data']['url']
#     print(f"Title: {title}, Score: {score}, URL: {url}")
