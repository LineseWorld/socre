import requests
from PIL import Image
from io import BytesIO

def download_picture(url,file_name):
    # 图片的URL
    # print("name:{} url: {}".format(file_name,url))
    # 使用requests库获取图片内容
    response = requests.get(url)
    response.raise_for_status()  # 如果请求失败，这里会抛出异常

    # 使用BytesIO来创建一个文件对象
    image_bytes = BytesIO(response.content)

    # 使用Pillow打开这个文件对象
    image = Image.open(image_bytes)

    # 保存图片到本地
    image.save(file_name)