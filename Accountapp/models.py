# accounting_app/models.py
from django.db import models


class Head(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Shead(models.Model):
    head = models.ForeignKey(Head, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Sub Head"
        verbose_name_plural = "Sub Heads"

    def __str__(self):
        return self.name


class charge(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Charge To"
        verbose_name_plural = "Charge To"

    def __str__(self):
        return self.name


class claim(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Claim By"
        verbose_name_plural = "Claim By"

    def __str__(self):
        return self.name


class paid(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Paid By"
        verbose_name_plural = "Paid By"

    def __str__(self):
        return self.name


class Vendor(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class AccountingEntry(models.Model):
    date = models.DateField(auto_now_add=True)
    Do = models.CharField(max_length=20,null=True, blank=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    
    head = models.ForeignKey(Head, on_delete=models.CASCADE)
    sub_head = models.ForeignKey(Shead, on_delete=models.CASCADE)
    # sub_head = models.CharField(max_length=50)
    description = models.TextField()
    receipt_number = models.CharField(max_length=20)
    charge_by = models.ForeignKey(
        charge, on_delete=models.CASCADE, null=True, blank=True
    )
    voucher = models.CharField(max_length=50, null=True, blank=True, unique=True)
    paid_by = models.ForeignKey(paid, on_delete=models.CASCADE, null=True, blank=True)
    claim_by = models.ForeignKey(claim, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.voucher and not self.pk:
            last_voucher = AccountingEntry.objects.all().order_by("-id").first()
            last_number = (
                int(last_voucher.voucher.split("-")[-1]) if last_voucher else 0
            )
            new_number = last_number + 1
            self.voucher = f"{self.charge_by}-{new_number}"

        super(AccountingEntry, self).save(*args, **kwargs)

    # New fields for instrument
    instrument = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        choices=[("cash", "Cash"), ("cheque", "Cheque"), ("online", "Online Transfer"),("card","Card")],
    )
    cash_number = models.CharField(max_length=20, default=0, null=True, blank=True)
    cheque_number = models.CharField(max_length=20, default=0, null=True, blank=True)
    online_number = models.CharField(max_length=20, default=0, null=True, blank=True)
    card_number = models.CharField(max_length=4, default=0, null=True, blank=True)
    vendors = models.ForeignKey(Vendor, null=True, blank=True, on_delete=models.CASCADE)

    attachments = models.FileField(upload_to="attachments/", null=True, blank=True)

    comments = models.TextField()

    def __str__(self):
        return f"{self.date} - {self.head} - {self.amount}"
