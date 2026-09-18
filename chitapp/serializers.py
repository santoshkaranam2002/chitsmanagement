from rest_framework import serializers
from .models import *


# ───────────────────────── User / Auth ─────────────────────────

class UserSerializers(serializers.ModelSerializer):
    orgName = serializers.CharField(source='org_name', required=False, allow_blank=True)
    memberId = serializers.IntegerField(source='member_id', required=False, allow_null=True)
    adminId = serializers.IntegerField(source='admin_id', required=False, allow_null=True)
    createdDate = serializers.CharField(source='created_date', required=False, allow_blank=True)

    class Meta:
        model = UserModels
        fields = ['name', 'email', 'phone', 'role', 'password', 'orgName', 'memberId', 'adminId', 'createdDate']

    def create(self, validated_data):
        return UserModels.objects.create(**validated_data)


class GetUserSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user_id', read_only=True)
    orgName = serializers.CharField(source='org_name', read_only=True)
    memberId = serializers.IntegerField(source='member_id', read_only=True)
    adminId = serializers.IntegerField(source='admin_id', read_only=True)
    initials = serializers.SerializerMethodField()

    class Meta:
        model = UserModels
        fields = ['id', 'name', 'email', 'phone', 'role', 'orgName', 'memberId', 'adminId', 'initials']

    def get_initials(self, obj):
        parts = (obj.name or '').split()
        return ''.join(p[0].upper() for p in parts[:2]) or '?'


# ───────────────────────── Chit Group ─────────────────────────

class GroupSerializers(serializers.ModelSerializer):
    chitValue = serializers.FloatField(source='chit_value', required=False)
    totalMembers = serializers.IntegerField(source='total_members', required=False)
    durationMonths = serializers.IntegerField(source='duration_months', required=False)
    monthlyInstallment = serializers.FloatField(source='monthly_installment', required=False)
    auctionDay = serializers.IntegerField(source='auction_day', required=False)
    startDate = serializers.CharField(source='start_date', required=False, allow_blank=True)
    currentMonth = serializers.IntegerField(source='current_month', required=False)
    startingBid = serializers.FloatField(source='starting_bid', required=False)
    minBid = serializers.FloatField(source='min_bid', required=False)
    maxBid = serializers.FloatField(source='max_bid', required=False)
    bidIncrement = serializers.FloatField(source='bid_increment', required=False)
    commissionType = serializers.CharField(source='commission_type', required=False)
    commissionValue = serializers.FloatField(source='commission_value', required=False)
    adminId = serializers.IntegerField(source='admin_id', required=False)
    createdDate = serializers.CharField(source='created_date', required=False, allow_blank=True)

    class Meta:
        model = ChitGroupModels
        fields = ['name', 'chitValue', 'totalMembers', 'durationMonths', 'monthlyInstallment', 'auctionDay',
                  'startDate', 'status', 'currentMonth', 'startingBid', 'minBid', 'maxBid', 'bidIncrement',
                  'commissionType', 'commissionValue', 'foreman', 'adminId', 'createdDate']

    def create(self, validated_data):
        return ChitGroupModels.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class GetGroupSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(source='group_id', read_only=True)
    chitValue = serializers.FloatField(source='chit_value', read_only=True)
    totalMembers = serializers.IntegerField(source='total_members', read_only=True)
    durationMonths = serializers.IntegerField(source='duration_months', read_only=True)
    monthlyInstallment = serializers.FloatField(source='monthly_installment', read_only=True)
    auctionDay = serializers.IntegerField(source='auction_day', read_only=True)
    startDate = serializers.CharField(source='start_date', read_only=True)
    currentMonth = serializers.IntegerField(source='current_month', read_only=True)
    startingBid = serializers.FloatField(source='starting_bid', read_only=True)
    minBid = serializers.FloatField(source='min_bid', read_only=True)
    maxBid = serializers.FloatField(source='max_bid', read_only=True)
    bidIncrement = serializers.FloatField(source='bid_increment', read_only=True)
    commissionType = serializers.CharField(source='commission_type', read_only=True)
    commissionValue = serializers.FloatField(source='commission_value', read_only=True)
    adminId = serializers.IntegerField(source='admin_id', read_only=True)
    memberCount = serializers.SerializerMethodField()

    class Meta:
        model = ChitGroupModels
        fields = ['id', 'name', 'chitValue', 'totalMembers', 'durationMonths', 'monthlyInstallment', 'auctionDay',
                  'startDate', 'status', 'currentMonth', 'startingBid', 'minBid', 'maxBid', 'bidIncrement',
                  'commissionType', 'commissionValue', 'foreman', 'adminId', 'memberCount']

    def get_memberCount(self, obj):
        return MembershipModels.objects.filter(group_id=obj.group_id).count()


# ───────────────────────── Member ─────────────────────────

class MemberSerializers(serializers.ModelSerializer):
    bankAccount = serializers.CharField(source='bank_account', required=False, allow_blank=True)
    joinDate = serializers.CharField(source='join_date', required=False, allow_blank=True)
    adminId = serializers.IntegerField(source='admin_id', required=False)
    createdDate = serializers.CharField(source='created_date', required=False, allow_blank=True)

    class Meta:
        model = MemberModels
        fields = ['name', 'phone', 'email', 'address', 'nominee', 'bankAccount', 'status',
                  'joinDate', 'adminId', 'createdDate']

    def create(self, validated_data):
        return MemberModels.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class GetMemberSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(source='member_id', read_only=True)
    bankAccount = serializers.CharField(source='bank_account', read_only=True)
    joinDate = serializers.CharField(source='join_date', read_only=True)
    adminId = serializers.IntegerField(source='admin_id', read_only=True)
    initials = serializers.SerializerMethodField()
    groupIds = serializers.SerializerMethodField()

    class Meta:
        model = MemberModels
        fields = ['id', 'code', 'name', 'phone', 'email', 'address', 'initials', 'joinDate',
                  'status', 'groupIds', 'nominee', 'bankAccount', 'adminId']

    def get_initials(self, obj):
        parts = (obj.name or '').split()
        return ''.join(p[0].upper() for p in parts[:2]) or '?'

    def get_groupIds(self, obj):
        return list(MembershipModels.objects.filter(member_id=obj.member_id).values_list('group_id', flat=True))


# ───────────────────────── Membership ─────────────────────────

class MembershipSerializers(serializers.ModelSerializer):
    groupId = serializers.IntegerField(source='group_id', required=False)
    memberId = serializers.IntegerField(source='member_id', required=False)
    chitNumber = serializers.IntegerField(source='chit_number', required=False)

    class Meta:
        model = MembershipModels
        fields = ['groupId', 'memberId', 'chitNumber']

    def create(self, validated_data):
        return MembershipModels.objects.create(**validated_data)


class GetMembershipSerializers(serializers.ModelSerializer):
    groupId = serializers.IntegerField(source='group_id', read_only=True)
    memberId = serializers.IntegerField(source='member_id', read_only=True)
    chitNumber = serializers.IntegerField(source='chit_number', read_only=True)

    class Meta:
        model = MembershipModels
        fields = ['groupId', 'memberId', 'chitNumber']


# ───────────────────────── Auction ─────────────────────────

class AuctionSerializers(serializers.ModelSerializer):
    groupId = serializers.IntegerField(source='group_id', required=False)
    monthIndex = serializers.IntegerField(source='month_index', required=False)
    scheduledDate = serializers.CharField(source='scheduled_date', required=False, allow_blank=True)
    startTime = serializers.CharField(source='start_time', required=False, allow_blank=True)
    endTime = serializers.CharField(source='end_time', required=False, allow_blank=True)
    startingBid = serializers.FloatField(source='starting_bid', required=False)
    bidIncrement = serializers.FloatField(source='bid_increment', required=False)
    winnerMemberId = serializers.IntegerField(source='winner_member_id', required=False, allow_null=True)
    winningBid = serializers.FloatField(source='winning_bid', required=False, allow_null=True)
    prizeAmount = serializers.FloatField(source='prize_amount', required=False, allow_null=True)
    dividendPerMember = serializers.FloatField(source='dividend_per_member', required=False, allow_null=True)
    finalInstallment = serializers.FloatField(source='final_installment', required=False, allow_null=True)

    class Meta:
        model = AuctionModels
        fields = ['groupId', 'monthIndex', 'label', 'status', 'scheduledDate', 'startTime', 'endTime',
                  'startingBid', 'bidIncrement', 'winnerMemberId', 'winningBid', 'prizeAmount',
                  'commission', 'dividendPerMember', 'finalInstallment', 'confirmed']

    def create(self, validated_data):
        return AuctionModels.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class GetAuctionSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(source='auction_id', read_only=True)
    groupId = serializers.IntegerField(source='group_id', read_only=True)
    monthIndex = serializers.IntegerField(source='month_index', read_only=True)
    scheduledDate = serializers.CharField(source='scheduled_date', read_only=True)
    startTime = serializers.CharField(source='start_time', read_only=True)
    endTime = serializers.CharField(source='end_time', read_only=True)
    startingBid = serializers.FloatField(source='starting_bid', read_only=True)
    bidIncrement = serializers.FloatField(source='bid_increment', read_only=True)
    winnerMemberId = serializers.IntegerField(source='winner_member_id', read_only=True)
    winningBid = serializers.FloatField(source='winning_bid', read_only=True)
    prizeAmount = serializers.FloatField(source='prize_amount', read_only=True)
    dividendPerMember = serializers.FloatField(source='dividend_per_member', read_only=True)
    finalInstallment = serializers.FloatField(source='final_installment', read_only=True)

    class Meta:
        model = AuctionModels
        fields = ['id', 'groupId', 'monthIndex', 'label', 'status', 'scheduledDate', 'startTime', 'endTime',
                  'startingBid', 'bidIncrement', 'winnerMemberId', 'winningBid', 'prizeAmount',
                  'commission', 'dividendPerMember', 'finalInstallment', 'confirmed']


# ───────────────────────── Bid ─────────────────────────

class BidSerializers(serializers.ModelSerializer):
    auctionId = serializers.IntegerField(source='auction_id', required=False)
    memberId = serializers.IntegerField(source='member_id', required=False)
    memberName = serializers.CharField(source='member_name', required=False, allow_blank=True)

    class Meta:
        model = BidModels
        fields = ['auctionId', 'memberId', 'memberName', 'amount', 'time']

    def create(self, validated_data):
        return BidModels.objects.create(**validated_data)


class GetBidSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(source='bid_id', read_only=True)
    auctionId = serializers.IntegerField(source='auction_id', read_only=True)
    memberId = serializers.IntegerField(source='member_id', read_only=True)
    memberName = serializers.CharField(source='member_name', read_only=True)

    class Meta:
        model = BidModels
        fields = ['id', 'auctionId', 'memberId', 'memberName', 'amount', 'time']


# ───────────────────────── Payment ─────────────────────────

class GetPaymentSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(source='payment_id', read_only=True)
    groupId = serializers.IntegerField(source='group_id', read_only=True)
    memberId = serializers.IntegerField(source='member_id', read_only=True)
    monthIndex = serializers.IntegerField(source='month_index', read_only=True)
    dueDate = serializers.CharField(source='due_date', read_only=True)
    paidDate = serializers.CharField(source='paid_date', read_only=True)
    transactionId = serializers.CharField(source='transaction_id', read_only=True)

    class Meta:
        model = PaymentModels
        fields = ['id', 'groupId', 'memberId', 'monthIndex', 'type', 'amount', 'dueDate',
                  'paidDate', 'status', 'method', 'transactionId']


# ───────────────────────── Dividend ─────────────────────────

class GetDividendSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(source='dividend_id', read_only=True)
    groupId = serializers.IntegerField(source='group_id', read_only=True)
    monthIndex = serializers.IntegerField(source='month_index', read_only=True)
    auctionId = serializers.IntegerField(source='auction_id', read_only=True)
    perMember = serializers.FloatField(source='per_member', read_only=True)
    totalPool = serializers.FloatField(source='total_pool', read_only=True)
    eligibleMembers = serializers.IntegerField(source='eligible_members', read_only=True)

    class Meta:
        model = DividendModels
        fields = ['id', 'groupId', 'monthIndex', 'auctionId', 'perMember', 'totalPool', 'eligibleMembers']


# ───────────────────────── Notification ─────────────────────────

class GetNotificationSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(source='notification_id', read_only=True)
    memberId = serializers.IntegerField(source='member_id', read_only=True)
    groupId = serializers.IntegerField(source='group_id', read_only=True)

    class Meta:
        model = NotificationModels
        fields = ['id', 'audience', 'memberId', 'groupId', 'title', 'message', 'type', 'time', 'read']
