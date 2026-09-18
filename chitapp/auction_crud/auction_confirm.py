from ..models import *
from ..serializers import *
from ..helpers import notify, today_str
import random
from rest_framework import generics
from rest_framework.response import Response


class AuctionConfirm(generics.GenericAPIView):
    """POST /auction_confirm/<id> — Pending Confirmation -> Completed.
    Generates the real financial records from the settlement that
    auction_close computed:

      - one Installment Payment per member (the winner still pays the
        full monthly installment; everyone else pays finalInstallment)
      - one Winner Payout Payment for the winner, already marked Paid
      - one Dividend row for group-wide dividend reporting
      - a result notification to every member + the admin
    """
    serializer_class = GetAuctionSerializers

    def post(self, request, auction_id):
        try:
            a = AuctionModels.objects.get(auction_id=auction_id)
            if a.status != 'Pending Confirmation':
                return Response({"Message": "Fail", "Status": 400,
                                  "Result": f"Auction is {a.status}, nothing to confirm."})

            group = ChitGroupModels.objects.get(group_id=a.group_id)
            memberships = MembershipModels.objects.filter(group_id=a.group_id)

            for m in memberships:
                amount = group.monthly_installment if m.member_id == a.winner_member_id else a.final_installment
                PaymentModels.objects.create(
                    group_id=a.group_id, member_id=m.member_id, month_index=a.month_index,
                    type='Installment', amount=amount, due_date=a.scheduled_date,
                    status='Pending',
                )

            PaymentModels.objects.create(
                group_id=a.group_id, member_id=a.winner_member_id, month_index=a.month_index,
                type='Winner Payout', amount=a.prize_amount, due_date=a.scheduled_date,
                paid_date=today_str(), status='Paid', method='Bank Transfer',
                transaction_id=f"TXN{random.randint(100000, 999999)}",
            )

            DividendModels.objects.create(
                group_id=a.group_id, month_index=a.month_index, auction_id=a.auction_id,
                per_member=a.dividend_per_member, total_pool=(a.dividend_per_member or 0) * group.total_members,
                eligible_members=group.total_members,
            )

            a.status = 'Completed'
            a.confirmed = True
            a.save()

            if a.month_index > group.current_month:
                group.current_month = a.month_index
                group.save()

            winner = MemberModels.objects.filter(member_id=a.winner_member_id).first()
            winner_name = winner.name if winner else 'A member'

            for m in memberships:
                won = m.member_id == a.winner_member_id
                notify(group.admin_id, 'member',
                       f"You won {a.label}!" if won else f"{a.label} result",
                       (f"Congratulations — your winning bid of ₹{int(a.winning_bid)} was accepted."
                        if won else f"The winning bid was ₹{int(a.winning_bid)} by {winner_name}. Your dividend: ₹{int(a.dividend_per_member)}."),
                       'result', member_id=m.member_id, group_id=a.group_id)

            notify(group.admin_id, 'admin', f"{a.label} settled",
                   f"{group.name} settlement confirmed — dues and dividends have been generated.",
                   'result', group_id=a.group_id)

            return Response({"Message": "Successfull", "Status": 200, "Result": GetAuctionSerializers(a).data})
        except Exception as e:
            return Response({"Message": "Fail", "Status": 400, "Result": str(e) or repr(e) or "Unknown error in auction_confirm"})
