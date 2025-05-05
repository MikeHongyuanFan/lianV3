from django.contrib import admin
from .models import Application, Document, Fee, Repayment, FundingCalculationHistory

# Register your models here.
admin.site.register(Application)
admin.site.register(Document)
admin.site.register(Fee)
admin.site.register(Repayment)
admin.site.register(FundingCalculationHistory)
