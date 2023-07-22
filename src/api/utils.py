import datetime
from django.utils import timezone
import pytz

def get_new_datetime():
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')  # Tạo đối tượng múi giờ Việt Nam
    vn_time = datetime.datetime.now(vn_tz)  # Chuyển đổi thời gian hiện tại sang múi giờ Việt Nam
    vn_now = vn_time.strftime('%Y-%m-%d %H:%M:%S')  # Convert sang chuỗi theo định dạng '%Y-%m-%d %H:%M:%S'
    return vn_now