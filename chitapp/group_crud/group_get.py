from ..models import *
from ..serializers import *
from rest_framework import generics
from rest_framework.response import Response


class GroupGet(generics.GenericAPIView):
    """GET /group_get/?adminId=1&status=Active — list groups for one org.
    GET /group_get/<id> — single group."""
    serializer_class = GetGroupSerializers

    def get(self, request, group_id=None):
        try:
            all_rows = list(ChitGroupModels.objects.all())

            if group_id:
                rows = [r for r in all_rows if r.group_id == int(group_id)]
                return Response({"Message": "Successfull", "Status": 200,
                                  "Result": GetGroupSerializers(rows, many=True).data})

            params = request.query_params
            rows = all_rows

            admin_id = params.get('adminId')
            if admin_id:
                rows = [r for r in rows if r.admin_id == int(admin_id)]

            status_f = params.get('status')
            if status_f and status_f != 'All':
                rows = [r for r in rows if r.status == status_f]

            rows = sorted(rows, key=lambda r: r.group_id, reverse=True)
            return Response({"Message": "Successfull", "Status": 200,
                              "Result": GetGroupSerializers(rows, many=True).data})
        except Exception as e:
            return Response({"Message": "Fail", "Status": 400, "Result": str(e) or repr(e) or "Unknown error in group_get"})
