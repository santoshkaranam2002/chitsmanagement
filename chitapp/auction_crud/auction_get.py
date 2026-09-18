from ..models import *
from ..serializers import *
from rest_framework import generics
from rest_framework.response import Response


class AuctionGet(generics.GenericAPIView):
    """GET /auction_get/?groupId=&status=&adminId=&memberId=
    GET /auction_get/<id> — single auction."""
    serializer_class = GetAuctionSerializers

    def get(self, request, auction_id=None):
        try:
            all_rows = list(AuctionModels.objects.all())

            if auction_id:
                rows = [r for r in all_rows if r.auction_id == int(auction_id)]
                return Response({"Message": "Successfull", "Status": 200,
                                  "Result": GetAuctionSerializers(rows, many=True).data})

            params = request.query_params
            rows = all_rows

            group_id = params.get('groupId')
            if group_id:
                rows = [r for r in rows if r.group_id == int(group_id)]

            admin_id = params.get('adminId')
            if admin_id:
                admin_group_ids = set(ChitGroupModels.objects.filter(admin_id=int(admin_id)).values_list('group_id', flat=True))
                rows = [r for r in rows if r.group_id in admin_group_ids]

            member_id = params.get('memberId')
            if member_id:
                member_group_ids = set(MembershipModels.objects.filter(member_id=int(member_id)).values_list('group_id', flat=True))
                rows = [r for r in rows if r.group_id in member_group_ids]

            status_f = params.get('status')
            if status_f and status_f != 'All':
                rows = [r for r in rows if r.status == status_f]

            rows = sorted(rows, key=lambda r: (r.scheduled_date, r.month_index), reverse=True)
            return Response({"Message": "Successfull", "Status": 200,
                              "Result": GetAuctionSerializers(rows, many=True).data})
        except Exception as e:
            return Response({"Message": "Fail", "Status": 400, "Result": str(e) or repr(e) or "Unknown error in auction_get"})
