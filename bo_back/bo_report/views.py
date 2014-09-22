import tldextract
from django.shortcuts import redirect
from time import time
import lxml.html as lh

from models import *
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from ipware.ip import get_real_ip, get_ip
import requests
import json
import re
import logging
from random import shuffle
import datetime
from bs4 import BeautifulSoup as bs
import traceback
from django.views.generic import TemplateView, FormView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

log = logging.getLogger('bo_report')
# logging.addLevelName(logging.INFO, 'info')
# log.setLevel(logging.INFO)

# logglyhandler = hoover.LogglyHttpHandler(token='8cf26149-794b-479e-8826-253e5935b8e6')
# logglyhandler.setLevel(logging.WARNING)
# logglyformatter = logging.Formatter('{"time": "%(asctime)s", "level":"%(levelname)s",' \
#  '"error_number": "%(error_number)s", "message":"%(message)s", "other":"%(other)s"}' ) 
# logglyhandler.setFormatter(logglyformatter)
# log.addHandler(logglyhandler)

class HttpResponseBadRequest(HttpResponse):
    status_code = 400

@csrf_exempt
def news(request):
	log.debug(request)
	if request.method == 'POST': 
		try:
			data = request.POST
			title = data['title']
			agency = data['agency']
			description = data['description']
			link_to_news = data['link_to_news']			
			try:
				country=Country.objects.get(name=data['country'])
			except:
				try:
					country=Country.objects.get(alpha2=data['country'])
				except Exception as e:
					log.warning(str(e) + str(data['country']))
					country=None

			try:
				url = Url.objects.get(address=data["url"])
			except:
				url = None
			try:
				published_date = datetime.datetime.strptime(data['date_published'], '%m/%d/%Y').date()
				#log.debug(str(type(published_date))+str(published_date))
			except Exception as e:
				log.debug(e)
				published_date = None

		except Exception as e:
			log.error(e)
			return HttpResponseBadRequest(e)
		try:
			News.objects.create(link_to_news=link_to_news, title=title, agency=agency, description= description, url=url, country=country, published_date=published_date)
		except Exception as e:
			log.error(e)
			return HttpResponseBadRequest("bad link to news.")	
		return HttpResponse()
	else:
		return HttpResponseBadRequest()		


def makeIPidentity(ip_add, ip2):
	def getNoneIP():
		r,_ = IPidentity.objects.get_or_create(ip_add='0.0.0.0')
		return r

	if not ip_add:
		if ip2:
			ip_add = ip2
			log.info("using ip2")
		else:
			log.error("no IP")
			return getNoneIP()

	webip = 'http://ip-api.com/json/'+ip_add
	try:
		r=requests.get(webip)
		if r.status_code==200 and r.json()['status']=='success':
			isp=r.json()['isp']
			country=Country.objects.get(alpha2=(r.json()['countryCode']))
			region=str(r.json()['region'])+"@"+str(r.json()['country'])
			city=r.json()['city']
			zipcode=r.json()['zip']
			lat=r.json()['lat']
			lon=r.json()['lon']
			org=r.json()['org']
		else:
			log.error("ip-api didn't work")
			return getNoneIP()

	except Exception as e:
		log.error(e)
		return getNoneIP()
	
	try:
		r,_ = IPidentity.objects.get_or_create(ip_add=ip_add, isp=isp,country=country,region=region,city=city,zipcode=zipcode,lat=lat,lon=lon,org=org)
	except Exception as e:
		log.error(e)
		return getNoneIP()
	return r

def validRedirect(history):
	first=history[0]
	last=history[-1]
	if "blogspot" in first and "blogspot" in last:
		return True
	first = tldextract.extract(first)
	last = tldextract.extract(last)
	if first.domain!=last.domain:
		return False
	else:
		return True

def decide_one_report(report):   #timeout=0  open=1  partial=2  blocked=3  Down = 4
	
	#special cases
	IR = Country.objects.get(alpha2='IR')
	if report.uid.chosen_country==IR and report.status_code == 403 and report.length < 1000:
		new_decision = 31
		return new_decision
	

	if  report.final_url != '0' and report.status_code != 200:
		new_decision = 11
	elif report.final_url == '0': #timeout
		new_decision = 0
	elif report.length < 1000: #tiny webpage, blocked
		new_decision= 31
	elif report.history != '[]':
		historyplus = [x for x in report.history.split("'") if 'http' in x]
		historyplus.append(report.final_url)
		if validRedirect(historyplus):
			new_decision = 1
		else:
			new_decision = 32
	else:
		new_decision=1
	return new_decision 

def makeDecision(url, country, isitproxy): 
	if isitproxy==True:
		all_reports=ReportDecision.objects.filter(report__uid__client='proxy',
		 report__uid__chosen_country=country, report__url=url)
	else:
		all_reports=ReportDecision.objects.filter(report__uid__chosen_country=country, 
			report__url=url).exclude(report__uid__client='proxy')

	all_reports = all_reports.select_related().values('decision')
	decisions = map(lambda d: d['decision'], all_reports)

	if decisions:
		numDown = decisions.count(11)
		numDecisions = len(decisions) - numDown
		numBlocked = decisions.count(31) +  decisions.count(32) 
		numTimeout = decisions.count(0)
		numOpen = decisions.count(1)
			
		blocked = numBlocked>1 or (numDecisions>2 and numTimeout> 0.6*numDecisions) 
		op = numOpen> 0 
		timeout =  numDecisions>2 and numTimeout> 0.2*numDecisions
		if op and blocked:
			decision=2
		elif op:
			decision=1
		elif blocked:
			decision=3
		elif timeout:
			decision=0
		else:
			decision=5

		ud, created=UrlDecision.objects.get_or_create(country=country, url=url)
		if isitproxy==True:
			ud.proxydecision=decision
		else:
			ud.volunteerdecision=decision

		### ???? need to come up with a better decision
		if ud.proxydecision in [5,100] and ud.volunteerdecision in [0,1,2,3]:
			ud.decision = ud.volunteerdecision
		else:
			ud.decision = ud.proxydecision
		ud.save()
	else:
		log.error("makeDecision no reports {0},{1}".format(url, country))

def processReport(repList, ipidentity, uid):
	for rep in repList:
		try:
			u=Url.objects.get(address=rep["url"])
			
			content_object= PageContent.objects.create(content=rep["content"].encode('unicode_escape'))
			report=UrlReport.objects.create(ipidentity=ipidentity, uid=uid, epoch=rep["epoch"], url=u,
				final_url=rep["final_url"], length=rep["length"], elapsed=rep["elapsed"], history=rep["history"], 
				headers=rep["headers"], cookies=rep["cookies"], status_code= rep["status_code"], content=content_object)
			
			if ipidentity.country and uid.chosen_country and ipidentity.country.id == uid.chosen_country.id:
				new_decision = decide_one_report(report)
				flag= (new_decision==32) or (new_decision==31)

				ReportDecision.objects.create(report=report, decision=new_decision, flag= flag)

				if uid.client=='proxy':
					makeDecision(u, uid.chosen_country, True)
				else:
					makeDecision(u, uid.chosen_country, False)
			else:
				log.info("NON MATCHING COUNTRY ipidentity.id={0} uid.uid={1}".format(ipidentity.country.id, uid.chosen_country.uid))
		except Exception as e:
			log.error(e)
			log.error(traceback.format_exc())


@csrf_exempt
def report(request):
	if request.method == 'POST':
		try:
			data = json.loads(request.body)
			reportList = data['report']
			uid = int(data['uid'])
			try:
				data['production']
			except:
				return HttpResponseForbidden()
		except Exception as e:
			log.error(e)
			return HttpResponseBadRequest(e)
		try:
			uid = ReporterUID.objects.get(uid=uid)
		except Exception as e:
			log.error(e)
			return HttpResponseBadRequest()

		if len(reportList)>0 :
			if uid.client=='proxy':
				ipidentity = uid.ipidentity
			else:
				ip = get_real_ip(request)
				ip2 =get_ip(request)
				ipidentity = makeIPidentity(ip, ip2)	
			''' POTENTIAL PLACE TO SUGGEST DOUBLE CHECKING COUNTRY 
			if ipidentity.country.id != uid.chosen_country.id:
			'''
			processReport(reportList, ipidentity, uid)
			return HttpResponse()
		else:
			log.error("empty reportlist "+ str(reportList))
			return HttpResponseBadRequest()
	else:
		return HttpResponseBadRequest()

@csrf_exempt
def websiteGenerator(request):  
	log.debug(request)
	if request.method == 'POST':  #generate uid
		try:
			data=json.loads(request.body)
			try:
				data['production']
			except:
				return HttpResponseForbidden()
			try:
				chosen_country=Country.objects.get(name__iexact=data['country'])
			except:
				try:
					chosen_country=Country.objects.get(alpha2__iexact=data['country'])
				except Exception as e:
					log.error(e)
					return HttpResponseBadRequest(e)
			try:
				client = data['client']
			except:
				client = None
			email=data['email']
			log.debug(str([email, client, chosen_country.alpha2]))
		except Exception as e:
			log.error(e)
			return HttpResponseBadRequest(e)

		if client=='proxy':
			ip=ip2=email.split(':')[0]
		else:
			ip = get_real_ip(request)
			ip2 = get_ip(request)
		ipidentity = makeIPidentity(ip, ip2)
		if client:
			uid,_ = ReporterUID.objects.get_or_create(client=client, chosen_country= chosen_country, email= email, ipidentity=ipidentity)
		else:
			uid,_ = ReporterUID.objects.get_or_create(chosen_country= chosen_country, email= email, ipidentity=ipidentity)

		return HttpResponse(json.dumps({'uid':uid.uid}), content_type="application/json")
	elif 'uid' in request.GET:
		if not 'production' in request.GET:
			return HttpResponseForbidden()
		try:
			uid=int(request.GET['uid'])
		except Exception as e:
			log.error(e)
			return HttpResponseBadRequest("bad params!")
		try:
			load_count = int(request.GET['load_count'])
		except:
			load_count = Url.objects.all().exclude(group__gte=5).count()

		# get reports from this uid in the last 5 days
		fiveDaysAgo = int(time()) - 432000
		recenturls = UrlReport.objects.filter(uid=uid, epoch__gte=fiveDaysAgo).values("url")
		recenturls = [v['url'] for v in recenturls]
		# use urls that are not reported
		newurls = Url.objects.all().exclude(group__gte=5).exclude(id__in=recenturls)
		lst=[l.address for l in newurls]
		shuffle(lst)
		lst=lst[:load_count]
		return HttpResponse(json.dumps({'websites':lst, 'uid':uid}), content_type="application/json")		
	else:
		log.info("websiteGenerator bad request")
		return HttpResponseBadRequest("Missing params")
		
class Moderation(TemplateView):
    template_name = 'mod/moderation.html'
    set_approve = 2 # Set value for ReportDecision when pressed Approve Button
    set_reject = 3 # Set value for ReportDecision when pressed Reject Button
    set_skip = -1 # Set value for ReportDecision when pressed Skip Button

    set_removeURL = 4
    set_removeURLbutAddNewOne = 5
    set_IRspecialCase = 6

    flag = 1 # default value when report need Moderation


    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):

        if request.method == 'POST':
            """
            Method is POST, when the user clicked in any of 3 button Options(Approve, Reject or Skip)
            """

            if request.POST['respond'] == 'Approve':
                """
                User Clicked Approve Button
                """

                # get the Report Decision getting Id for POST['flag'] included in template like hidden input field
                report_decision = ReportDecision.objects.get(id=request.POST['flag'])
                # if is Approve, set the correspond value self.approve
                report_decision.flag = self.set_approve
                #save
                report_decision.save()

            elif request.POST['respond'] == 'Reject':
                """
                Executed when user Clicked on Reject Button
                """
                # get the Report Decision getting Id for POST['flag'] included in template like hidden input field
                report_decision = ReportDecision.objects.get(id=request.POST['flag'])
                report_decision.flag = self.set_reject
                report_decision.decision = 1
                report_decision.save()
                #Call Special function...
                isitproxy = report_decision.report.uid.client=='proxy'
                makeDecision(
                    report_decision.report.url,
                    report_decision.report.uid.chosen_country,
                    isitproxy
                )

            elif request.POST['respond'] == 'Skip':
                """
                Execute when user Clicked on Respond Button
                """
                report_decision = ReportDecision.objects.get(id=request.POST['flag'])
                report_decision.flag = self.set_skip
                report_decision.save()

            elif request.POST['respond'] == 'removeURL':

                report_decision = ReportDecision.objects.get(id=request.POST['flag'])
                report_decision.flag = self.set_removeURL
                report_decision.save()

                u = report_decision.report.url 
                c = report_decision.report.uid.chosen_country

                u.group = 6
                u.save()

                UrlDecision.objects.filter(country=c, url=u).delete()

            elif request.POST['respond'] == 'removeURLbutAddNewOne':

                report_decision = ReportDecision.objects.get(id=request.POST['flag'])
                report_decision.flag = self.set_removeURLbutAddNewOne
                report_decision.save()

                u = report_decision.report.url 
                c = report_decision.report.uid.chosen_country
                u.group = 7
                u.save()
                
                UrlDecision.objects.filter(country=c, url=u).delete()
                #Url.objects.get_or_create(address= report_decision.report.final_url, category= u.category, group=8
            elif request.POST['respond'] == 'IRspecialCase':
				ir = Country.objects.get(alpha2='IR')
				ReportDecision.objects.filter(flag=self.flag, report__uid__chosen_country=ir, decision=3, report__length=332).update(flag=self.set_IRspecialCase)

			#Get actual "Country Code" for redirect to appropiate url /moderate/COUNTRY_CODE
            country_code = request.POST['country_code']

            # Keep in the same page (Skip Page) if the user is in Skip page (/moderate/COUNTRY_CODE/SKIP)
            # When pressed any button (Approved, Reject or SKip

            if request.POST.get('skip', None):
                # keep in Skip Page.
                return HttpResponseRedirect(reverse('moderation_page', args=[country_code, 'skip']))

            return HttpResponseRedirect(reverse('moderation_page', args=[country_code]))

        return super(Moderation, self).dispatch(request, *args, **kwargs)

    def get_report(self, uid):
        """
        Get report..function, only a auxilia function that get a Reporter Model Object and verify this has
        ReportDecisions for get and return only 1
        :param reporter:
        :return:
        """
        # get all ReportDecision of this reporter
        reports = ReportDecision.objects.filter(
            report__uid=uid,
            flag = self.flag,  #comment or change according the requirements
        )
        if reports:
            # if this Reporter has ReportDecisions Record..Return the first..
            return reports[0]
        else:
            # if not have more ReportDecisions..return False
            return False

    def get_context_data(self, **kwargs):
        """
        Return Context Data for templates: moderation.html or moderate.html
        :param kwargs:
        :return:
        """
        # get Default Context data
        context = super(Moderation, self).get_context_data()

        # Get option selected for the User, if user select YES in the option "View reports skipped:" (moderation.html)
        # so this add a prefix /skip/ to the URL that we can acces via "choose_opt". urls.py Line:15
        view_reports_skipped = self.kwargs.get('choose_opt', None)
        # Get country_code. See Urls.py
        country_code = self.kwargs.get('country_code', None)

        # Save Country Code for show in templates
        context['country_code'] = country_code
        # Get all Countries ..used for template moderation.html (Select OPtion) Line: 25 to 29 ,
        # but show only Countries with existing Reporters
        context['countries'] = ReporterUID.objects.values('chosen_country__alpha3', 'chosen_country__name').distinct()

        if view_reports_skipped == 'skip':
            """
            If user selected see only Skipped reports on template moderation.html. Line 34 to 36,
            so set flag default value from 1 to -1 for use of function get_report. Line: 83
            """
            self.flag = -1
            context['skip'] = 'skip'

        if country_code:
            """
            If url has a Country Code defined..so the user are selected a option and we need render a diferent template:
            moderate.html, this template show all fields of a Report.
            """

            self.template_name = 'mod/moderate.html'

            # get exact Country based on the unique country_code (alpha3)
            country = Country.objects.get(alpha3__iexact=country_code)
            # Now get all Reporters for this Country.
            uid = ReporterUID.objects.filter(chosen_country=country)

            # If exists Reporters for this Country..
            if uid:
				# Get the first ReporDecision to moderate of this Reporter..
				report_decision = self.get_report(uid[0])
				# set context for the first ReportDecision returned
				context['country'] = country
				if report_decision:
					report_decision.report.time = datetime.datetime.fromtimestamp(report_decision.report.epoch)
					soup=bs(report_decision.report.content.content)                #make BeautifulSoup
					prettyHTML=soup.prettify()   #prettify the html
					report_decision.report.prettycontent = prettyHTML
				context['report_decision'] = report_decision

				# this value is used in themplate for determinated if a Country or Reporter has or don't have more Reports to moderate
				# and show the corresponding message, moderate.html 48 to 51
				context['has_reports'] = True if report_decision else False
            else:
                context['has_reports'] = False

        return context