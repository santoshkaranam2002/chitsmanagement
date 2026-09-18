from ..models import *
from ..serializers import *
from rest_framework import generics
from rest_framework.response import Response


class MemberDelete(generics.GenericAPIView):
    serializer_class = GetMemberSerializers

    def delete(self, request, member_id):
        try:
            a = MemberModels.objects.get(member_id=member_id)
            a.delete()
            MembershipModels.objects.filter(member_id=member_id).delete()
            UserModels.objects.filter(member_id=member_id, role='member').delete()
            return Response({"Message": "Successfull", "Status": 200, "Result": "Deleted {}".format(member_id)})
        except Exception as e:
            return Response({"Message": "Fail", "Status": 400, "Result": str(e) or repr(e) or "Unknown error in member_delete"})
