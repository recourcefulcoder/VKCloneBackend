from sqlalchemy import event
from sqlalchemy.orm import ORMExecuteState

from src.celery_app import delete_refresh_task

from .models import User


def delete_refresh_token(session, connection, target):
    delete_refresh_task.delay(target.id)
    pass


def orm_execution(orm_execute_state: ORMExecuteState):
    # for automatic deletion of user tokens from
    # Redis on deletion
    if orm_execute_state.is_delete:
        if orm_execute_state.bind_mapper.class_ == User:
            pass


def initialize_orm_listeners():
    event.listen(User, "after_delete", delete_refresh_token)
