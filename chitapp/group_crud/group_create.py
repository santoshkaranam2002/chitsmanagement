from ..models import *
from ..serializers import *
from ..helpers import today_str
from rest_framework import generics
from rest_framework.response import Response


class GroupCreate(generics.GenericAPIView):
    """Admin creates a new chit scheme (group). Body matches ChitGroup
    fields from the frontend's "New Chit Group" modal."""
    serializer_class = GroupSerializers

    def post(self, request):
        try:
            data = request.data.copy()
            data['status'] = data.get('status') or 'Upcoming'
            data['currentMonth'] = data.get('currentMonth') or 0
            data['startDate'] = data.get('startDate') or today_str()
            data['createdDate'] = today_str()

            s = GroupSerializers(data=data)
            s.is_valid(raise_exception=True)
            obj = s.save()

            return Response({"Message": "Successfull", "Status": 200, "Result": GetGroupSerializers(obj).data})
        except Exception as e:
            return Response({"Message": "Fail", "Status": 400, "Result": str(e) or repr(e) or "Unknown error in group_create"})
