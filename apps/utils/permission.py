from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    对象级权限，仅允许对象的所有者编辑它。
    假设模型实例具有 `owner` 属性。
    """

    def has_object_permission(self, request, view, obj):
        # 任何请求都允许读取权限，
        # 所以我们总是允许 GET，HEAD 或 OPTIONS 请求。
        if request.method in permissions.SAFE_METHODS:
            return True

        # obj 就是你的model实例
        # 实例必须具有名为 `owner` 的属性,没有就改成对应字段
        # 当前是根据 UserFav 表的 外键user字段判断
        return obj.user == request.user
