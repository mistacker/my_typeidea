from django.contrib import admin


class BaseOwnerAdmin(object):
    """
    1. 用来自定补充文章，分类，标签，侧边栏，友链这些Model的owner字段
    2. 用来针对queryset过滤当前用户数据
    """
    exclude = ('owner',)

    def save_models(self):
        self.new_obj.owner = self.request.user
        return super(BaseOwnerAdmin, self).save_models()

    def get_list_queryset(self):
        qs = super(BaseOwnerAdmin, self).get_list_queryset()
        return qs.filter(owner=self.request.user)
