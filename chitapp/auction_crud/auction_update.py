from ..models import *
from ..serializers import *
from rest_framework import generics
from rest_framework.response import Response


class AuctionUpdate(generics.GenericAPIView):
    serializer_class = AuctionSerializers

    def put(self, request, auction_id):
        try:
            a = AuctionModels.objects.get(auction_id=auction_id)
            b = AuctionSerializers(a, data=request.data, partial=True)
            b.is_valid(raise_exception=True)
            data = b.save()
            return Response({"Message": "Successfull", "Status": 200, "Result": GetAuctionSerializers(data).data})
        except Exception as e:
            return Response({"Message": "Fail", "Status": 400, "Result": str(e) or repr(e) or "Unknown error in auction_update"})
