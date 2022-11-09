# from django.contrib.auth.backends import BaseBackend
#
# from account.models import Account
# from django.contrib.auth.hashers import check_password
#
#
# class MyAccountManager(BaseBackend):
#
#     def authenticate(self, request, username=None, password=None):
#
#         try:
#             user = Account.objects.get(email=username)
#             success = user.check_password(password)
#             if success:
#                 return user
#         except Account.DoesNotExist:
#             return None
#
#     def get_user(self, user_id):
#         try:
#             return Account.objects.get(pk=user_id)
#         except Account.DoesNotExist:
#             return None
