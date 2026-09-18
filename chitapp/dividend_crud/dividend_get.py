from ..models import *
from ..serializers import *
from rest_framework import generics
from rest_framework.response import Response


class DividendGet(generics.GenericAPIView):
    """GET /dividend_get/?adminId=&groupId=&memberId="""
    serializer_class = GetDividendSerializers

    def get(self, request):
        try:
            rows = list(DividendModels.objects.all())
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
                member_group_ids = set(MembershipModels.objects.filter(member_id=int(member_id)).values_list('group_id', flat=True))
                rows = [r for r in rows if r.group_id in member_group_ids]

            rows = sorted(rows, key=lambda r: r.month_index, reverse=True)
            return Response({"Message": "Successfull", "Status": 200, "Result": GetDividendSerializers(rows, many=True).data})
        except Exception as e:
            return Response({"Message": "Fail", "Status": 400, "Result": str(e) or repr(e) or "Unknown error in dividend_get"})
