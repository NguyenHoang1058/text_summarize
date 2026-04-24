import requests

class NewsFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://newsapi.org/v2/top-headlines'

    def fetch_top_headlines(self, category='general', country='us'):
        url = f"{self.base_url}?country={country}&category={category}&apiKey={self.api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status() # check for HTTP errors
            news_data = response.json()
            return news_data.get('articles', [])
        except requests.exceptions.RequestException as e:
            print(f"Error while call API: {e}")
            return []
