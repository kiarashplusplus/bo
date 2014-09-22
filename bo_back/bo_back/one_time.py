from bo_report.models import *
from bo_report.views import *
#from bo_back.one_time import *
from django.db.models import F

from django.core.cache import cache

#cache.clear()

def runReportDecision():
	offset = 0
	pagesize = 100000
	co = UrlReport.objects.count()
	print co
	while offset < co:
		print offset, co
		for r in UrlReport.objects.select_related('ipidentity','uid').all()[offset : offset + pagesize].iterator():
			if  r.ipidentity.country and r.uid.chosen_country and r.ipidentity.country.id == r.uid.chosen_country.id:
				new_dec= decide_one_report(r)
				dec, _ = ReportDecision.objects.get_or_create(report=r)
				dec.decision = new_dec
				dec.flag = (new_dec==32) or (new_dec==31)
				dec.save()
		offset += pagesize

def runMakeDecision():
	i=0
	for u in Url.objects.all().exclude(group__gte=10):
		print i, u.address
		i+=1
		x = UrlReport.objects.filter(url = u, ipidentity__country=F('uid__chosen_country')).values('ipidentity__country__id', 'uid__client').distinct()
		for cname in x:
			c = Country.objects.get(id= cname['ipidentity__country__id'])
			makeDecision(u, c, cname['uid__client']=='proxy')

def SLOWrunMakeDecision(offset = 0):
	flagSet = set()
	pagesize = 100000
	i=0
	co = ReportDecision.objects.count()
	print co
	while offset < co:
		print offset, co
		for rd in ReportDecision.objects.select_related().all()[offset : offset + pagesize].iterator():
			i= i+1
			if (rd.report.ipidentity.country.id, rd.report.url.id, rd.report.uid.client=='proxy') not in flagSet:
				flagSet.add( (rd.report.ipidentity.country.id, rd.report.url.id, rd.report.uid.client=='proxy') )
				print "making decision", i, len(flagSet)
				if rd.report.uid.client=='proxy':
					makeDecision(rd.report.url, rd.report.ipidentity.country, True)
				else:
					makeDecision(rd.report.url, rd.report.ipidentity.country, False)
		offset += pagesize

from django.core.mail import send_mail
from time import time
from datetime import datetime
from django.db.models import Count

def sendSummary():
	ss = str(UrlDecision.objects.values('decision').annotate(Count('decision')))
	summary = "DateTime: {0}\ntotal flagged: {1}\ntotal decision: {2}\nsummary: {3}\n,active urls: {4}\n".format(str(datetime.now()), 
			ReportDecision.objects.filter(flag=1).count(), UrlDecision.objects.count(), ss,
			Url.objects.all().exclude(group__gte=5).count())
	send_mail('Summary', summary, 'inquiry@blockedonline.com',
   			 ['inquiry@blockedonline.com'], fail_silently=True)
			
def urlCleanUp(offset = 604800):
	sendSummary()
	sevenDaysAgo = int(time()) - offset
	i=0
	for u in Url.objects.all():
		print i
		i = i+1
		all_reports = ReportDecision.objects.filter(report__url=u, report__epoch__gte=sevenDaysAgo).select_related().values('decision')
		decisions = map(lambda d: d['decision'], all_reports)	
		if len(decisions) < 10:
			continue
		threshold = 0.7*len(decisions)
		if decisions.count(32) + decisions.count(11) > threshold: #if (redirected or down) most of the time
			UrlDecision.objects.filter(url = u).delete()
			ReportDecision.objects.filter(report__url = u).update(flag=0) #remove all the flags associatede with it
			u.group = 100
			u.save()
		elif decisions.count(31) > threshold: #elif small most of the time
			UrlDecision.objects.filter(url = u).delete()
			ReportDecision.objects.filter(report__url = u).update(flag=0) #remove all the flags associatede with it
			u.group = 102
			u.save()		
			#send_mail('URL BLOCKED EVERYWHERE', str(u.address)+"\t"+str(u.id), 'inquiry@blockedonline.com',
   			# ['inquiry@blockedonline.com'], fail_silently=True)
	sendSummary()

def delete_one_url(url_id):
	u =Url.objects.get(id=url_id)
	print u.address
	UrlDecision.objects.filter(url = u).delete()
	ReportDecision.objects.filter(report__url = u).update(flag=0)
	u.group = 101
	u.save()


def delete_one_uid(uid):
	RUID = ReporterUID.objects.get(uid=uid)
	c= RUID.chosen_country
	UrlDecision.objects.filter(country=c).delete()
	ReportDecision.objects.filter(report__uid = RUID).delete()
	i=0
	for u in Url.objects.all().exclude(group__gte=10):
		print i, u.address
		i+=1
		x = ReportDecision.objects.filter(report__url = u, report__uid__chosen_country=c, report__ipidentity__country=F('report__uid__chosen_country')).values('report__uid__client').distinct()
		for cname in x:
			makeDecision(u, c, cname['report__uid__client']=='proxy')


def processIRANagain():
	c = Country.objects.get(alpha2='IR')
	for rd in ReportDecision.objects.filter(report__uid__chosen_country = c, report__length__lte=1000, report__status_code=403):
		new_dec= decide_one_report(rd.report)
		rd.decision = new_dec
		rd.save()

	i=0
	for u in Url.objects.all().exclude(group__gte=10):
		print i, u.address
		i+=1
		x = ReportDecision.objects.filter(report__url = u, report__uid__chosen_country=c, report__ipidentity__country=F('report__uid__chosen_country')).values('report__uid__client').distinct()
		for cname in x:
			makeDecision(u, c, cname['report__uid__client']=='proxy')
