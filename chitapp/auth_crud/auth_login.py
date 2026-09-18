from ..models import *
from ..serializers import *
from rest_framework import generics
from rest_framework.response import Response


class AuthLogin(generics.GenericAPIView):
    """Body: {email, password, role}. Role must match the account's stored
    role — this is what powers the Admin/Member toggle on the login page."""
    serializer_class = GetUserSerializers

    def post(self, request):
        try:
            identifier = (request.data.get("email") or "").strip().lower()
            password = (request.data.get("password") or "").strip()
            role = (request.data.get("role") or "").strip().lower()

            if not identifier or not password or not role:
                return Response({"Message": "Fail", "Status": 400,
                                  "Result": "Email/phone, password and role are all required."})

            user = UserModels.objects.filter(email__iexact=identifier).first()
            if not user:
                user = UserModels.objects.filter(phone=identifier).first()

            if not user:
                return Response({"Message": "Fail", "Status": 400,
                                  "Result": "No account found with this email/phone."})

            if user.password != password:
                return Response({"Message": "Fail", "Status": 400,
                                  "Result": "Incorrect password. Please try again."})

            if user.role.lower() != role:
                return Response({"Message": "Fail", "Status": 400,
                                  "Result": f"This account is registered as {user.role}. Please select the correct role."})

            return Response({"Message": "Successfull", "Status": 200, "Result": GetUserSerializers(user).data})
        except Exception as e:
            return Response({"Message": "Fail", "Status": 400, "Result": str(e) or repr(e) or "Unknown error in auth_login"})
