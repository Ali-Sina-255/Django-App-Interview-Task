
import pyotp 
from datetime import datetime, timedelta

def send_otp(request):
    totp = pyotp.TOTP(pyotp.random_base32(),interval=60)
    otp = totp.now()
    request.session['otp_secret_key'] = totp.secret
    valid_data = datetime.now() + timedelta(minutes=2)
    request.session['otp_valid_date'] = str(valid_data)
    print(f'your otp code is {otp}')
    return otp
    
