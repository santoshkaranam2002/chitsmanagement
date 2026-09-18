from ..models import *
from ..serializers import *
from rest_framework import generics
from rest_framework.response import Response


class GroupDelete(generics.GenericAPIView):
    serializer_class = GetGroupSerializers

    def delete(self, request, group_id):
        try:
            a = ChitGroupModels.objects.get(group_id=group_id)
            a.delete()
            MembershipModels.objects.filter(group_id=group_id).delete()
            return Response({"Message": "Successfull", "Status": 200, "Result": "Deleted {}".format(group_id)})
        except Exception as e:
            return Response({"Message": "Fail", "Status": 400, "Result": str(e) or repr(e) or "Unknown error in group_delete"})
