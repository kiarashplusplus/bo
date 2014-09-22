
from django.contrib import admin
from models import *

class NewsAdmin(admin.ModelAdmin):
	fields = ('title','description','published_date','agency', 'link_to_news', 'country','url')

admin.site.register(News,NewsAdmin)
admin.site.register(Country)
admin.site.register(Url)
admin.site.register(ReportDecision)