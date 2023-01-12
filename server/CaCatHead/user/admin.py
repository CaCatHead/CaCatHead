from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from CaCatHead.contest.models import Contest
from CaCatHead.post.models import Post
from CaCatHead.problem.models import ProblemRepository
from CaCatHead.user import models


class UserInfoInline(admin.StackedInline):
    model = models.UserInfo
    verbose_name_plural = '用户信息组'
    can_delete = False


class StudentInfoInline(admin.StackedInline):
    model = models.StudentInfo
    verbose_name_plural = '学生信息组'
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = [UserInfoInline, StudentInfoInline]

    actions = (
        'grant_create_contest', 'revoke_create_contest', 'grant_create_post', 'revoke_create_post', 'grant_polygon',
        'revoke_polygon')

    @admin.action(description='授予创建比赛权限')
    def grant_create_contest(self, _request, queryset):
        content_type = ContentType.objects.get_for_model(Contest)
        add_contest_perm = Permission.objects.get(codename='add_contest', content_type=content_type)
        for user in queryset.all():
            user.user_permissions.add(add_contest_perm)

    @admin.action(description='收回创建比赛权限')
    def revoke_create_contest(self, _request, queryset):
        content_type = ContentType.objects.get_for_model(Contest)
        add_contest_perm = Permission.objects.get(codename='add_contest', content_type=content_type)
        for user in queryset.all():
            user.user_permissions.remove(add_contest_perm)

    @admin.action(description='授予创建公告权限')
    def grant_create_post(self, _request, queryset):
        content_type = ContentType.objects.get_for_model(Post)
        add_post_perm = Permission.objects.get(codename='add_post', content_type=content_type)
        for user in queryset.all():
            user.user_permissions.add(add_post_perm)

    @admin.action(description='收回创建公告权限')
    def revoke_create_post(self, _request, queryset):
        content_type = ContentType.objects.get_for_model(Post)
        add_post_perm = Permission.objects.get(codename='add_post', content_type=content_type)
        for user in queryset.all():
            user.user_permissions.remove(add_post_perm)

    @admin.action(description='授予 Polygon 权限')
    def grant_polygon(self, _request, queryset):
        content_type = ContentType.objects.get_for_model(ProblemRepository)
        polygon_perm = Permission.objects.get(codename='polygon', content_type=content_type)
        for user in queryset.all():
            user.user_permissions.add(polygon_perm)

    @admin.action(description='收回 Polygon 权限')
    def revoke_polygon(self, _request, queryset):
        content_type = ContentType.objects.get_for_model(ProblemRepository)
        polygon_perm = Permission.objects.get(codename='polygon', content_type=content_type)
        for user in queryset.all():
            user.user_permissions.remove(polygon_perm)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# from rbac import rbacRole
# from rbac.models import RbacRole
# from rbac.functions.review import AssignedRoles
# from rbac.functions.administrative import AssignUser, DelAssignUser


# class UserAdmin(admin.ModelAdmin):
#     list_filter = ('is_superuser', 'is_staff', 'is_teacher')
#     fields = ('username', 'student_id', 'student_name',
#               'is_superuser', 'is_staff', 'is_teacher')
#     list_display = ('username', 'student_id', 'student_name',
#                     'is_superuser', 'is_staff', 'is_teacher')
#     search_fields = ('username', 'student_id', 'student_name',
#                      'is_superuser', 'is_staff', 'is_teacher')
#     ordering = ('id',)
#     actions_on_top = True
#     actions_on_bottom = True
#     actions_selection_counter = True
#     actions = ['toTeacher', 'toStaff']
#
#     def get_actions(self, request):
#         actions = super(UserAdmin, self).get_actions(request)
#         if not request.user.is_superuser and 'delete_selected' in actions:
#             del actions['delete_selected']
#         return actions
#
#     def has_add_permission(self, request):
#         return False
#
#     def has_delete_permission(self, request, obj=None):
#         return True if request.user.is_superuser else False
#
#     def toTeacher(self, request, queryset):
#         pass
#         # message_bit = ""
#         # for user in queryset:
#         #     teacherRole = RbacRole.objects.get(
#         #         name=rbacRole.getCommonRoles("TEACHER"))
#         #     if teacherRole in AssignedRoles(user):
#         #         continue
#         #     if AssignUser(user, teacherRole):
#         #         user.is_teacher = True
#         #         user.save()
#         #     else:
#         #         message_bit += '用户名为 %s 的用户设置为老师角色失败\n' % obj.username
#         # if not message_bit:
#         #     message_bit += "批量授予老师角色成功！"
#         # self.message_user(request, message_bit)
#     toTeacher.short_description = '为选中的用户授予老师角色'
#
#     def toStaff(self, request, queryset):
#         pass
#         # message_bit = ""
#         # for user in queryset:
#         #     adminRole = RbacRole.objects.get(
#         #         name=rbacRole.getAdminRoles("ADMIN_ROLE"))
#         #     if adminRole in AssignedRoles(user):
#         #         continue
#         #     if AssignUser(user, adminRole):
#         #         user.is_staff = True
#         #         user.save()
#         #     else:
#         #         message_bit += '用户名为 %s 的用户改为管理员失败\n' % obj.username
#         # if not message_bit:
#         #     message_bit += "批量授予管理员角色成功！"
#         # self.message_user(request, message_bit)
#     toStaff.short_description = '为选中的用户授予管理员角色'
#
#     def save_model(self, request, obj, form, change):
#         pass
#         # message_bit = ""
#         # isTrue = True
#         # if change:
#         #     oldUser = self.model.objects.get(pk=obj.pk)
#         #     if oldUser.is_teacher and (not obj.is_teacher):
#         #         teacherRole = RbacRole.objects.get(
#         #             name=rbacRole.getCommonRoles("TEACHER"))
#         #         if teacherRole in AssignedRoles(obj):
#         #             if not DelAssignUser(user=obj, role=teacherRole):
#         #                 message_bit += "用户 %s 取消老师角色失败\n" % obj.username
#         #                 isTrue = False
#         #             else:
#         #                 message_bit += "用户 %s 取消老师角色成功\n" % obj.username
#         #         else:
#         #             message_bit += "用户 %s 取消老师角色成功\n" % obj.username
#         #     if (not oldUser.is_teacher) and obj.is_teacher:
#         #         teacherRole = RbacRole.objects.get(
#         #             name=rbacRole.getCommonRoles("TEACHER"))
#         #         if teacherRole not in AssignedRoles(obj):
#         #             if not AssignUser(user=obj, role=teacherRole):
#         #                 message_bit += "用户 %s 授予老师角色失败\n" % obj.username
#         #                 isTrue = False
#         #             else:
#         #                 message_bit += "用户 %s 授予老师角色成功\n" % obj.username
#         #         else:
#         #             message_bit += "用户 %s 授予老师角色成功\n" % obj.username
#         #     if oldUser.is_staff and (not obj.is_staff):
#         #         adminRole = RbacRole.objects.get(
#         #             name=rbacRole.getAdminRoles("ADMIN_ROLE"))
#         #         if adminRole in AssignedRoles(obj):
#         #             if not DelAssignUser(user=obj, role=adminRole):
#         #                 message_bit += "用户 %s 取消管理员角色失败\n" % obj.username
#         #                 isTrue = False
#         #             else:
#         #                 message_bit += "用户 %s 取消管理员角色成功\n" % obj.username
#         #         else:
#         #             message_bit += "用户 %s 取消管理员角色成功\n" % obj.username
#         #     if (not oldUser.is_staff) and obj.is_staff:
#         #         adminRole = RbacRole.objects.get(
#         #             name=rbacRole.getAdminRoles("ADMIN_ROLE"))
#         #         if adminRole not in AssignedRoles(obj):
#         #             if not AssignUser(user=obj, role=adminRole):
#         #                 message_bit += "用户 %s 授予管理员角色失败\n" % obj.username
#         #                 isTrue = False
#         #             else:
#         #                 message_bit += "用户 %s 授予管理员角色成功\n" % obj.username
#         #         else:
#         #             message_bit += "用户 %s 授予管理员角色成功\n" % obj.username
#
#         #     if isTrue:
#         #         obj.save()
#         #         message_bit += "用户 %s 修改成功" % obj.username
#         #     else:
#         #         message_bit += "用户 %s 修改失败" % obj.username
#         # else:
#         #     obj.save()
#         #     if obj.is_teacher:
#         #         teacherRole = RbacRole.objects.get(
#         #             name=rbacRole.getCommonRoles("TEACHER"))
#         #         if not AssignUser(user=obj, role=teacherRole):
#         #             message_bit += "用户 %s 授予老师角色失败\n" % obj.username
#         #     if obj.is_staff:
#         #         adminRole = RbacRole.objects.get(
#         #             name=rbacRole.getAdminRoles("ADMIN_ROLE"))
#         #         if not AssignUser(user=obj, role=adminRole):
#         #             message_bit += "用户 %s 授予管理员角色失败\n" % obj.username
#         #     if not message_bit:
#         #         message_bit += "用户 %s 添加成功" % obj.username
#         # self.message_user(request, message_bit)
#
#
# admin.site.register(models.User, UserAdmin)
