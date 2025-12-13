import requests


class Post:
    def __init__(self):
        self.blog_url = "https://api.npoint.io/c790b4d5cab58020d391"
        self.response = requests.get(self.blog_url)
        self.all_posts = self.response.json()

    def get_all_posts(self):
        return self.all_posts




