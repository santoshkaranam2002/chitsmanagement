from ..models import *
from ..serializers import *
from ..helpers import now_str
from rest_framework import generics
from rest_framework.response import Response


class BidCreate(generics.GenericAPIView):
    """Body: {auctionId, memberId, amount}. Validates: auction must be
    Live, member must belong to the group, and amount must be at least
    (current leading bid or startingBid) + bidIncrement."""
    serializer_class = BidSerializers

    def post(self, request):
        try:
            auction_id = int(request.data.get('auctionId'))
            member_id = int(request.data.get('memberId'))
            amount = float(request.data.get('amount'))

            a = AuctionModels.objects.get(auction_id=auction_id)
            if a.status != 'Live':
                return Response({"Message": "Fail", "Status": 400, "Result": "This auction is not currently live."})

            if not MembershipModels.objects.filter(group_id=a.group_id, member_id=member_id).exists():
                return Response({"Message": "Fail", "Status": 400, "Result": "You are not a member of this group."})

            top_bid = BidModels.objects.filter(auction_id=auction_id).order_by('-amount').first()
            min_required = (top_bid.amount if top_bid else a.starting_bid) + a.bid_increment
            if amount < min_required:
                return Response({"Message": "Fail", "Status": 400,
                                  "Result": f"Your bid must be at least ₹{int(min_required)} (current bid + ₹{int(a.bid_increment)} increment)."})

            member = MemberModels.objects.get(member_id=member_id)
            bid = BidModels.objects.create(auction_id=auction_id, member_id=member_id,
                                            member_name=member.name, amount=amount, time=now_str())

            return Response({"Message": "Successfull", "Status": 200, "Result": GetBidSerializers(bid).data})
        except Exception as e:
            return Response({"Message": "Fail", "Status": 400, "Result": str(e) or repr(e) or "Unknown error in bid_create"})
