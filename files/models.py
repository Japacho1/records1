from django.db import models
from datetime import date
import os
from simple_history.models import HistoricalRecords
from django.utils import timezone
from decimal import Decimal


# ---------------------------
# Step 1: Lookup Models First
# ---------------------------

class TenantType(models.Model):
    code = models.CharField(max_length=20, unique=True)  # e.g., 'office'
    label = models.CharField(max_length=100)
    history = HistoricalRecords()
    # e.g., 'Office Tenant'

    def __str__(self):
        return self.label


class DocumentType(models.Model):
    code = models.CharField(max_length=20, unique=True)  # e.g., 'kra'
    label = models.CharField(max_length=100)
    history = HistoricalRecords()
    # e.g., 'KRA Certificate'

    def __str__(self):
        return self.label


# ---------------------------
# Step 2: Main Models
# ---------------------------

class Tenant(models.Model):
    name = models.CharField(max_length=255)

    # Optional email
    email = models.EmailField(null=True, blank=True)

    # Old field (keep temporarily for migration)
    tenant_type = models.CharField(max_length=10, null=True, blank=True)

    # New dynamic ForeignKey field
    tenant_type_fk = models.ForeignKey(
        TenantType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # ✅ New fields
    commencement_date = models.DateField(
        null=True,
        blank=True,
        help_text="Rent commencement date"
    )
    escalation_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Escalation rate in % (e.g., 5.00 for 5%)"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    # ✅ NEW: total size properties
    @property
    def total_size_sqm(self):
        return sum((unit.size_sqm or Decimal('0.00')) for unit in self.units.all())

    @property
    def total_size_sqft(self):
        return sum((unit.size_sqft or Decimal('0.00')) for unit in self.units.all())




# ✅ NEW: Unit model
class Unit(models.Model):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="units"
    )
    unit_id = models.CharField(max_length=50)  # e.g., "A1", "B3"

    # Users can fill in either sqm or sqft
    size_sqm = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True,
        help_text="Size in square metres"
    )
    size_sqft = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True,
        help_text="Size in square feet"
    )

    def save(self, *args, **kwargs):
        """
        Ensure both sqm and sqft are always calculated.
        User can enter either sqm or sqft, and we auto-fill the other.
        """
        if self.size_sqm and not self.size_sqft:
            # Convert sqm → sqft
            self.size_sqft = round(float(self.size_sqm) * 10.7639, 2)
        elif self.size_sqft and not self.size_sqm:
            # Convert sqft → sqm
            self.size_sqm = round(float(self.size_sqft) / 10.7639, 2)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.unit_id} ({self.size_sqm} sqm / {self.size_sqft} sqft)"



class ExpiryRule(models.Model):
    tenant_type = models.ForeignKey(TenantType, on_delete=models.CASCADE)
    doc_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    days_valid = models.PositiveIntegerField(
        help_text="Number of days this document is valid for"
    )

    def __str__(self):
        return f"{self.tenant_type} - {self.doc_type}: {self.days_valid} days"


class TenantExpiryRule(models.Model):
    tenant = models.ForeignKey("Tenant", on_delete=models.CASCADE)
    doc_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    days_valid = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.tenant.name} - {self.doc_type}: {self.days_valid} days"


from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

class Document(models.Model):
    tenant = models.ForeignKey(
        'Tenant',
        on_delete=models.CASCADE,
        related_name='documents'
    )
    doc_type_fk = models.ForeignKey(
        'DocumentType',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    file = models.FileField(upload_to='documents/')
    upload_date = models.DateField(auto_now_add=True)
    commencement_date = models.DateField(null=True, blank=True, default=None)
    expiry_date = models.DateField(null=True, blank=True)
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        """
        Automatically calculate expiry date.
        Priority:
        1. Tenant-specific rule
        2. Tenant type rule
        3. None (expiry left blank)
        """
        if self.commencement_date and self.doc_type_fk:
            expiry_days = None

            # Step 1: Check tenant-specific rule
            try:
                tenant_rule = TenantExpiryRule.objects.get(
                    tenant=self.tenant,
                    doc_type=self.doc_type_fk
                )
                expiry_days = tenant_rule.days_valid
            except TenantExpiryRule.DoesNotExist:
                # Step 2: Fallback to tenant type rule
                if self.tenant.tenant_type_fk:
                    try:
                        type_rule = ExpiryRule.objects.get(
                            tenant_type=self.tenant.tenant_type_fk,
                            doc_type=self.doc_type_fk
                        )
                        expiry_days = type_rule.days_valid
                    except ExpiryRule.DoesNotExist:
                        expiry_days = None

            # Step 3: Apply expiry days if found
            if expiry_days is not None:
                self.expiry_date = self.commencement_date + timezone.timedelta(days=expiry_days)
            else:
                self.expiry_date = None

        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        """
        Returns True if the document is expired, False otherwise.
        """
        if self.expiry_date:
            return self.expiry_date < timezone.now().date()
        return False

    def __str__(self):
        return f"{self.tenant} - {self.doc_type_fk} ({self.upload_date})"


class EmailReminderLog(models.Model):
    tenant = models.ForeignKey('Tenant', on_delete=models.CASCADE)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    sent_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=10,
        choices=[('Success', 'Success'), ('Failed', 'Failed')]
    )
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reminder to {self.tenant.name} at {self.sent_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
class ArchivedDocument(models.Model):
    tenant_name = models.CharField(max_length=255)
    tenant_type = models.CharField(max_length=100, null=True, blank=True)  # ✅ NEW
    doc_type = models.CharField(max_length=100)
    file = models.FileField(upload_to='archives/')
    upload_date = models.DateField()
    commencement_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    archived_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Archived: {self.tenant_name} - {self.doc_type}"

