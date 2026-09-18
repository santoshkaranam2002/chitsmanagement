from django.urls import path
from .views import *

urlpatterns = [

    ## ── Auth ──
    path("auth_login/", AuthLogin.as_view()),
    path("auth_signup/", AuthSignup.as_view()),

    ## ── Groups ──
    path("group_create/", GroupCreate.as_view()),
    path("group_get/", GroupGet.as_view()),
    path("group_get/<int:group_id>", GroupGet.as_view()),
    path("group_update/<int:group_id>", GroupUpdate.as_view()),
    path("group_delete/<int:group_id>", GroupDelete.as_view()),

    ## ── Members ──
    path("member_create/", MemberCreate.as_view()),
    path("member_get/", MemberGet.as_view()),
    path("member_get/<int:member_id>", MemberGet.as_view()),
    path("member_update/<int:member_id>", MemberUpdate.as_view()),
    path("member_delete/<int:member_id>", MemberDelete.as_view()),
    path("member_assign_group/", MemberAssignGroup.as_view()),
    path("membership_get/", MembershipGet.as_view()),

    ## ── Auctions ──
    path("auction_create/", AuctionCreate.as_view()),
    path("auction_get/", AuctionGet.as_view()),
    path("auction_get/<int:auction_id>", AuctionGet.as_view()),
    path("auction_update/<int:auction_id>", AuctionUpdate.as_view()),
    path("auction_delete/<int:auction_id>", AuctionDelete.as_view()),
    path("auction_open/<int:auction_id>", AuctionOpen.as_view()),
    path("auction_close/<int:auction_id>", AuctionClose.as_view()),
    path("auction_confirm/<int:auction_id>", AuctionConfirm.as_view()),

    ## ── Bids ──
    path("bid_create/", BidCreate.as_view()),
    path("bid_get/", BidGet.as_view()),

    ## ── Payments ──
    path("payment_get/", PaymentGet.as_view()),
    path("payment_mark_paid/<int:payment_id>", PaymentMarkPaid.as_view()),

    ## ── Dividends ──
    path("dividend_get/", DividendGet.as_view()),

    ## ── Notifications ──
    path("notification_get/", NotificationGet.as_view()),
    path("notification_read/<int:notification_id>", NotificationRead.as_view()),
]
