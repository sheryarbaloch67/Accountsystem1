from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import AccountingEntry, Head, charge, paid, claim, Vendor, Shead
from django.http import HttpResponse, HttpResponseNotFound
from datetime import datetime, date
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    PasswordChangeForm,
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import JsonResponse
import inflect
from collections import Counter


# Create your views here.


def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Log in the user
            user = form.get_user()
            login(request, user)
            return redirect(
                "submitfile"
            )  # Replace 'dashboard' with the appropriate URL
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


@login_required(login_url="signin")
def signout(request):
    logout(request)
    return redirect("signin")  # Replace 'signin' with the appropriate URL


@login_required(login_url="signin")
def home(request):
    data = AccountingEntry.objects.all()
    heads = Head.objects.all()
    charges = charge.objects.all()
    paids = paid.objects.all()
    claims = claim.objects.all()
    vendors = Vendor.objects.all()
    subheads = Shead.objects.all()
    today = date.today()

    # ndate=str(today)+"-"+str(1)
    return render(request, "file.html", locals())


@login_required(login_url="signin")
def accounting_form(request):
    if request.method == "POST":
        head_id = request.POST.get("head")
        # date = request.POST['date']
        amount = request.POST["amount"]
        sub_head = request.POST["subHead"]
        description = request.POST["description"]
        receipt_number = request.POST.get("receiptNumber")
        charge_by = request.POST["chargeBy"]
        # voucher = request.POST['Voucher']
        paid_by = request.POST["paidBy"]
        claim_by = request.POST["claimBy"]
        comments = request.POST["comments"]

        instrument = request.POST["instrument"]
        cash_number = request.POST.get("cashNumber", None)
        cheque_number = request.POST.get("chequeNumber", None)
        online_number = request.POST.get("onlineNumber", None)
        card_number = request.POST.get("cardNumber", None)

        user = request.user
        user = str(user)

        vendors_ids = request.POST["vendors"]

        today = date.today()
        today2 = str(today).split("-")
        today2 = today2[0] + today2[1] + today2[2]

        data = AccountingEntry.objects.filter(date=today)
        count = 0
        if instrument == "cash" or instrument == "Cash":
            for i in data:
                if i.instrument == "cash" or i.instrument == "Cash":
                    count = count + 1
            count = count + 1

            count = str(today2) + "-" + str(count)

        # Handle file uploads
        attachments = request.FILES.get("attachments", None)

        amount = str(amount)

        # Check if the values are not empty before converting to integers
        if head_id:
            head = Head.objects.get(id=int(head_id))
        else:
            # Handle the case where head_id is empty
            head = None
        if sub_head:
            sub_head = Shead.objects.get(id=int(sub_head))
        else:
            # Handle the case where head_id is empty
            sub_head = None

        if vendors_ids:
            if not Vendor.objects.filter(name=vendors_ids).exists():
                newobject = Vendor.objects.create(
                    name=vendors_ids,
                )

                newobject.save()
                vendors_ids = Vendor.objects.get(name=vendors_ids)
            else:
                vendors_ids = Vendor.objects.get(name=vendors_ids)
        else:
            # Handle the case where head_id is empty
            pass

        if charge_by:
            charge_by_obj = charge.objects.get(id=int(charge_by))
            # voucher = str(charge_by_obj) + "-" + str(voucher)
        else:
            # Handle the case where charge_by is empty
            charge_by_obj = None

        if paid_by:
            paid_by_obj = paid.objects.get(id=int(paid_by))
        else:
            # Handle the case where paid_by is empty
            paid_by_obj = None

        if claim_by:
            claim_by_obj = claim.objects.get(id=int(claim_by))
        else:
            # Handle the case where claim_by is empty
            claim_by_obj = None

        # Create a new AccountingEntry object and save it to the database
        new_entry = AccountingEntry.objects.create(
            # date=date,
            amount=amount,
            head=head,
            sub_head=sub_head,
            description=description,
            receipt_number=receipt_number,
            charge_by=charge_by_obj,
            # voucher=voucher,
            paid_by=paid_by_obj,
            claim_by=claim_by_obj,
            comments=comments,
            vendors=vendors_ids,
            instrument=instrument,
            cash_number=count,
            cheque_number=cheque_number,
            online_number=online_number,
            card_number=card_number,
            attachments=attachments,
            Do=user,
        )
        new_entry.save()

        return redirect("submitfile")

    return render(request, "submit.html")


@login_required(login_url="signin")
def edit(request, id):
    data = AccountingEntry.objects.get(id=id)
    heads = Head.objects.all()
    subheads = Shead.objects.all()
    charges = charge.objects.all()
    Paid = paid.objects.all()
    claims = claim.objects.all()
    vendors = Vendor.objects.all()

    return render(request, "editfile.html", locals())


@login_required(login_url="signin")
def printer(request, id):
    data = AccountingEntry.objects.get(id=id)
    p = inflect.engine()
    instruments = str(data.instrument).title()
    amount_in_words = p.number_to_words(int(data.amount)).title() + " Rupees"
    if (
        str(data.charge_by) == "xabta"
        or str(data.charge_by) == "Xabta"
        or str(data.charge_by) == "XABTA"
    ):
        logo = "xabta"
    elif (
        str(data.charge_by) == "bt"
        or str(data.charge_by) == "Bt"
        or str(data.charge_by) == "BT"
    ):
        logo = "bt"

    return render(request, "print.html", locals())


@login_required(login_url="signin")
def deleterecord(request, id):
    data = AccountingEntry.objects.get(id=id)
    data.delete()

    return redirect("submitfile")


@login_required(login_url="signin")
def ufile(request):
    if request.method == "POST":
        entry_id = request.POST.get("userid")
        entry = AccountingEntry.objects.get(id=entry_id)
        vocher = entry.voucher
        vocher = str(vocher.split("-")[1])
        vocher = f"{entry.charge_by}-{vocher}"

        # Check if entry_id is not empty
        if entry_id:
            try:
                entry = AccountingEntry.objects.get(id=entry_id)
            except AccountingEntry.DoesNotExist:
                # Handle the case where the entry with the provided ID doesn't exist
                return HttpResponseNotFound("Entry not found")

            entry.amount = request.POST["amount"]
            entry.head = Head.objects.get(id=int(request.POST["head"]))
            entry.sub_head = Shead.objects.get(id=int(request.POST["subHead"]))
            entry.description = request.POST.get("description")
            entry.receipt_number = request.POST.get("receiptNumber")
            entry.charge_by = charge.objects.get(id=int(request.POST.get("chargeBy")))
            # entry.voucher = str(entry.charge_by) + "-" + str(request.POST['Voucher'])
            entry.paid_by = paid.objects.get(id=int(request.POST.get("paidBy")))
            vendors_ids = request.POST.get("vendors")
            entry.claim_by = claim.objects.get(id=int(request.POST.get("claimBy")))
            entry.comments = request.POST.get("comments")
            vocher = entry.voucher
            vocher = str(vocher.split("-")[1])
            vocher = f"{entry.charge_by}-{vocher}"
            entry.voucher = vocher

            vendors_ids = request.POST["vendors"]

            if vendors_ids:
                if not Vendor.objects.filter(name=vendors_ids).exists():
                    newobject = Vendor.objects.create(
                        name=vendors_ids,
                    )
                    newobject.save()
                    vendors_ids = Vendor.objects.get(name=vendors_ids)
                else:
                    vendors_ids = Vendor.objects.get(name=vendors_ids)

            entry.vendors = vendors_ids

            iscash = entry.instrument
            entry.instrument = request.POST.get("instrument")
            entry.cheque_number = request.POST.get("chequeNumber")
            entry.online_number = request.POST.get("onlineNumber")
            entry.card_number = request.POST.get("cardNumber")

            today = date.today()
            today2 = str(today).split("-")
            today2 = today2[0] + today2[1] + today2[2]

            count = 0
            if str(iscash) != "cash":
                data = AccountingEntry.objects.filter(date=today)
                if entry.instrument == "cash" or entry.instrument == "Cash":
                    count = 0
                    for i in data:
                        if i.instrument == "cash" or i.instrument == "Cash":
                            count = count + 1
                count = count + 1

                count = str(today2) + "-" + str(count)
                entry.cash_number = count

            if "attachments" in request.FILES:
                entry.attachments = request.FILES["attachments"]
            else:
                current_attachment_url = request.POST.get("current_attachment")
                entry.attachments = current_attachment_url

            # Other fields...

            entry.save()

            return redirect("submitfile")

    return render(request, "submit.html")


@login_required(login_url="signin")
def get_subheads(request):
    head_id = request.GET.get("head_id")
    if head_id:
        subheads = Shead.objects.filter(head__id=head_id).values("id", "name")
        return JsonResponse(list(subheads), safe=False)
    else:
        return JsonResponse([], safe=False)


@login_required(login_url="signin")
def summary(request, selected_date):
    selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()

    today = selected_date
    ndate = str(today)
    ndate = ndate.split("-")
    ndate = ndate[0] + ndate[1] + ndate[2]
    date_object = datetime.strptime(ndate, "%Y%m%d")
    formatted_date = date_object.strftime("%Y%b%d").title()

    todayentry = AccountingEntry.objects.filter(date=today)
    amount = 0
    cash = 0
    cheque = 0
    online = 0
    card = 0
    xcount = 0
    bcount = 0
    item_counts = Counter()
    for i in todayentry:
        amount = amount + i.amount
        if i.instrument == "cash":
            cash = cash + 1
        elif i.instrument == "cheque":
            cheque = cheque + 1
        elif i.instrument == "card":
            card = card + 1
        else:
            online = online + 1

    for j in todayentry:
        if (
            str(j.charge_by) == "xabta"
            or str(j.charge_by) == "Xabta"
            or str(j.charge_by) == "XABTA"
        ):
            xcount = xcount + 1
        elif (
            str(j.charge_by) == "bt"
            or str(j.charge_by) == "Bt"
            or str(j.charge_by) == "BT"
        ):
            bcount = bcount + 1

    for k in todayentry:
        # Count items for the item_counts dictionary
        item_counts[k.head.name] += 1

    if xcount != 0 and bcount != 0:
        logo = "showboth"
    elif xcount != 0 and bcount == 0:
        logo = "showxabta"
    elif xcount == 0 and bcount != 0:
        logo = "showbt"

    p = inflect.engine()
    amount_in_words = p.number_to_words(int(amount)).title() + " Rupees"

    # Convert item_counts to a dictionary for use in the template
    item_counts_dict = dict(item_counts)

    return render(request, "summary.html", locals())


@login_required(login_url="signin")
def tsummary(request):
    today = date.today()
    todayentry = AccountingEntry.objects.filter(date=today)

    return render(request, "summarytable.html", locals())


@login_required(login_url="signin")
def showresult(request):
    admin = request.user.is_staff
    accounting_form = AccountingEntry.objects.all().order_by("-id")
    # for i in accounting_form:
    #     print(i.date)
    # print(accounting_form)
    today = date.today()
    # formatted_date = today.strftime("%b. %d, %Y")
    # print(today)
    return render(request, "submit.html", locals())
