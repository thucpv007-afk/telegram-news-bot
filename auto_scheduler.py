# auto_scheduler.py - Phiên bản đã sửa lỗi
import schedule
import time
from datetime import datetime
import requests

class TelegramNotifier:
    """Class gửi thông báo Telegram"""
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
    
    def send_message(self, text, parse_mode='HTML'):
        url = f"{self.base_url}/sendMessage"
        payload = {
            'chat_id': self.chat_id,
            'text': text,
            'parse_mode': parse_mode
        }
        try:
            response = requests.post(url, json=payload)
            return response.json()
        except Exception as e:
            print(f"❌ Lỗi gửi tin: {e}")
            return None

class SimpleNewsAnalyzer:
    """Class phân tích tin tức đơn giản (demo)"""
    
    def get_latest_high_impact_news(self):
        """Lấy tin tức tác động cao (demo - bạn sẽ thay bằng API thật)"""
        # Trong thực tế, bạn sẽ gọi API tin tức ở đây
        current_time = datetime.now().strftime("%H:%M")
        
        # Return demo data với thời gian hiện tại
        return [{
            'title': f'Cập nhật thị trường lúc {current_time}',
            'source': 'Bloomberg',
            'date': datetime.now().strftime('%d/%m/%Y'),
            'impact': 'high',
            'sentiment': 'positive',
            'analysis': 'Thị trường giao dịch ổn định. Các chỉ số chính duy trì xu hướng tích cực.',
            'affected_assets': ['Vàng', 'Chứng khoán', 'BĐS']
        }]
    
    def generate_daily_summary(self):
        """Tạo báo cáo tổng hợp"""
        return {
            'total_news': 156,
            'high_impact': 23,
            'medium_impact': 67,
            'low_impact': 66,
            'gold_score': 72,
            'gold_change': '+3.2%',
            'stocks_score': 45,
            'stocks_change': '-1.8%',
            'realestate_score': 58,
            'realestate_change': '+0.5%',
            'crypto_score': 81,
            'crypto_change': '+5.7%',
            'fed_rate': '5.25-5.50%',
            'vnindex': '1,282 (+1.2%)',
            'usd_index': '105.2 (-0.8%)',
            'gold_price': '$2,750 (+2.1%)',
            'recommendations': '• Vàng: Xu hướng tích cực, có thể tăng vị thế\n• Cổ phiếu: Thận trọng với biến động\n• BĐS: Quan sát thêm tín hiệu'
        }

# ===== CẤU HÌNH =====
BOT_TOKEN = "8465675309:AAE7_NwmS6fccxc5-e0Ojrla7F0Yi7mUrbk"
CHAT_ID = "8385186450"

notifier = TelegramNotifier(BOT_TOKEN, CHAT_ID)
analyzer = SimpleNewsAnalyzer()

# ===== CÁC HÀM SCHEDULED =====

def send_news_update():
    """Gửi cập nhật tin tức (8AM, 1PM, 5PM)"""
    print(f"⏰ {datetime.now().strftime('%H:%M:%S')} - Gửi cập nhật tin tức...")
    
    latest_news = analyzer.get_latest_high_impact_news()
    
    for news in latest_news:
        message = f"""
🔴 <b>TIN TỨC VĨ MÔ</b> 📈

<b>📰 {news['title']}</b>

📅 <i>{news['date']}</i>
🏢 <i>Nguồn: {news['source']}</i>

💡 <b>Phân tích:</b>
{news['analysis']}

📊 <b>Ảnh hưởng đến:</b>
{' • '.join(news['affected_assets'])}
"""
        notifier.send_message(message)
        print("✅ Đã gửi tin tức!")
        time.sleep(2)

def send_daily_summary():
    """Gửi báo cáo tổng hợp (8AM)"""
    print(f"📊 {datetime.now().strftime('%H:%M:%S')} - Gửi báo cáo tổng hợp...")
    
    summary = analyzer.generate_daily_summary()
    
    message = f"""
📊 <b>BÁO CÁO VĨ MÔ HÀNG NGÀY</b>
🗓 {datetime.now().strftime('%d/%m/%Y %H:%M')}

━━━━━━━━━━━━━━━━━━━━

📈 <b>TỔNG QUAN</b>
• Tổng số tin: {summary['total_news']}
• Tác động cao: {summary['high_impact']} 🔴
• Tác động TB: {summary['medium_impact']} 🟡
• Tác động thấp: {summary['low_impact']} 🟢

━━━━━━━━━━━━━━━━━━━━

💰 <b>TÁC ĐỘNG TÀI SẢN</b>

🪙 Vàng: {summary['gold_score']}/100 ({summary['gold_change']})
📊 Chứng khoán: {summary['stocks_score']}/100 ({summary['stocks_change']})
🏢 BĐS: {summary['realestate_score']}/100 ({summary['realestate_change']})
₿ Crypto: {summary['crypto_score']}/100 ({summary['crypto_change']})

━━━━━━━━━━━━━━━━━━━━

🔑 <b>CHỈ SỐ QUAN TRỌNG</b>
• Fed Rate: {summary['fed_rate']}
• VN-Index: {summary['vnindex']}
• USD Index: {summary['usd_index']}
• Giá vàng: {summary['gold_price']}

━━━━━━━━━━━━━━━━━━━━

💡 <b>KHUYẾN NGHỊ</b>
{summary['recommendations']}
"""
    notifier.send_message(message)
    print("✅ Đã gửi báo cáo!")

def send_market_open_alert():
    """Cảnh báo trước giờ mở cửa thị trường (8:45AM)"""
    print(f"🔔 {datetime.now().strftime('%H:%M:%S')} - Gửi cảnh báo mở cửa...")
    
    message = "🔔 <b>Thị trường sắp mở cửa!</b>\n\nKiểm tra các tin tức quan trọng qua đêm."
    notifier.send_message(message)
    print("✅ Đã gửi cảnh báo!")

def send_test_message():
    """Gửi tin test ngay khi khởi động"""
    message = f"""
🤖 <b>BOT ĐÃ KHỞI ĐỘNG!</b>

⏰ Thời gian: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

📅 <b>Lịch trình cập nhật:</b>
• 08:00 - Báo cáo buổi sáng + Tin tức
• 08:45 - Cảnh báo mở cửa thị trường
• 13:00 - Tin tức buổi trưa
• 17:00 - Tin tức cuối ngày

Bot đang hoạt động và theo dõi tin tức! 🚀
"""
    notifier.send_message(message)
    print("✅ Đã gửi tin khởi động!")

# ===== LÊN LỊCH =====

# 8:00 AM - Báo cáo tổng hợp + Tin tức buổi sáng
schedule.every().day.at("08:00").do(send_daily_summary)
schedule.every().day.at("08:01").do(send_news_update)  # Delay 1 phút để tránh trùng

# 8:45 AM - Cảnh báo mở cửa thị trường
schedule.every().day.at("08:45").do(send_market_open_alert)

# 1:00 PM (13:00) - Tin tức buổi trưa
schedule.every().day.at("13:00").do(send_news_update)

# 5:00 PM (17:00) - Tin tức cuối ngày
schedule.every().day.at("17:00").do(send_news_update)

# ===== CHẠY BOT =====

if __name__ == "__main__":
    print("=" * 60)
    print("🤖 TELEGRAM NEWS BOT - AUTO SCHEDULER")
    print("=" * 60)
    print(f"⏰ Khởi động lúc: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("-" * 60)
    print("📅 Lịch trình cập nhật:")
    print("   • 08:00 - Báo cáo tổng hợp + Tin tức buổi sáng")
    print("   • 08:45 - Cảnh báo mở cửa thị trường")
    print("   • 13:00 - Tin tức buổi trưa")
    print("   • 17:00 - Tin tức cuối ngày")
    print("-" * 60)
    print("💡 Nhấn Ctrl+C để dừng bot")
    print("=" * 60)
    print()
    
    # Gửi tin test khi khởi động
    send_test_message()
    
    # TEST NGAY CÁC CHỨC NĂNG (Tùy chọn - comment dòng dưới nếu không muốn test)
    print("\n🧪 TEST CÁC CHỨC NĂNG:")
    print("-" * 60)
    send_news_update()  # Test tin tức
    time.sleep(3)
    send_daily_summary()  # Test báo cáo
    time.sleep(3)
    send_market_open_alert()  # Test cảnh báo
    print("-" * 60)
    print("✅ Test hoàn tất! Bot sẽ tự động gửi theo lịch.\n")
    
    # Chạy vòng lặp chính
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Kiểm tra mỗi 60 giây
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("🛑 Bot đã dừng!")
        print(f"⏰ Thời gian dừng: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("=" * 60)
        
        # Gửi tin thông báo dừng
        notifier.send_message("🛑 <b>Bot đã dừng hoạt động</b>")
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        notifier.send_message(f"❌ <b>Bot gặp lỗi:</b>\n{e}")