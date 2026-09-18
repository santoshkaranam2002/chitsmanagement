from ..models import *
from ..serializers import *
from rest_framework import generics
from rest_framework.response import Response


class GroupUpdate(generics.GenericAPIView):
    serializer_class = GroupSerializers

    def put(self, request, group_id):
        try:
            a = ChitGroupModels.objects.get(group_id=group_id)
            b = GroupSerializers(a, data=request.data, partial=True)
            b.is_valid(raise_exception=True)
            data = b.save()
            return Response({"Message": "Successfull", "Status": 200, "Result": GetGroupSerializers(data).data})
        except Exception as e:
            return Response({"Message": "Fail", "Status": 400, "Result": str(e) or repr(e) or "Unknown error in group_update"})
