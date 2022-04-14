'''
==============================
test1：生成二维码及查看
==============================
'''
from PIL import Image
import qrcode

qr = qrcode.QRCode(
    version=5,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=4,
    border=4
    )

qr.add_data("因为add_data 函数的限制，我不知道如何在这里换行，我只能接下去写，总的来说我觉得使用网络链接是一个有意思办法。")
qr.make(fit=True)


img = qr.make_image(fill_color="black", back_color="white")
img = img.convert("RGBA")


img.show()   # 显示图片,可以通过save保存