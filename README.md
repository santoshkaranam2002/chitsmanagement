# ChitFlow Backend

Django REST API for the ChitFlow digital chit fund & online auction platform,
using MongoDB (via Djongo) — matching the same stack and code conventions as
your other backends (estatecraft-backend, hostelmanagement, laptoservices,
spamanagement).

## Setup

1. Make sure MongoDB is running locally (the same server your other
   projects already use):
   ```
   mongodb://localhost:27017
   ```
   The app connects to a database named `chitflow` — created automatically
   on first write, no manual setup needed.

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # macOS / Linux
   pip install -r requirements.txt
   ```

3. Run migrations (Djongo maps these onto MongoDB collections):
   ```bash
   python manage.py makemigrations chitapp
   python manage.py migrate
   ```

4. Start the server:
   ```bash
   python manage.py runserver
   ```
   - Swagger / API docs: http://127.0.0.1:8000/
   - API base: http://127.0.0.1:8000/api/

The Angular frontend (`chitflow-angular`) already points at
`http://127.0.0.1:8000/api` by default — see `src/app/services/chit-api.ts`
if you need to change that.

## First login

There's no seed data and no Django admin data — the app is meant to be used
end-to-end from the UI:

1. Open the Angular app and go to **Register** → this creates your first
   Admin/organizer account (`auth_signup`).
2. Sign in as that Admin, create a Chit Group, then use **Add Member** to
   add members — each one automatically gets a login too (shown once in a
   confirmation dialog: email + a temporary password, default
   `Member@123` unless you set one).
3. Members log in from the same Login screen using the **Member** toggle.

## App structure

Mirrors the Estatecraft backend's conventions exactly:

```
chitapp/
  models.py            — every table (Mongo collection), integer auto-increment PKs
  serializers.py        — write serializers + "Get" (read) serializers per model
  helpers.py              — notify() / date helpers shared by the crud modules
  views.py                 — aggregates every view class for urls.py
  urls.py                    — one path per endpoint
  auth_crud/                  — login, signup
  group_crud/                   — chit group CRUD
  member_crud/                    — member CRUD, group assignment, membership listing
  auction_crud/                     — auction CRUD + open/close/confirm lifecycle
  bid_crud/                           — place bid, list bids
  payment_crud/                         — list payments, mark paid
  dividend_crud/                          — list dividends
  notification_crud/                        — list notifications, mark read
```

Every endpoint replies with the same envelope:
```json
{ "Message": "Successfull" | "Fail", "Status": 200 | 400, "Result": ... }
```

## The auction lifecycle (the core business logic)

1. **Schedule** — Admin creates an auction for a group/month (`auction_create`).
2. **Open** — Admin opens it (`auction_open`): status → Live, members get notified.
3. **Bid** — members place bids (`bid_create`), validated against the group's
   minimum increment.
4. **Close** — Admin closes it (`auction_close`): picks the highest bid as
   winner and computes the full settlement:
   ```
   prizeAmount  = chitValue − winningBid
   commission   = group's fixed value, or round(winningBid × pct/100)
   pool         = winningBid − commission
   dividend     = round(pool / totalMembers)
   finalPayable = monthlyInstallment − dividend
   ```
   Status → Pending Confirmation. Nothing is written to Payments/Dividends yet.
5. **Confirm** — Admin reviews and confirms (`auction_confirm`): generates one
   Installment payment per member (winner still pays the full monthly
   installment; everyone else pays the reduced `finalInstallment`), one
   Winner Payout payment (already marked Paid), one Dividend record, and
   result notifications to every member. Status → Completed.

## Notes

- Every endpoint uses `AllowAny` permissions and plain-text password
  checks — this matches the reference project's demo-grade auth model.
  Don't deploy this as-is to a public server without adding real
  authentication (tokens/JWT) and hashed passwords first.
- Data is scoped per organizer via `adminId` query params the frontend
  sends on every list request — not a hard security boundary, just enough
  to keep one admin's groups from showing up for another in this demo.
