from ..models import *
from ..serializers import *
from rest_framework import generics
from rest_framework.response import Response


class MembershipGet(generics.GenericAPIView):
    """GET /membership_get/?adminId=&groupId=&memberId= — the raw group<->
    member<->chitNumber junction rows, used by the frontend to resolve
    chit numbers and group/member membership everywhere."""
    serializer_class = GetMembershipSerializers

    def get(self, request):
        try:
            rows = list(MembershipModels.objects.all())
            params = request.query_params

            admin_id = params.get('adminId')
            if admin_id:
                admin_group_ids = set(ChitGroupModels.objects.filter(admin_id=int(admin_id)).values_list('group_id', flat=True))
                rows = [r for r in rows if r.group_id in admin_group_ids]

            group_id = params.get('groupId')
            if group_id:
                rows = [r for r in rows if r.group_id == int(group_id)]

            member_id = params.get('memberId')
            if member_id:
                rows = [r for r in rows if r.member_id == int(member_id)]

            return Response({"Message": "Successfull", "Status": 200, "Result": GetMembershipSerializers(rows, many=True).data})
        except Exception as e:
            return Response({"Message": "Fail", "Status": 400, "Result": str(e) or repr(e) or "Unknown error in membership_get"})
