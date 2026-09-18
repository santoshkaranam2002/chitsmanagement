from ..models import *
from ..serializers import *
from rest_framework import generics
from rest_framework.response import Response


class AuctionCreate(generics.GenericAPIView):
    """Admin schedules a new auction for a group. Body: {groupId, monthIndex,
    label?, scheduledDate, startTime, endTime, startingBid?, bidIncrement?}.
    startingBid/bidIncrement default to the group's own scheme values."""
    serializer_class = AuctionSerializers

    def post(self, request):
        try:
            group_id = int(request.data.get('groupId'))
            group = ChitGroupModels.objects.get(group_id=group_id)

            data = request.data.copy()
            month_index = int(data.get('monthIndex') or (group.current_month + 1))
            data['monthIndex'] = month_index
            data['label'] = data.get('label') or f"Auction #{month_index}"
            data['status'] = 'Upcoming'
            data['startingBid'] = data.get('startingBid') or group.starting_bid
            data['bidIncrement'] = data.get('bidIncrement') or group.bid_increment
            data['confirmed'] = False

            s = AuctionSerializers(data=data)
            s.is_valid(raise_exception=True)
            obj = s.save()

            return Response({"Message": "Successfull", "Status": 200, "Result": GetAuctionSerializers(obj).data})
        except Exception as e:
            return Response({"Message": "Fail", "Status": 400, "Result": str(e) or repr(e) or "Unknown error in auction_create"})
