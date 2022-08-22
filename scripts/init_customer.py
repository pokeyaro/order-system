# 依赖django运行，启动环境
import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

# 读取配置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'order.settings')
# 伪造让django启动
django.setup()


from web import models
from utils.encrypt import md5

# 创建级别
# level_obj = models.Level.objects.create(title="VIP", percent=90)
# models.Customer.objects.create(username='zhangsan', password=md5('zhangsan'), mobile='13312345678', level=level_obj, creator_id=1)
# models.Customer.objects.create(username='xiaoming', password=md5('xiaoming'), mobile='18903456785', level_id=1, creator_id=1)
