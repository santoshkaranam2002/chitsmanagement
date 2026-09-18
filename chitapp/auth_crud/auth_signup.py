from ..models import *
from ..serializers import *
from ..helpers import today_str
from rest_framework import generics
from rest_framework.response import Response


class AuthSignup(generics.GenericAPIView):
    """Body: {orgName, ownerName, email, phone, password}. Creates a new
    Admin/organizer account — this is the only self-signup in the app;
    members are always added by an admin (see member_create)."""
    serializer_class = UserSerializers

    def post(self, request):
        try:
            email = (request.data.get("email") or "").strip().lower()
            if not email:
                return Response({"Message": "Fail", "Status": 400, "Result": "Email is required."})

            if UserModels.objects.filter(email__iexact=email).exists():
                return Response({"Message": "Fail", "Status": 400,
                                  "Result": "An account with this email already exists. Please log in instead."})

            data = request.data.copy()
            data['email'] = email
            data['name'] = data.get('ownerName') or data.get('name') or ''
            data['role'] = 'admin'
            data['createdDate'] = today_str()

            s = UserSerializers(data=data)
            s.is_valid(raise_exception=True)
            obj = s.save()

            # An admin's own admin_id is its own user_id — every group/member
            # this org creates will carry this same value for data scoping.
            obj.admin_id = obj.user_id
            obj.save()

            return Response({"Message": "Successfull", "Status": 200, "Result": GetUserSerializers(obj).data})
        except Exception as e:
            return Response({"Message": "Fail", "Status": 400, "Result": str(e) or repr(e) or "Unknown error in auth_signup"})
