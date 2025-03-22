# from .models import User
#
# from sqlalchemy import event
#
# from src.auth import TokenManager
#
#
# def after_delete_listener(user, connection, target):
#     print("DELETED")
#     TokenManager().sync_delete_refresh(target.id)
#
#
# def initialize_orm_listeners():
#     print("LISTENERS INTIALIZED!")
#     event.listen(User, "after_delete", after_delete_listener)
