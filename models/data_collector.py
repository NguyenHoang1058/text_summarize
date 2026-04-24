import time
import csv
import os
from models.news_api import NewsFetcher
from models.scraper import ArticleScraper

def thu_thap_va_luu_csv():
    API_KEY = 'c4514401725448a88b62f613940ebe0c'
    news_client = NewsFetcher(api_key=API_KEY)
    
    # Danh sách chủ đề cần quét
    CATEGORIES = ['general', 'technology', 'sports', 'business', 'entertainment', 'health', 'science'] 
    FILE_CSV = 'du_lieu_100k.csv'

    print("\n[HỆ THỐNG] BẮT ĐẦU CHIẾN DỊCH CÀO DỮ LIỆU...")
    
    # Tạo file và viết Header nếu chưa có
    if not os.path.exists(FILE_CSV):
        with open(FILE_CSV, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['title', 'content', 'url'])

    tong_so_bai = 0
    
    for category in CATEGORIES:
        print(f"\n--- Đang quét API chủ đề: {category} ---")
        articles = news_client.fetch_top_headlines(category=category)
        
        for article in articles:
            url = article.get('url')
            if not url: 
                continue
                
            article_data = ArticleScraper.get_full_text(url)
            
            # Chỉ lưu những bài có độ dài nội dung > 200 ký tự
            if article_data and article_data['text'] and len(article_data['text']) > 200:
                with open(FILE_CSV, mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([article_data['title'], article_data['text'], url])
                
                tong_so_bai += 1
                print(f"  [+] Đã lưu bài {tong_so_bai}: {article_data['title'][:40]}...")
            
            time.sleep(1) # Nghỉ để không bị server chặn
            
    print(f"\n[HỆ THỐNG] HOÀN TẤT LƯỢT GOM DATA! Đã thêm: {tong_so_bai} bài.")