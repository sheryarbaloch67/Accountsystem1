from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import AccountingEntry,Head,charge,paid,claim,Vendor,Shead
from django.http import HttpResponse, HttpResponseNotFound
from datetime import datetime, date

# Create your views here.


def home(request):
     heads = Head.objects.all()
     charges =charge.objects.all()
     paids = paid.objects.all()
     claims= claim.objects.all()
     vendors=Vendor.objects.all()
     subheads=Shead.objects.all()
     today = date.today()
     return render(request,"file.html",locals())
 
def accounting_form(request):
    if request.method == 'POST':
        head_id = request.POST.get('head')
        # date = request.POST['date']
        amount = request.POST['amount']
        sub_head = request.POST['subHead']
        description = request.POST['description']
        receipt_number = request.POST['receiptNumber']
        charge_by = request.POST['chargeBy']
        # voucher = request.POST['Voucher']
        paid_by = request.POST['paidBy']
        claim_by = request.POST['claimBy']
        comments = request.POST['comments']

        instrument = request.POST['instrument']
        cash_number = request.POST.get('cashNumber', None)
        cheque_number = request.POST.get('chequeNumber', None)
        online_number = request.POST.get('onlineNumber', None)

        vendors_ids = request.POST['vendors']

        # Handle file uploads
        attachments = request.FILES.get('attachments', None)

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
            vendors_ids=Vendor.objects.get(name=vendors_ids)
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
            cash_number=cash_number,
            cheque_number=cheque_number,
            online_number=online_number,
            attachments=attachments
        )
        new_entry.save()

        return redirect("submitfile")

    return render(request, 'submit.html')


def edit(request,id):
    data=AccountingEntry.objects.get(id=id)
    heads = Head.objects.all()
    charges =charge.objects.all()
    Paids = paid.objects.all()
    claims= claim.objects.all()
    vendors=Vendor.objects.all()

    return render(request,"editfile.html",locals())


def ufile(request):
    if request.method == 'POST':
        entry_id = request.POST.get('userid')

        # Check if entry_id is not empty
        if entry_id:
            try:
                entry = AccountingEntry.objects.get(id=entry_id)
            except AccountingEntry.DoesNotExist:
                # Handle the case where the entry with the provided ID doesn't exist
                return HttpResponseNotFound("Entry not found")

            entry.amount = request.POST['amount']
            entry.head = Head.objects.get(id=int(request.POST['head']))
            entry.sub_head = request.POST['subHead']
            entry.description = request.POST['description']
            entry.receipt_number = request.POST['receiptNumber']
            entry.charge_by = charge.objects.get(id=int(request.POST['chargeBy']))
            # entry.voucher = str(entry.charge_by) + "-" + str(request.POST['Voucher'])
            entry.paid_by = paid.objects.get(id=int(request.POST['paidBy']))
            entry.claim_by = claim.objects.get(id=int(request.POST['claimBy']))
            entry.comments = request.POST['comments']

            # Handle file uploads
            entry.attachments = request.FILES.get('attachments', None)

            # Other fields...

            entry.save()

            return redirect("submitfile")

    return render(request, 'submit.html')






def showresult(request):
    accounting_form=AccountingEntry.objects.all()
    for i in accounting_form:
        print(i.date)
    print(accounting_form)
    today = date.today()
    # formatted_date = today.strftime("%b. %d, %Y")
    # print(today)
    return render(request,"submit.html",locals())


