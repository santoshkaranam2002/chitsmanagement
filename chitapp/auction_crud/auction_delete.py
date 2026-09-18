from ..models import *
from ..serializers import *
from rest_framework import generics
from rest_framework.response import Response


class AuctionDelete(generics.GenericAPIView):
    serializer_class = GetAuctionSerializers

    def delete(self, request, auction_id):
        try:
            a = AuctionModels.objects.get(auction_id=auction_id)
            a.delete()
            BidModels.objects.filter(auction_id=auction_id).delete()
            return Response({"Message": "Successfull", "Status": 200, "Result": "Deleted {}".format(auction_id)})
        except Exception as e:
            return Response({"Message": "Fail", "Status": 400, "Result": str(e) or repr(e) or "Unknown error in auction_delete"})
