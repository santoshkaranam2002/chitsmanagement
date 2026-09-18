from ..models import *
from ..serializers import *
from ..helpers import today_str
import random
from rest_framework import generics
from rest_framework.response import Response


class PaymentMarkPaid(generics.GenericAPIView):
    """POST /payment_mark_paid/<id> — Body: {method?}. Marks one payment
    Paid and stamps it with today's date + a generated transaction id."""
    serializer_class = GetPaymentSerializers

    def post(self, request, payment_id):
        try:
            p = PaymentModels.objects.get(payment_id=payment_id)
            p.status = 'Paid'
            p.paid_date = today_str()
            p.method = request.data.get('method') or p.method or 'UPI'
            p.transaction_id = p.transaction_id or f"TXN{random.randint(100000, 999999)}"
            p.save()
            return Response({"Message": "Successfull", "Status": 200, "Result": GetPaymentSerializers(p).data})
        except Exception as e:
            return Response({"Message": "Fail", "Status": 400, "Result": str(e) or repr(e) or "Unknown error in payment_mark_paid"})
