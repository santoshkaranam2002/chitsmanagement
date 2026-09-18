from ..models import *
from ..serializers import *
from ..helpers import notify
from rest_framework import generics
from rest_framework.response import Response


class AuctionOpen(generics.GenericAPIView):
    """POST /auction_open/<id> — Upcoming -> Live. Notifies every member
    of the group plus the admin."""
    serializer_class = GetAuctionSerializers

    def post(self, request, auction_id):
        try:
            a = AuctionModels.objects.get(auction_id=auction_id)
            if a.status != 'Upcoming':
                return Response({"Message": "Fail", "Status": 400,
                                  "Result": f"Auction is already {a.status}, cannot open it."})

            a.status = 'Live'
            a.save()

            group = ChitGroupModels.objects.filter(group_id=a.group_id).first()
            group_name = group.name if group else 'Your group'

            notify(group.admin_id if group else 0, 'admin', f"{a.label} is live",
                   f"{group_name} auction opened at {a.start_time}.", 'auction', group_id=a.group_id)

            member_ids = MembershipModels.objects.filter(group_id=a.group_id).values_list('member_id', flat=True)
            for mid in member_ids:
                notify(group.admin_id if group else 0, 'member', f"{a.label} is now open",
                       f"{group_name} {a.label} has started. Place your bid before {a.end_time}.",
                       'auction', member_id=mid, group_id=a.group_id)

            return Response({"Message": "Successfull", "Status": 200, "Result": GetAuctionSerializers(a).data})
        except Exception as e:
            return Response({"Message": "Fail", "Status": 400, "Result": str(e) or repr(e) or "Unknown error in auction_open"})
