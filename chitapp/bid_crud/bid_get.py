from ..models import *
from ..serializers import *
from rest_framework import generics
from rest_framework.response import Response


class BidGet(generics.GenericAPIView):
    """GET /bid_get/?auctionId=5 — bids for one auction, highest first."""
    serializer_class = GetBidSerializers

    def get(self, request):
        try:
            auction_id = request.query_params.get('auctionId')
            rows = list(BidModels.objects.all())
            if auction_id:
                rows = [r for r in rows if r.auction_id == int(auction_id)]
            rows = sorted(rows, key=lambda r: r.amount, reverse=True)
            return Response({"Message": "Successfull", "Status": 200, "Result": GetBidSerializers(rows, many=True).data})
        except Exception as e:
            return Response({"Message": "Fail", "Status": 400, "Result": str(e) or repr(e) or "Unknown error in bid_get"})
