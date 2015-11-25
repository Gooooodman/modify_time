# coding:utf-8
from markdown import markdown
# 作为合法的标签库，模块需要包含一个名为register的模块级变量。
# 这个变量是template.Library的实例，是所有注册标签和过滤器的数据结构。
#  所以，请在你的模块的顶部插入如下语句：
from django import template
register = template.Library()
# 以上语句
@register.filter(name="my_markdown")
def my_markdown(value):
    return markdown(value)