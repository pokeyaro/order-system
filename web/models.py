from django.db import models
from django.core.validators import RegexValidator


class ActiveBaseModel(models.Model):
    active = models.SmallIntegerField(verbose_name="状态", default=1, choices=((1, "激活"), (0, "删除")))

    class Meta:
        abstract = True


class Administrator(ActiveBaseModel):
    """ 管理员表 """
    username = models.CharField(verbose_name="用户名", max_length=32, db_index=True)
    password = models.CharField(verbose_name="密码", max_length=64)
    mobile = models.CharField(verbose_name="手机号", max_length=11, db_index=True)
    create_date = models.DateTimeField(verbose_name="创建日期", auto_now_add=True)


class Level(ActiveBaseModel):
    """ 级别表 """
    title = models.CharField(verbose_name="标题", max_length=32)
    percent = models.IntegerField(verbose_name="折扣", help_text="请填入0-100整数，表示百分比，如：50，表示50%")

    def __str__(self):
        return self.title


class Customer(ActiveBaseModel):
    """ 客户表 """
    username = models.CharField(verbose_name="用户名", max_length=32, db_index=True)
    password = models.CharField(verbose_name="密码", max_length=64)
    mobile = models.CharField(verbose_name="手机号", max_length=11, db_index=True,
                              validators=[RegexValidator(r'^1[3-8]\d{9}$', '手机号格式不正确')])
    balance = models.DecimalField(verbose_name="账户余额", default=0, max_digits=10, decimal_places=2)
    # 关联数据时，会将它作为条件，去自动进行筛选 limit_choices_to={'active': 1, 'id__gt': 4}
    level = models.ForeignKey(verbose_name="级别", to="Level", on_delete=models.CASCADE)
    create_datetime = models.DateTimeField(verbose_name="创建日期", auto_now_add=True)
    creator = models.ForeignKey(verbose_name="创建者", to="Administrator", on_delete=models.CASCADE)


class PricePolicy(models.Model):
    """ 价格策略（原价，后续可以根据用户级别不同做不同的折扣） """
    count = models.IntegerField(verbose_name="数量")
    price = models.DecimalField(verbose_name="价格", default=0, max_digits=10, decimal_places=2)


class Order(ActiveBaseModel):
    """ 订单表 """
    status_choices = (
        (1, "待执行"),
        (2, "正在执行"),
        (3, "已完成"),
        (4, "失败"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)
    oid = models.CharField(verbose_name="订单号", max_length=64, unique=True)
    url = models.URLField(verbose_name="视频地址", db_index=True)
    count = models.IntegerField(verbose_name="数量")
    price = models.DecimalField(verbose_name="价格", default=0, max_digits=10, decimal_places=2)
    real_price = models.DecimalField(verbose_name="实付价格", default=0, max_digits=10, decimal_places=2)
    old_view_count = models.CharField(verbose_name="原播放量", max_length=32, default="0")
    create_datetime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    customer = models.ForeignKey(verbose_name="客户", to="Customer", on_delete=models.CASCADE)
    memo = models.TextField(verbose_name="备注", null=True, blank=True)


class TransactionRecord(ActiveBaseModel):
    """ 交易记录 """
    charge_type_class_mapping = {
        1: "success",
        2: "danger",
        3: "default",
        4: "info",
        5: "primary",
    }
    charge_type_choices = (
        (1, "充值"),
        (2, "扣款"),
        (3, "创建订单"),
        (4, "删除订单"),
        (5, "撤销订单"),
    )
    charge_type = models.SmallIntegerField(verbose_name="类型", choices=charge_type_choices)
    customer = models.ForeignKey(verbose_name="客户", to="Customer", on_delete=models.CASCADE)
    amount = models.DecimalField(verbose_name="金额", default=0, max_digits=10, decimal_places=2)
    creator = models.ForeignKey(verbose_name="管理员", to="Administrator", on_delete=models.CASCADE, null=True,
                                blank=True)
    order_oid = models.CharField(verbose_name="订单号", max_length=64, null=True, blank=True, db_index=True)
    create_datetime = models.DateTimeField(verbose_name="交易时间", auto_now_add=True)
    memo = models.TextField(verbose_name="备注", null=True, blank=True)
