from ..models import *
from ..serializers import *
from ..helpers import notify
from rest_framework import generics
from rest_framework.response import Response


class AuctionClose(generics.GenericAPIView):
    """POST /auction_close/<id> — Live -> Pending Confirmation. Picks the
    highest bid as winner and computes the full settlement, exactly as:

        prizeAmount   = chitValue - winningBid
        commission    = group's Fixed value, or round(winningBid * pct/100)
        pool          = winningBid - commission
        dividend      = round(pool / totalMembers)
        finalPayable  = monthlyInstallment - dividend

    Nothing is written to Payments/Dividends yet — that only happens once
    Admin reviews and calls auction_confirm."""
    serializer_class = GetAuctionSerializers

    def post(self, request, auction_id):
        try:
            a = AuctionModels.objects.get(auction_id=auction_id)
            if a.status != 'Live':
                return Response({"Message": "Fail", "Status": 400,
                                  "Result": f"Auction is {a.status}, cannot close it."})

            top_bid = BidModels.objects.filter(auction_id=auction_id).order_by('-amount').first()
            if not top_bid:
                return Response({"Message": "Fail", "Status": 400, "Result": "No bids were placed — cannot determine a winner."})

            group = ChitGroupModels.objects.get(group_id=a.group_id)

            commission = (group.commission_value if group.commission_type == 'Fixed'
                          else round(top_bid.amount * group.commission_value / 100))
            prize_amount = group.chit_value - top_bid.amount
            pool = top_bid.amount - commission
            per_member = round(pool / group.total_members) if group.total_members else 0
            final_installment = group.monthly_installment - per_member

            a.status = 'Pending Confirmation'
            a.winner_member_id = top_bid.member_id
            a.winning_bid = top_bid.amount
            a.prize_amount = prize_amount
            a.commission = commission
            a.dividend_per_member = per_member
            a.final_installment = final_installment
            a.confirmed = False
            a.save()

            notify(group.admin_id, 'admin', f"{a.label} awaiting confirmation",
                   f"{group.name} auction closed — review the result before confirming.",
                   'result', group_id=a.group_id)

            return Response({"Message": "Successfull", "Status": 200, "Result": GetAuctionSerializers(a).data})
        except Exception as e:
            return Response({"Message": "Fail", "Status": 400, "Result": str(e) or repr(e) or "Unknown error in auction_close"})
