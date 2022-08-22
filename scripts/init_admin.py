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

# models.Administrator.objects.create(username='admin', password=md5('admin'), mobile='13900001234')
