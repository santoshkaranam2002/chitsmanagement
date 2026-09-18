from ..models import *
from ..serializers import *
from rest_framework import generics
from rest_framework.response import Response


class MemberAssignGroup(generics.GenericAPIView):
    """Body: {memberId, groupId, chitNumber?}. Adds an EXISTING member into
    another group (used by the "Add Member" button on a Group Detail page
    when the picked member already exists in the system)."""
    serializer_class = MembershipSerializers

    def post(self, request):
        try:
            member_id = int(request.data.get('memberId'))
            group_id = int(request.data.get('groupId'))

            if MembershipModels.objects.filter(member_id=member_id, group_id=group_id).exists():
                return Response({"Message": "Fail", "Status": 400, "Result": "This member is already in this group."})

            chit_number = request.data.get('chitNumber')
            if not chit_number:
                used = set(MembershipModels.objects.filter(group_id=group_id).values_list('chit_number', flat=True))
                n = 1
                while n in used:
                    n += 1
                chit_number = n

            row = MembershipModels.objects.create(group_id=group_id, member_id=member_id, chit_number=int(chit_number))
            return Response({"Message": "Successfull", "Status": 200, "Result": GetMembershipSerializers(row).data})
        except Exception as e:
            return Response({"Message": "Fail", "Status": 400, "Result": str(e) or repr(e) or "Unknown error in member_assign_group"})
