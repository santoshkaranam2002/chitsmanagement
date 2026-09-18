from ..models import *
from ..serializers import *
from ..helpers import today_str
from rest_framework import generics
from rest_framework.response import Response


DEFAULT_MEMBER_PASSWORD = "Member@123"


class MemberCreate(generics.GenericAPIView):
    """Admin adds a new member. Body: MemberModels fields + adminId, plus
    optionally { groupId, chitNumber } to assign them into a group right
    away (chitNumber auto-picks the next free number if omitted).

    Also provisions a login (UserModels, role=member) so the member can
    sign in immediately — default password is Member@123 unless the
    request supplies one under "password"; the response includes the
    password once so Admin can share it with the member."""
    serializer_class = MemberSerializers

    def post(self, request):
        try:
            data = request.data.copy()
            data['status'] = data.get('status') or 'Active'
            data['joinDate'] = data.get('joinDate') or today_str()
            data['createdDate'] = today_str()

            email = (data.get('email') or '').strip().lower()
            if email and UserModels.objects.filter(email__iexact=email).exists():
                return Response({"Message": "Fail", "Status": 400,
                                  "Result": "A login already exists with this email."})

            s = MemberSerializers(data=data)
            s.is_valid(raise_exception=True)
            member = s.save()

            password = (request.data.get('password') or DEFAULT_MEMBER_PASSWORD).strip()
            login_email = email or f"member{member.member_id}@chitflow.demo"
            UserModels.objects.create(
                name=member.name, email=login_email, phone=member.phone, role='member',
                password=password, member_id=member.member_id,
                admin_id=int(request.data.get('adminId') or 0), created_date=today_str(),
            )

            group_id = request.data.get('groupId')
            chit_number = request.data.get('chitNumber')
            assigned_group_id = None
            assigned_chit_number = None
            if group_id:
                group_id = int(group_id)
                if not chit_number:
                    used = set(MembershipModels.objects.filter(group_id=group_id).values_list('chit_number', flat=True))
                    n = 1
                    while n in used:
                        n += 1
                    chit_number = n
                MembershipModels.objects.create(group_id=group_id, member_id=member.member_id,
                                                 chit_number=int(chit_number))
                assigned_group_id = group_id
                assigned_chit_number = int(chit_number)

            result = GetMemberSerializers(member).data
            result['loginEmail'] = login_email
            result['loginPassword'] = password
            if assigned_group_id:
                result['assignedGroupId'] = assigned_group_id
                result['assignedChitNumber'] = assigned_chit_number
            return Response({"Message": "Successfull", "Status": 200, "Result": result})
        except Exception as e:
            return Response({"Message": "Fail", "Status": 400, "Result": str(e) or repr(e) or "Unknown error in member_create"})
