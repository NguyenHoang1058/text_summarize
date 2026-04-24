from flask import Flask, render_template, redirect, url_for, flash, request
import threading
import os
import csv

from models.news_api import NewsFetcher
from models.scraper import ArticleScraper
from models.ai_summarizer import TextSummarizer

# Nhập các hàm xử lý từ thư mục models
from models.data_collector import thu_thap_va_luu_csv
from models.model_trainer import huan_luyen_ai

app = Flask(__name__)
# Secret key bắt buộc phải có để dùng tính năng thông báo flash của Flask
API_KEY = 'c4514401725448a88b62f613940ebe0c'
news_client = NewsFetcher(api_key=API_KEY)
ai_bot = TextSummarizer(model_path="./my_summary_model")


app.secret_key = "khoa_bi_mat_cho_do_an" 

@app.route('/')
def index():
    # Chỉ hiển thị bảng điều khiển
    return render_template('index.html', result=None)

@app.route('/get-news', methods=['GET'])
def get_todays_news():

    category = request.args.get('category', 'general')
    articles = news_client.fetch_top_headlines(category=category)[:3]
    
    results = []
    for art in articles:
        url = art.get('url')
        if not url or art.get('title') == '[Removed]': continue
        
        data = ArticleScraper.get_full_text(url)
        if data and data['text']:
            summary_text = ai_bot.summarize(data['text'])
            results.append({
                'title': art.get('title'),
                'summary': summary_text,
                'url': url,
                'image': art.get('urlToImage'),
                'time': art.get('publishedAt')[:10] if art.get('publishedAt') else "N/A"
            })
            
    return render_template('summary.html', results=results, category=category)      

@app.route('/run-collector')
def run_collector():
    # Khởi tạo một luồng chạy ngầm để web không bị đơ
    thread = threading.Thread(target=thu_thap_va_luu_csv)
    thread.start()
    
    # Gửi thông báo về lại giao diện web
    flash("Đã kích hoạt tiến trình GOM DỮ LIỆU. Vui lòng mở Terminal để xem tiến độ!", "info")
    return redirect(url_for('index'))

@app.route('/run-trainer')
def run_trainer():
    # Khởi tạo luồng chạy ngầm cho việc train
    thread = threading.Thread(target=huan_luyen_ai)
    thread.start()
    
    flash("Đã kích hoạt tiến trình HUẤN LUYỆN AI. Vui lòng mở Terminal để xem chi tiết!", "success")
    return redirect(url_for('index'))

@app.route('/preview-data')
def preview_data():
    file_path = 'du_lieu_100k.csv'
    data = []

    # Kiểm tra tồn tại data
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None) # Lấy dòng tiêu đề

            # Lấy 50 dòng data đầu tiên
            for i, row in enumerate(reader):
                if i >= 50:
                    break
                data.append(row)
    else:
        header = None
        flash("Chưa có file dữ liệu. Vui lòng gom data trước !!!", "warning")
        return redirect(url_for('index'))
    
    # Chuyển dữ liệu sang trang giao diện mới
    return render_template('data_preview.html', header=header, data=data)

if __name__ == '__main__':
    app.run(debug=True)