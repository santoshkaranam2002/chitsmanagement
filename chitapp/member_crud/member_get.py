from ..models import *
from ..serializers import *
from rest_framework import generics
from rest_framework.response import Response


class MemberGet(generics.GenericAPIView):
    """GET /member_get/?adminId=1&groupId=2&q=sai — list.
    GET /member_get/<id> — single member."""
    serializer_class = GetMemberSerializers

    def get(self, request, member_id=None):
        try:
            all_rows = list(MemberModels.objects.all())

            if member_id:
                rows = [r for r in all_rows if r.member_id == int(member_id)]
                return Response({"Message": "Successfull", "Status": 200,
                                  "Result": GetMemberSerializers(rows, many=True).data})

            params = request.query_params
            rows = all_rows

            admin_id = params.get('adminId')
            if admin_id:
                rows = [r for r in rows if r.admin_id == int(admin_id)]

            group_id = params.get('groupId')
            if group_id:
                member_ids = set(MembershipModels.objects.filter(group_id=int(group_id)).values_list('member_id', flat=True))
                rows = [r for r in rows if r.member_id in member_ids]

            q = params.get('q')
            if q:
                ql = q.lower()
                rows = [r for r in rows if ql in (r.name or '').lower() or ql in (r.phone or '') or ql in (r.code or '').lower()]

            rows = sorted(rows, key=lambda r: r.member_id, reverse=True)
            return Response({"Message": "Successfull", "Status": 200,
                              "Result": GetMemberSerializers(rows, many=True).data})
        except Exception as e:
            return Response({"Message": "Fail", "Status": 400, "Result": str(e) or repr(e) or "Unknown error in member_get"})
