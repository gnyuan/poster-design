from django.db import models
from utils.models import CoreModel


class Templ(CoreModel):
    cover = models.CharField(null=True, max_length=256, verbose_name="封面", help_text="封面")
    url = models.TextField(null=True, verbose_name="模板地址", help_text="模板地址")
    type = models.IntegerField(null=True, default=0, verbose_name="模板类型", help_text="模板类型: 1模板2素材3文字4图片")
    title = models.CharField(null=True, max_length=64, verbose_name="模板名称", help_text="模板名称")
    name = models.CharField(null=True, max_length=64, verbose_name="模板名称", help_text="模板名称")
    search = models.CharField(null=True, max_length=64, verbose_name="模板名称", help_text="模板名称")
    data = models.TextField(null=True, verbose_name="模板数据", help_text="模板数据")
    content = models.TextField(null=True, verbose_name="模板内容", help_text="模板内容")
    width = models.IntegerField(null=True, verbose_name="宽度", help_text="宽度")
    height = models.IntegerField(null=True, verbose_name="高度", help_text="高度")
    state = models.IntegerField(null=True, default=1, verbose_name="是否启用", help_text="是否启用: 0-未启用, 1-启用")
    category = models.IntegerField(null=True, default=0, verbose_name="分类", help_text="分类: ")
    resource = models.TextField(null=True, verbose_name="资源", help_text="资源")
    tag = models.TextField(null=True, verbose_name="标签", help_text="标签")

    cate = models.ForeignKey(to='Cate', verbose_name='所属类别', on_delete=models.SET_NULL, db_constraint=False,
                             null=True,
                             blank=True, help_text="所属类别")

    class Meta:
        db_table = "templ"
        verbose_name = '模板'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)

class Cate(CoreModel): # categoory table
    name = models.CharField(null=True, max_length=64, verbose_name="分类名称", help_text="分类名称")
    type = models.IntegerField(null=True, default=0, verbose_name="分类类型", help_text="分类类型: 1模板2素材3文字4图片")
    pid = models.ForeignKey(to="Cate", on_delete=models.PROTECT, default=None, verbose_name="上级部门",
                               db_constraint=False, null=True, blank=True, help_text="上级部门")
    class Meta:
        db_table = "cate"
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)
        indexes = [
            models.Index(fields=['name'])
        ]

class Image(CoreModel):
    key = models.CharField(null=True, max_length=64, verbose_name="图片key", help_text="图片key")
    thumb = models.TextField(null=True, verbose_name="缩略图", help_text="缩略图")
    url = models.TextField(null=True, verbose_name="图片url", help_text="图片url")
    path = models.CharField(null=True, max_length=256, verbose_name="图片路径", help_text="图片路径")
    width = models.IntegerField(null=True, verbose_name="宽度", help_text="宽度")
    height = models.IntegerField(null=True, verbose_name="高度", help_text="高度")
    category = models.IntegerField(null=True, default=0, verbose_name="分类", help_text="分类: ")
    state = models.IntegerField(null=True, default=1, verbose_name="是否启用", help_text="是否启用: 0-未启用, 1-启用")
    search = models.CharField(null=True, max_length=64, verbose_name="图片名称", help_text="图片名称")
    original = models.CharField(null=True, max_length=64, verbose_name="原始图片", help_text="原始图片")
    author = models.CharField(null=True, max_length=64, verbose_name="作者", help_text="作者")
    color = models.CharField(null=True, max_length=64, verbose_name="颜色", help_text="颜色")
    description = models.TextField(null=True, verbose_name="描述", help_text="描述")

    cate = models.ForeignKey(to='Cate', verbose_name='所属类别', on_delete=models.SET_NULL, db_constraint=False,
                             null=True,
                             blank=True, help_text="所属类别")

    class Meta:
        db_table = "image"
        verbose_name = '图片'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)



class UImage(CoreModel):
    cover = models.CharField(null=True, max_length=256, verbose_name="封面", help_text="封面")
    data = models.TextField(null=True, verbose_name="模板数据", help_text="模板数据")
    height = models.IntegerField(null=True, verbose_name="高度", help_text="高度")
    width = models.IntegerField(null=True, verbose_name="宽度", help_text="宽度")
    url = models.TextField(null=True, verbose_name="图片url", help_text="图片url")
    username = models.CharField(max_length=32, verbose_name="登录用户名", null=True, blank=True, help_text="登录用户名")
    category = models.IntegerField(null=True, default=0, verbose_name="分类", help_text="分类: ")

    class Meta:
        db_table = "uimage"
        verbose_name = '用户图片'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)

class UPoster(CoreModel):
    title = models.CharField(null=True, max_length=64, verbose_name="图片名称", help_text="图片名称")
    height = models.IntegerField(null=True, verbose_name="高度", help_text="高度")
    width = models.IntegerField(null=True, verbose_name="宽度", help_text="宽度")
    url = models.TextField(null=True, verbose_name="图片url", help_text="图片url")
    username = models.CharField(max_length=32, verbose_name="登录用户名", null=True, blank=True, help_text="登录用户名")
    category = models.IntegerField(null=True, default=0, verbose_name="分类", help_text="分类: ")

    class Meta:
        db_table = "uposter"
        verbose_name = '用户作品'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)

class Material(CoreModel):
    title = models.CharField(null=True, max_length=64, verbose_name="图片名称", help_text="图片名称")
    width = models.IntegerField(null=True, verbose_name="宽度", help_text="宽度")
    height = models.IntegerField(null=True, verbose_name="高度", help_text="高度")
    original = models.CharField(null=True, max_length=64, verbose_name="原始图片", help_text="原始图片")
    category = models.IntegerField(null=True, default=0, verbose_name="分类", help_text="分类: ")
    type = models.CharField(null=True, max_length=64, verbose_name="图片类型", help_text="图片类型")
    model = models.TextField(null=True, verbose_name="图片model", help_text="图片model")
    thumb = models.TextField(null=True, verbose_name="缩略图", help_text="缩略图")
    url = models.TextField(null=True, verbose_name="图片url", help_text="图片url")
    state = models.IntegerField(null=True, default=1, verbose_name="是否启用", help_text="是否启用: 0-未启用, 1-启用")

    cate = models.ForeignKey(to='Cate', verbose_name='所属类别', on_delete=models.SET_NULL, db_constraint=False,
                             null=True,
                             blank=True, help_text="所属类别")

    class Meta:
        db_table = "material"
        verbose_name = '图片'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)

class Font(CoreModel):
    alias = models.CharField(null=True, max_length=64, verbose_name="字体alias", help_text="字体alias")
    font_family = models.CharField(null=True, max_length=64, verbose_name="字体family", help_text="字体family")
    lang = models.CharField(null=True, max_length=64, verbose_name="字体语言", help_text="字体语言")
    oid = models.IntegerField(null=True, verbose_name="oid", help_text="oid")
    preview = models.TextField(null=True, verbose_name="字体预览", help_text="字体预览")
    size = models.IntegerField(null=True, verbose_name="字体大小", help_text="字体大小")
    ttf = models.TextField(null=True, verbose_name="字体ttf", help_text="字体ttf")
    value = models.CharField(null=True, max_length=64, verbose_name="字体value", help_text="字体value")
    version = models.CharField(null=True, max_length=64, verbose_name="字体version", help_text="字体version")
    woff = models.TextField(null=True, verbose_name="字体woff", help_text="字体woff")
    woff_size = models.IntegerField(null=True, verbose_name="字体大小", help_text="字体大小")

    class Meta:
        db_table = "font"
        verbose_name = '字体'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)
