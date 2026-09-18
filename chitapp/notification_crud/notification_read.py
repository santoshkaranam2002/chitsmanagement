from ..models import *
from ..serializers import *
from rest_framework import generics
from rest_framework.response import Response


class NotificationRead(generics.GenericAPIView):
    """POST /notification_read/<id> — marks one notification read."""
    serializer_class = GetNotificationSerializers

    def post(self, request, notification_id):
        try:
            n = NotificationModels.objects.get(notification_id=notification_id)
            n.read = True
            n.save()
            return Response({"Message": "Successfull", "Status": 200, "Result": GetNotificationSerializers(n).data})
        except Exception as e:
            return Response({"Message": "Fail", "Status": 400, "Result": str(e) or repr(e) or "Unknown error in notification_read"})
