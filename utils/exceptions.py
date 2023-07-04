from rest_framework.exceptions import APIException, ValidationError


class LockedException(APIException):
    status_code = 422
    default_detail = "Cannot edit a locked item. This record is considered ReadOnly since its already APPROVED! You might need to contact the administrator to unlock this item!"
