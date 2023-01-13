from rest_framework import permissions
from .permissions import IsStaffEditorPermisson


class StaffEditorPermissionMixin():
    permission_classes = [permissions.IsAdminUser, IsStaffEditorPermisson]
