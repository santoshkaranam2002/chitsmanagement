from datetime import datetime
from .models import NotificationModels


def now_str():
    return datetime.now().strftime('%Y-%m-%d %H:%M')


def today_str():
    return datetime.now().strftime('%Y-%m-%d')


def notify(admin_id, audience, title, message, ntype='system', member_id=None, group_id=None):
    """Creates one notification row. audience='admin' shows it on the
    organizer's bell; audience='member' shows it only to member_id."""
    NotificationModels.objects.create(
        admin_id=admin_id or 0,
        audience=audience,
        member_id=member_id,
        group_id=group_id,
        title=title,
        message=message,
        type=ntype,
        time=now_str(),
        read=False,
    )
