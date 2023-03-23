
from fdfs_client.client import Fdfs_client, get_tracker_conf

track_config = get_tracker_conf('/home/kaplc/PycharmProjects/MeiDuo/meiduo_project/meiduo_project/utils/fastdfs/client.conf')

client = Fdfs_client(track_config)
ret = client.upload_by_filename('/home/kaplc/PycharmProjects/MeiDuo/meiduo_project/meiduo_project/static/favicon.ico')
print(ret)