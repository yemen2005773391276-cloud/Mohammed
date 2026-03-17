from flask import Flask, render_template, request
from ntscraper import Nitter

app = Flask(__name__)

def get_twitter_data(username):
    # تنظيف اسم المستخدم من أي مسافات أو علامة @
    username = username.strip().replace('@', '')
    scraper = Nitter(log_level=1)
    
    try:
        # محاولة جلب بيانات الملف الشخصي
        target_user = scraper.get_profile_info(username)
        
        if target_user:
            return {
                "success": True,
                "name": target_user.get('name', username),
                "username": username,
                "followers": target_user.get('stats', {}).get('followers', '0'),
                "following": target_user.get('stats', {}).get('following', '0'),
                "bio": target_user.get('bio', 'لا يوجد وصف حالياً')
            }
    except Exception as e:
        print(f"Error fetching data: {e}")
        
    return {"success": False, "error": "تعذر جلب البيانات، قد يكون الحساب خاصاً أو الخادم مشغولاً."}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    user_input = request.form.get('user_id')
    if not user_input:
        return render_template('index.html', error="يرجى إدخال اسم المستخدم أولاً")
        
    result = get_twitter_data(user_input)
    if result["success"]:
        return render_template('index.html', data=result)
    return render_template('index.html', error=result["error"])

if __name__ == "__main__":
    app.run(debug=True)
