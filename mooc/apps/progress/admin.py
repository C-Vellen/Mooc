from django.contrib import admin
from .models import TutoProgress, PageProgress, QuestionProgress, PropositionProgress

admin.site.register(TutoProgress)
admin.site.register(PageProgress)
admin.site.register(QuestionProgress)
admin.site.register(PropositionProgress)

