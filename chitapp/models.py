from django.db import models


class UserModels(models.Model):
    """Login account — Admin (chit organizer) or Member. A Member account
    is auto-provisioned when Admin adds them via member_create, so a
    member never signs up themselves; only Admin uses auth_signup."""
    user_id = models.IntegerField(primary_key=True)

    name = models.CharField(max_length=150, blank=True, default="")
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True, default="")
    role = models.CharField(max_length=20, blank=True, default="member")  # admin | member
    password = models.CharField(max_length=100, blank=True, default="")
    org_name = models.CharField(max_length=150, blank=True, default="")
    # set when role == member — links this login to its MemberModels row
    member_id = models.IntegerField(null=True, blank=True, default=None)
    # set when role == admin — every group/member/etc. this admin owns
    # carries this same id as admin_id, so data stays scoped per organization
    admin_id = models.IntegerField(null=True, blank=True, default=None)
    created_date = models.CharField(max_length=30, blank=True, default="")

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.user_id:
            latest = UserModels.objects.order_by('-user_id').first()
            self.user_id = (latest.user_id + 1) if latest else 1
        return super().save(*args, **kwargs)

    class Meta:
        db_table = "user_table"


class ChitGroupModels(models.Model):
    """A chit scheme run by one organizer — e.g. "Santosh Group"."""
    group_id = models.IntegerField(primary_key=True)

    name = models.CharField(max_length=150, blank=True, default="")
    chit_value = models.FloatField(default=0)
    total_members = models.IntegerField(default=0)
    duration_months = models.IntegerField(default=0)
    monthly_installment = models.FloatField(default=0)
    auction_day = models.IntegerField(default=1)
    start_date = models.CharField(max_length=30, blank=True, default="")
    status = models.CharField(max_length=20, blank=True, default="Upcoming")  # Active | Upcoming | Completed
    current_month = models.IntegerField(default=0)
    starting_bid = models.FloatField(default=0)
    min_bid = models.FloatField(default=0)
    max_bid = models.FloatField(default=0)
    bid_increment = models.FloatField(default=0)
    commission_type = models.CharField(max_length=20, blank=True, default="Fixed")  # Fixed | Percent
    commission_value = models.FloatField(default=0)
    foreman = models.CharField(max_length=150, blank=True, default="")
    admin_id = models.IntegerField(default=0)
    created_date = models.CharField(max_length=30, blank=True, default="")

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.group_id:
            latest = ChitGroupModels.objects.order_by('-group_id').first()
            self.group_id = (latest.group_id + 1) if latest else 1
        return super().save(*args, **kwargs)

    class Meta:
        db_table = "group_table"


class MemberModels(models.Model):
    """A chit member's profile — contact/KYC details. Every member also
    gets a UserModels login row (role=member) created alongside this one
    by member_create, so they can sign in and bid."""
    member_id = models.IntegerField(primary_key=True)

    code = models.CharField(max_length=30, blank=True, default="")
    name = models.CharField(max_length=150, blank=True, default="")
    phone = models.CharField(max_length=30, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    address = models.CharField(max_length=250, blank=True, default="")
    nominee = models.CharField(max_length=150, blank=True, default="")
    bank_account = models.CharField(max_length=100, blank=True, default="")
    status = models.CharField(max_length=20, blank=True, default="Active")  # Active|Inactive|Completed|Suspended
    join_date = models.CharField(max_length=30, blank=True, default="")
    admin_id = models.IntegerField(default=0)
    created_date = models.CharField(max_length=30, blank=True, default="")

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.member_id:
            latest = MemberModels.objects.order_by('-member_id').first()
            self.member_id = (latest.member_id + 1) if latest else 1
        if not self.code:
            self.code = f"MEM-{str(self.member_id).zfill(3)}"
        return super().save(*args, **kwargs)

    class Meta:
        db_table = "member_table"


class MembershipModels(models.Model):
    """Junction row: this member holds chit number N in this group."""
    membership_id = models.IntegerField(primary_key=True)

    group_id = models.IntegerField(default=0)
    member_id = models.IntegerField(default=0)
    chit_number = models.IntegerField(default=0)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.membership_id:
            latest = MembershipModels.objects.order_by('-membership_id').first()
            self.membership_id = (latest.membership_id + 1) if latest else 1
        return super().save(*args, **kwargs)

    class Meta:
        db_table = "membership_table"


class AuctionModels(models.Model):
    """One month's chit auction for a group."""
    auction_id = models.IntegerField(primary_key=True)

    group_id = models.IntegerField(default=0)
    month_index = models.IntegerField(default=1)
    label = models.CharField(max_length=60, blank=True, default="")
    # Upcoming | Live | Pending Confirmation | Completed
    status = models.CharField(max_length=30, blank=True, default="Upcoming")
    scheduled_date = models.CharField(max_length=30, blank=True, default="")
    start_time = models.CharField(max_length=20, blank=True, default="")
    end_time = models.CharField(max_length=20, blank=True, default="")
    starting_bid = models.FloatField(default=0)
    bid_increment = models.FloatField(default=0)

    winner_member_id = models.IntegerField(null=True, blank=True, default=None)
    winning_bid = models.FloatField(null=True, blank=True, default=None)
    prize_amount = models.FloatField(null=True, blank=True, default=None)
    commission = models.FloatField(null=True, blank=True, default=None)
    dividend_per_member = models.FloatField(null=True, blank=True, default=None)
    final_installment = models.FloatField(null=True, blank=True, default=None)
    confirmed = models.BooleanField(default=False)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.auction_id:
            latest = AuctionModels.objects.order_by('-auction_id').first()
            self.auction_id = (latest.auction_id + 1) if latest else 1
        return super().save(*args, **kwargs)

    class Meta:
        db_table = "auction_table"


class BidModels(models.Model):
    bid_id = models.IntegerField(primary_key=True)

    auction_id = models.IntegerField(default=0)
    member_id = models.IntegerField(default=0)
    member_name = models.CharField(max_length=150, blank=True, default="")
    amount = models.FloatField(default=0)
    time = models.CharField(max_length=30, blank=True, default="")

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.bid_id:
            latest = BidModels.objects.order_by('-bid_id').first()
            self.bid_id = (latest.bid_id + 1) if latest else 1
        return super().save(*args, **kwargs)

    class Meta:
        db_table = "bid_table"


class PaymentModels(models.Model):
    payment_id = models.IntegerField(primary_key=True)

    group_id = models.IntegerField(default=0)
    member_id = models.IntegerField(default=0)
    month_index = models.IntegerField(default=0)
    type = models.CharField(max_length=20, blank=True, default="Installment")  # Installment | Winner Payout
    amount = models.FloatField(default=0)
    due_date = models.CharField(max_length=30, blank=True, default="")
    paid_date = models.CharField(max_length=30, blank=True, default="")
    status = models.CharField(max_length=20, blank=True, default="Pending")  # Paid|Pending|Partial|Overdue
    method = models.CharField(max_length=30, blank=True, default="")
    transaction_id = models.CharField(max_length=60, blank=True, default="")

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.payment_id:
            latest = PaymentModels.objects.order_by('-payment_id').first()
            self.payment_id = (latest.payment_id + 1) if latest else 1
        return super().save(*args, **kwargs)

    class Meta:
        db_table = "payment_table"


class DividendModels(models.Model):
    dividend_id = models.IntegerField(primary_key=True)

    group_id = models.IntegerField(default=0)
    month_index = models.IntegerField(default=0)
    auction_id = models.IntegerField(default=0)
    per_member = models.FloatField(default=0)
    total_pool = models.FloatField(default=0)
    eligible_members = models.IntegerField(default=0)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.dividend_id:
            latest = DividendModels.objects.order_by('-dividend_id').first()
            self.dividend_id = (latest.dividend_id + 1) if latest else 1
        return super().save(*args, **kwargs)

    class Meta:
        db_table = "dividend_table"


class NotificationModels(models.Model):
    notification_id = models.IntegerField(primary_key=True)

    audience = models.CharField(max_length=20, blank=True, default="admin")  # admin | member
    member_id = models.IntegerField(null=True, blank=True, default=None)
    group_id = models.IntegerField(null=True, blank=True, default=None)
    admin_id = models.IntegerField(default=0)
    title = models.CharField(max_length=200, blank=True, default="")
    message = models.CharField(max_length=400, blank=True, default="")
    type = models.CharField(max_length=20, blank=True, default="system")  # auction|payment|dividend|result|system
    time = models.CharField(max_length=30, blank=True, default="")
    read = models.BooleanField(default=False)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.notification_id:
            latest = NotificationModels.objects.order_by('-notification_id').first()
            self.notification_id = (latest.notification_id + 1) if latest else 1
        return super().save(*args, **kwargs)

    class Meta:
        db_table = "notification_table"
