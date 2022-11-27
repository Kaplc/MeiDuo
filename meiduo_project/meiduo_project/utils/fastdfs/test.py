
from fdfs_client.client import Fdfs_client

client = Fdfs_client(r'G:\project\MeiDuo\meiduo_project\meiduo_project\utils\fastdfs\client.conf')
ret = client.upload_by_filename(r'G:\project\MeiDuo\meiduo_project\meiduo_project\static\favicon.ico')
print(ret)
