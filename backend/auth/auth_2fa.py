import pyotp
import qrcode
import io
import base64

def generate_2fa_secret(username):
    secret=pyotp.random_base32()

    uri=pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name="CHAITRA")

    qr=qrcode.make(uri)

    buffer=io.BytesIO()
    qr.save(buffer, format="PNG")
    qr_image=base64.b64encode(buffer.getvalue()).decode()
    return secret, qr_image

def verify_otp(secret, otp):
    totp=pyotp.TOTP(secret)
    return totp.verify(otp)