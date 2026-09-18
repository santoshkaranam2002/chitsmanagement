from ..models import *
from ..serializers import *
from rest_framework import generics
from rest_framework.response import Response


class MemberUpdate(generics.GenericAPIView):
    serializer_class = MemberSerializers

    def put(self, request, member_id):
        try:
            a = MemberModels.objects.get(member_id=member_id)
            b = MemberSerializers(a, data=request.data, partial=True)
            b.is_valid(raise_exception=True)
            data = b.save()

            # keep the linked login's display name/phone in sync
            login = UserModels.objects.filter(member_id=member_id, role='member').first()
            if login:
                login.name = data.name
                login.phone = data.phone
                login.save()

            return Response({"Message": "Successfull", "Status": 200, "Result": GetMemberSerializers(data).data})
        except Exception as e:
            return Response({"Message": "Fail", "Status": 400, "Result": str(e) or repr(e) or "Unknown error in member_update"})
