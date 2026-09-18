from ..models import *
from ..serializers import *
from rest_framework import generics
from rest_framework.response import Response


class NotificationGet(generics.GenericAPIView):
    """GET /notification_get/?audience=admin&adminId=1
    GET /notification_get/?audience=member&memberId=4"""
    serializer_class = GetNotificationSerializers

    def get(self, request):
        try:
            rows = list(NotificationModels.objects.all())
            params = request.query_params

            audience = params.get('audience')
            if audience:
                rows = [r for r in rows if r.audience == audience]

            admin_id = params.get('adminId')
            if admin_id:
                rows = [r for r in rows if r.admin_id == int(admin_id)]

            member_id = params.get('memberId')
            if member_id:
                rows = [r for r in rows if r.member_id == int(member_id)]

            rows = sorted(rows, key=lambda r: r.notification_id, reverse=True)[:50]
            return Response({"Message": "Successfull", "Status": 200, "Result": GetNotificationSerializers(rows, many=True).data})
        except Exception as e:
            return Response({"Message": "Fail", "Status": 400, "Result": str(e) or repr(e) or "Unknown error in notification_get"})
