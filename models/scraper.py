from newspaper import Article, Config

class ArticleScraper:
    @staticmethod
    def get_full_text(url):
        try:

            user_config = Config()

            user_config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'

            user_config.request_timeout = 15

            scraper = Article(url, config=user_config)
            scraper.download()
            scraper.parse()
            return {
                "title": scraper.title,
                "text": scraper.text
            }
        except Exception as e:
            print(f"Error while scrap data from {url}: {e}")
            return None