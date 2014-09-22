from django.shortcuts import render_to_response
from models import *
from django.http import HttpResponse
import json
from django.forms.models import model_to_dict
flag_list=['ac', 'ae', 'af', 'ag', 'ai', 'al', 'am', 'an', 'ao', 'ap', 'aq', 'ar', 'as', 'at', 'au', 'aw', 'az', 'ba', 'bb', 'bd', 'be', 'bf', 'bg', 'bh', 'bi', 'bj', 'bm', 'bn', 'bo', 'br', 'bs', 'bt', 'bv', 'bw', 'by', 'bz', 'ca', 'cc', 'cd', 'cf', 'cg', 'ch', 'ci', 'ck', 'cl', 'cm', 'cn', 'co', 'cr', 'cs', 'cu', 'cv', 'cx', 'cy', 'cz', 'de', 'dj', 'dk', 'dm', 'do', 'dz', 'ec', 'ee', 'eg', 'eh', 'er', 'es', 'et', 'eu', 'fi', 'fj', 'fk', 'fm', 'fo', 'fr', 'ga', 'gb', 'gd', 'ge', 'gf', 'gg', 'gh', 'gi', 'gl', 'gm', 'gn', 'gp', 'gq', 'gr', 'gs', 'gt', 'gu', 'gw', 'gy', 'hk', 'hm', 'hn', 'hr', 'ht', 'hu', 'id', 'ie', 'il', 'im', 'in', 'io', 'iq', 'ir', 'is', 'it', 'je', 'jm', 'jo', 'jp', 'ke', 'kg', 'kh', 'ki', 'km', 'kn', 'kp', 'kr', 'kw', 'ky', 'kz', 'la', 'lb', 'lc', 'li', 'lk', 'lr', 'ls', 'lt', 'lu', 'lv', 'ly', 'ma', 'mc', 'md', 'mg', 'mh', 'mk', 'ml', 'mm', 'mn', 'mo', 'mp', 'mq', 'mr', 'ms', 'mt', 'mu', 'mv', 'mw', 'mx', 'my', 'mz', 'na', 'nc', 'ne', 'nf', 'ng', 'ni', 'nl', 'no', 'np', 'nr', 'nu', 'nz', 'om', 'pa', 'pe', 'pf', 'pg', 'ph', 'philippines_flagsm', 'pk', 'pl', 'pm', 'pn', 'pr', 'priv-172', 'priv-192', 'priv-localhost', 'ps', 'pt', 'pw', 'py', 'qa', 're', 'ro', 'ru', 'rw', 'sa', 'sb', 'sc', 'sd', 'se', 'sg', 'sh', 'si', 'sj', 'sk', 'sl', 'sm', 'sn', 'so', 'sr', 'st', 'sv', 'sy', 'sz', 'tc', 'td', 'tf', 'tg', 'th', 'tj', 'tk', 'tl', 'tm', 'tn', 'to', 'tp', 'tr', 'tt', 'tv', 'tw', 'tz', 'ua', 'ug', 'uk', 'um', 'us', 'uy', 'uz', 'va', 'vc', 've', 'vg', 'vi', 'vn', 'vu', 'wf', 'ws', 'xx', 'ye', 'yt', 'yu', 'za', 'zm', 'zw']
from django.db.models import Count
import hoover
import re
from datetime import datetime
import logging

class HttpResponseBadRequest(HttpResponse):
    status_code = 400

log = logging.getLogger('bo_apis')
# logging.addLevelName(logging.INFO, 'info')
# log.setLevel(logging.INFO)

# logglyhandler = hoover.LogglyHttpHandler(token='7e3806dd-1b8d-4955-870c-d049747f6140')
# logglyhandler.setLevel(logging.WARNING)
# logglyformatter = logging.Formatter('{"time": "%(asctime)s", "level":"%(levelname)s",' \
#  '"error_number": "%(error_number)s", "message":"%(message)s", "other":"%(other)s"}' ) 
# logglyhandler.setFormatter(logglyformatter)
# log.addHandler(logglyhandler)


# http://blockedonline.com/blocked/data?homepage

# http://blockedonline.com/blocked/data?url_query=google    //search through urls

# http://blockedonline.com/blocked/data?url=http://images.google.com&v=0  //quick summary
# http://blockedonline.com/blocked/data?url=http://images.google.com&v=1  //map data for url

# http://blockedonline.com/blocked/data?country=us&v=0  //horizonal stacked graph
# http://blockedonline.com/blocked/data?country=us&v=1 //extra data
# http://blockedonline.com/blocked/data?country=us&v=2 //quick summary
# http://blockedonline.com/blocked/data?country=us&v=3 //top websites
# http://blockedonline.com/blocked/data?country=us&v=4 //donut
# http://blockedonline.com/blocked/data?country=us&v=5 //news

def news(request):
	result = {}
	result['status']='OK'
	top_news=News.objects.all()[:50]
	result['news']= [{"news_title": n.title, "description": n.description, "link":n.getUrl(), "agency":n.agency} for n in top_news]
	return HttpResponse(json.dumps(result, indent=2), content_type="application/json")

def data(request):
	if 'country' in request.GET and 'v' in request.GET:
		version=request.GET['v']
		cty=request.GET['country']
		try:
			cty= cty.upper()
			c=Country.objects.get(alpha2__iexact=cty)
		except:
			log.error("wrong country param sent to bo_api {0}".format(str(cty)))
			return HttpResponse(json.dumps({'status':'ERROR', 'message':'wrong country param.'}, indent=2), content_type="application/json")

		if version=='0':   #horizonal stacked graph
			result={}

			#lst=UrlDecision.objects.filter(country=c).select_related().values('url__category').distinct()
			#cats=list(set([s.url.category for s in lst]))

			result['title']="Blocked Vs. Open Pages Of All The Websites Scanned"
			data=[]
			def get_country_decisions(country, decision_type):
				decisions=UrlDecision.objects.filter(
					country=country, decision=decision_type).select_related().values('url__category').annotate(Count("id")).order_by()
				return [{'x':str(d['url__category']), 'y': int(d['id__count'])} for d in decisions]
	      
			blk2 = get_country_decisions(c, 3)
			partial2 = get_country_decisions(c, 2)
			opn2 = get_country_decisions(c, 1)
				
			if blk2 or partial2 or opn2:
				blkkeys=[k['x'] for k in blk2]
				partialkeys=[k['x'] for k in partial2]
				opnkeys=[k['x'] for k in opn2]

				for k in partial2:
					if not k['x'] in blkkeys:
						blk2.append({'x':k['x'], 'y': 0})
						blkkeys.append(k['x'])
					if not k['x'] in opnkeys:
						opn2.append({'x':k['x'], 'y': 0})
						opnkeys.append(k['x'])
						
				for k in blk2:
					if not k['x'] in partialkeys:
						partial2.append({'x':k['x'], 'y': 0})	
						partialkeys.append(k['x'])					
					if not k['x'] in opnkeys:
						opn2.append({'x':k['x'], 'y': 0})
						opnkeys.append(k['x'])

				for k in opn2:
					if not k['x'] in partialkeys:
						partial2.append({'x':k['x'], 'y': 0})
						partialkeys.append(k['x'])						
					if not k['x'] in blkkeys:
						blk2.append({'x':k['x'], 'y': 0})
						blkkeys.append(k['x'])

				blk2.sort(key=lambda x:x['x'])
				partial2.sort(key=lambda x:x['x'])
				opn2.sort(key=lambda x:x['x'])

				data.append({"key": "Blocked", "color": "#BD362F", "values": blk2})
				data.append({"key": "Partially/Inconsistently Blocked", "color": "#BD3620", "values": partial2})
				data.append({"key": "Open", "color": "#51A351", "values": opn2})

				result['data']=data
			if len(data)>0:
				result['status']='OK'
				result['v']=int(version)
				return HttpResponse(json.dumps(result, indent=2), content_type="application/json")
			else:
				return HttpResponse(json.dumps({'v':int(version), 'status':'ERROR', 'message':'No data!'}, indent=2), content_type="application/json")

		elif version=='1': # all data
			result={}
			dic=model_to_dict(c)
			for key, val in dic.items():
				if val==None: del dic[key]

			items=[]

			if "internet_code" in dic: items.append({"key":"Internet Code:", "value":dic["internet_code"], "logo":"http://blockedonline.github.io/final/img/WebCountryCode.png"})
			if "population" in dic: items.append({"key":"Country population:", "value":dic["population"],"logo":"http://blockedonline.github.io/final/img/population-01.png"})
			if "population_with_internet" in dic: items.append({'key':"Population with internet access:",'value':dic["population_with_internet"],'logo':'http://blockedonline.github.io/final/img/InternetAccess.png'})
			if "median_age" in dic: items.append({'key':"Country median age:",'value':dic["median_age"],'logo':'http://blockedonline.github.io/final/img/InternetSpeed-02.png'})
			if "upload_speed" in dic and 'download_speed' in dic: items.append({'key':"Average Internet Speed:",'value': "Download:{0}\nUpload:{1}".format(dic["download_speed"],dic["upload_speed"]),'logo':'http://blockedonline.github.io/final/img/CountryMedianAge-01.png'})
			if "press_freedom_rank" in dic: items.append({'key':"Press Freedom Index according to Reporters Without Borders:",'value':str(dic["press_freedom_rank"]),'logo':'http://blockedonline.github.io/final/img/FreedomIndex.png'})

			result['title']="More Information"
			result['bullets']=items

			if len(items)>0:
				result['status']='OK'
				result['v']=int(version)
				return HttpResponse(json.dumps(result, indent=2), content_type="application/json")
			else:
				return HttpResponse(json.dumps({'v':int(version),'status':'ERROR', 'message':'No data!'}, indent=2), content_type="application/json")

		elif version=='2': # quick details

			result={}


			def get_decision_count_country(country, decision):
				return UrlDecision.objects.filter(country=country, decision=decision).select_related().count()

			op = get_decision_count_country(c, 1)
			partial = get_decision_count_country(c, 2)
			cl = get_decision_count_country(c, 3)
			timeout = get_decision_count_country(c, 0)

			items=[]
			#items.append(str(c.name))
			if c.official_name!=None: items.append({'key':'Official Name:', 'value':str(c.official_name), 'logo':'http://blockedonline.github.io/final/img/countryName-01.png'})
			if cl>0: items.append({'key':'Number of websites blocked:','value':str(cl),'logo':'http://blockedonline.github.io/final/img/blockedOrInaccessible-01.png'})
			if timeout>0: items.append({'key':'Number of websites inaccessible due to timeout:','value':str(timeout),'logo':''})
			if partial>0: items.append({'key':'Number of websites partially or inconsistently blocked:','value':str(partial),'logo':'http://blockedonline.github.io/final/img/inconsistentlyBlocked-02.png'})
			if op>0: items.append({'key':'Number of websites open:','value':str(op),'logo':'http://blockedonline.github.io/final/img/available-01.png'})
			#if not (op or cl or partial): items.append({'key':'statement','value':"We don't have any data from this location. <strong>We need your help.</strong>",'logo':''})
			numReporters=ReporterUID.objects.filter(chosen_country=c).select_related().count()
			if numReporters:
				for n in range(numReporters):
					last_reporter=ReporterUID.objects.filter(chosen_country=c).reverse()[n]
					query = UrlReport.objects.filter(uid=last_reporter)
					if query.exists():
						timeofreport=query.reverse()[0].epoch
						timeofreport=datetime.fromtimestamp(timeofreport).strftime('%Y-%m-%d')

						items.append({'key':'Number of reporters from the country','value':str(numReporters),'logo':'http://blockedonline.github.io/final/img/reporters-01.png'})
						items.append({'key':'Last report from the country','value':str(timeofreport),'logo':'http://blockedonline.github.io/final/img/lastReport-01.png'})
						break

			result['title']="Quick Summary"
			result['bullets']=items

			if len(items)>0:
				result['status']='OK'
				result['v']=int(version)
				
				if c.alpha2.lower() in flag_list:
					result['flag']="http://blockedonline.github.io/index_files/flags/{0}.gif".format(c.alpha2.lower())
				else:
					result['flag']="http://blockedonline.github.io/index_files/flags/0.gif"
				return HttpResponse(json.dumps(result, indent=2), content_type="application/json")
			else:
				return HttpResponse(json.dumps({'v':int(version),'status':'ERROR', 'message':'No data!'}, indent=2), content_type="application/json")

		elif version=='3': # Top websites
			result={}

			# lst=UrlDecision.objects.filter(country=c, url__base_url=None)
			# blocked=[o for o in lst if o.decision==3]

			# items=sorted(blocked, key=lambda x: x.url.global_rank)
			# items=items[:10]
			# items=[x.url.address for x in items]

			blocked = UrlDecision.objects.filter(country=c, url__base_url=None, decision=3).select_related().order_by('url__global_rank').values('url__address')[:10]
			items = map(lambda d: d['url__address'], blocked)

			result['title']="Top Blocked Websites With Highest Global Rank"
			result['websites']=items

			
			if len(items)>0:
				result['status']='OK'
				result['v']=int(version)
				return HttpResponse(json.dumps(result, indent=2), content_type="application/json")
			else:
				return HttpResponse(json.dumps({'v':int(version),'status':'ERROR', 'message':'No data!'}, indent=2), content_type="application/json")

		elif version=='4':  #Donut

			result={}
			lst=UrlDecision.objects.filter(country=c).select_related().values('url__category').distinct()
			# cats=list(set([s.url.category for s in lst]))
			result['title']="Blocked Websites By Category"
			data = UrlDecision.objects.filter(country=c, decision=3).values('url__category').annotate(value=Count('url__category'))

			data = [{'label': x['url__category'], 'value': x['value']} for x in data]
			result['data']=data
			if len(data)>0:
				result['status']='OK'
				result['v']=int(version)
				return HttpResponse(json.dumps(result, indent=2), content_type="application/json")
			else:
				return HttpResponse(json.dumps({'v':int(version),'status':'ERROR', 'message':'No data!'}, indent=2), content_type="application/json")

		
		elif version=='5':  #news
			result={}
			lst=News.objects.filter(country=c)[:6]
			result['title']="News"

			data = [{"news_title": n.title, "description": n.description, "link":n.getUrl(), "agency":n.agency} for n in lst]
			result['data']=data
			if len(data)>0:
				result['status']='OK'
				result['v']=int(version)
				return HttpResponse(json.dumps(result, indent=2), content_type="application/json")
			else:
				return HttpResponse(json.dumps({'v':int(version),'status':'ERROR', 'message':'No data!'}, indent=2), content_type="application/json")

		else:
			return HttpResponse(json.dumps({'v': version,'status':'ERROR', 'message':'wrong v param.'}, indent=2), content_type="application/json")
	
	elif 'url_query' in request.GET:
		q=request.GET['url_query']
		q=q.replace('www.', '')
		urls=Url.objects.filter(base_url=None, address__icontains=q).exclude(group__gte=5).values('address')[:10]
		items = [{'url':u['address']} for u in urls]

		return HttpResponse(json.dumps({'result':items}, indent=2), content_type="application/json")
	elif 'url' in request.GET and 'v' in request.GET:
		try:
			ur=request.GET['url']
			u=Url.objects.get(address__iexact=ur)
			v=int(request.GET['v'])
		except:
			log.error("wrong url param sent to bo_api  {0}\t{1}".format(request.GET['url'], request.GET['v']))
			return HttpResponse(json.dumps({'status':'ERROR', 'message':'wrong url param.'}, indent=2), content_type="application/json")

		def get_decisions_url(url, decision):
			return UrlDecision.objects.filter(url=url, decision=decision)
		def get_decision_url_count(url, decision):
			return get_decisions_url(url, decision).count()

		if v==0:
			items=[]
			items.append({'key':'Global Rank:', 'value':str(u.global_rank), 'logo':'http://blockedonline.github.io/final/img/alexa.png'})

			decisionCount=UrlDecision.objects.filter(url=u).count()
			
			openCountryCount = get_decision_url_count(u, 1)
			partialCountryCount = get_decision_url_count(u, 2)
			blockedCountryCount = get_decision_url_count(u, 3)

			items.append({'key':'Number of countries checked for this website:','value':str(decisionCount),'logo':'http://blockedonline.github.io/final/img/lastReport-01.png'})

			if openCountryCount: 
				items.append({'key':'Number of countries open:','value':str(openCountryCount),'logo':'http://blockedonline.github.io/final/img/available-01.png'})
			if partialCountryCount: 
				items.append({'key':'Number of countries inconsistently blocked this website:','value':str(partialCountryCount),'logo':'http://blockedonline.github.io/final/img/inconsistentlyBlocked-02.png'})
			if blockedCountryCount: 
				items.append({'key':'Number of countries blocked this website:','value':str(blockedCountryCount),'logo':'http://blockedonline.github.io/final/img/blockedOrInaccessible-01.png'})

			result={}
			result['status']='OK'
			result['v']=v
			result['bullets']=items
			result['title']="Quick Summary"
			return HttpResponse(json.dumps(result, indent=2), content_type="application/json")
		elif v==1:

			decisions=UrlDecision.objects.filter(url=u).count()
			if not decisions:
				return HttpResponse(json.dumps({'v':v,'status':'ERROR', 'message':'No data!'}, indent=2), content_type="application/json")
			else:
				result={}
				result['status']='OK'
				result['v']=v
				result['title']="Status Of The Website Around The World"
				data={}
				openCountries=get_decisions_url(u, 1)
				partialCountries=get_decisions_url(u, 2)
				blockedCountries=get_decisions_url(u, 3)
				for op in openCountries:
					#data[op.alpha3]={"fillKey": "open", "number": UrlReport.objects.filter(url=u).count()}
					data[op.country.alpha3]={"fillKey": "open"}
				for bl in blockedCountries:
					#data[bl.alpha3]={"fillKey": "blocked", "number": UrlReport.objects.filter(url=u).count()}
					data[bl.country.alpha3]={"fillKey": "blocked"}
				for pr in partialCountries:
					#data[pr.alpha3]={"fillKey": "partially_blocked", "number": UrlReport.objects.filter(url=u).count()}
					data[pr.country.alpha3]={"fillKey": "partially_blocked"}

				result['data']=data
				return HttpResponse(json.dumps(result, indent=2), content_type="application/json")
		
		elif v==2:  #news
			result={}
			lst=News.objects.filter(url=u)[:6]
			result['title']="News"
			data = [{"news_title": n.title, "description": n.description, "link":n.getUrl(), "agency":n.agency} for n in lst]
			result['data']=data
			if len(data):
				result['status']='OK'
				result['v']=int(v)
				return HttpResponse(json.dumps(result, indent=2), content_type="application/json")
			else:
				return HttpResponse(json.dumps({'v':int(v),'status':'ERROR', 'message':'No data!'}, indent=2), content_type="application/json")

		else:
			return HttpResponse(json.dumps({'status':'ERROR', 'message':'wrong v param.'}, indent=2), content_type="application/json")
	
	elif 'homepage' in request.GET:
		result={}
		result['status']='OK'
		terms=[{'alpha2': u'CA', 'alpha3': u'CAN', 'c': u'Canada', 'n': '73', 'comparative_grade': 0.129749537576801, 'total_scanned': '11707'}, {'alpha2': u'LT', 'alpha3': u'LTU', 'c': u'Lithuania', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '2328'}, {'alpha2': u'KH', 'alpha3': u'KHM', 'c': u'Cambodia', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '1073'}, {'alpha2': u'ET', 'alpha3': u'ETH', 'c': u'Ethiopia', 'n': '1', 'comparative_grade': 0.005186419632921814, 'total_scanned': '4012'}, {'alpha2': u'AR', 'alpha3': u'ARG', 'c': u'Argentina', 'n': '4', 'comparative_grade': 0.018724783412627507, 'total_scanned': '4445'}, {'alpha2': u'BO', 'alpha3': u'BOL', 'c': u'Bolivia', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '1404'}, {'alpha2': u'SA', 'alpha3': u'SAU', 'c': u'Saudi Arabia', 'n': '1322', 'comparative_grade': 1, 'total_scanned': '11707'}, {'alpha2': u'GT', 'alpha3': u'GTM', 'c': u'Guatemala', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '2298'}, {'alpha2': u'BA', 'alpha3': u'BIH', 'c': u'Bosnia and Herzegovina', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '173'}, {'alpha2': u'RU', 'alpha3': u'RUS', 'c': u'Russian Federation', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '11707'}, {'alpha2': u'LR', 'alpha3': u'LBR', 'c': u'Liberia', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '203'}, {'alpha2': u'MV', 'alpha3': u'MDV', 'c': u'Maldives', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '30'}, {'alpha2': u'TZ', 'alpha3': u'TZA', 'c': u'Tanzania', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '30'}, {'alpha2': u'PK', 'alpha3': u'PAK', 'c': u'Pakistan', 'n': '110', 'comparative_grade': 0.1955130018280563, 'total_scanned': '11707'}, {'alpha2': u'AL', 'alpha3': u'ALB', 'c': u'Albania', 'n': '1', 'comparative_grade': 0.012757765522552004, 'total_scanned': '1631'}, {'alpha2': u'AE', 'alpha3': u'ARE', 'c': u'United Arab Emirates', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '299'}, {'alpha2': u'VN', 'alpha3': u'VNM', 'c': u'Viet Nam', 'n': '103', 'comparative_grade': 0.18308690444473594, 'total_scanned': '11706'}, {'alpha2': u'KE', 'alpha3': u'KEN', 'c': u'Kenya', 'n': '11', 'comparative_grade': 0.04488861958033056, 'total_scanned': '5099'}, {'alpha2': u'KR', 'alpha3': u'KOR', 'c': u'South Korea', 'n': '205', 'comparative_grade': 0.3643651397704686, 'total_scanned': '11707'}, {'alpha2': u'TR', 'alpha3': u'TUR', 'c': u'Turkey', 'n': '123', 'comparative_grade': 0.21861908386228115, 'total_scanned': '11707'}, {'alpha2': u'AF', 'alpha3': u'AFG', 'c': u'Afghanistan', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '226'}, {'alpha2': u'CZ', 'alpha3': u'CZE', 'c': u'Czech Republic', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '7208'}, {'alpha2': u'IN', 'alpha3': u'IND', 'c': u'India', 'n': '90', 'comparative_grade': 0.15996518331386425, 'total_scanned': '11707'}, {'alpha2': u'MN', 'alpha3': u'MNG', 'c': u'Mongolia', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '117'}, {'alpha2': u'FR', 'alpha3': u'FRA', 'c': u'France', 'n': '18', 'comparative_grade': 0.03298480671167607, 'total_scanned': '11355'}, {'alpha2': u'SK', 'alpha3': u'SVK', 'c': u'Slovakia', 'n': '49', 'comparative_grade': 0.08709215535977054, 'total_scanned': '11707'}, {'alpha2': u'PE', 'alpha3': u'PER', 'c': u'Peru', 'n': '12', 'comparative_grade': 0.023246903156818533, 'total_scanned': '10741'}, {'alpha2': u'SG', 'alpha3': u'SGP', 'c': u'Singapore', 'n': '104', 'comparative_grade': 0.18489603716655514, 'total_scanned': '11704'}, {'alpha2': u'CN', 'alpha3': u'CHN', 'c': u'China', 'n': '26', 'comparative_grade': 0.0686294310223697, 'total_scanned': '7883'}, {'alpha2': u'AM', 'alpha3': u'ARM', 'c': u'Armenia', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '5587'}, {'alpha2': u'DO', 'alpha3': u'DOM', 'c': u'Dominican Republic', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '2498'}, {'alpha2': u'UA', 'alpha3': u'UKR', 'c': u'Ukraine', 'n': '93', 'comparative_grade': 0.16549526620689778, 'total_scanned': '11693'}, {'alpha2': u'LY', 'alpha3': u'LBY', 'c': u'Libya', 'n': '2', 'comparative_grade': 0.00392676270377096, 'total_scanned': '10598'}, {'alpha2': u'ID', 'alpha3': u'IDN', 'c': u'Indonesia', 'n': '120', 'comparative_grade': 0.21328691108515235, 'total_scanned': '11707'}, {'alpha2': u'MU', 'alpha3': u'MUS', 'c': u'Mauritius', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '536'}, {'alpha2': u'SE', 'alpha3': u'SWE', 'c': u'Sweden', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '338'}, {'alpha2': u'BG', 'alpha3': u'BGR', 'c': u'Bulgaria', 'n': '1', 'comparative_grade': 0.008205014024953597, 'total_scanned': '2536'}, {'alpha2': u'RO', 'alpha3': u'ROU', 'c': u'Romania', 'n': '87', 'comparative_grade': 0.154659432238664, 'total_scanned': '11705'}, {'alpha2': u'TD', 'alpha3': u'TCD', 'c': u'Chad', 'n': '1', 'comparative_grade': 0.02447990066739096, 'total_scanned': '850'}, {'alpha2': u'ZA', 'alpha3': u'ZAF', 'c': u'South Africa', 'n': '176', 'comparative_grade': 0.3154072121127972, 'total_scanned': '11611'}, {'alpha2': u'MY', 'alpha3': u'MYS', 'c': u'Malaysia', 'n': '112', 'comparative_grade': 0.19906778367947553, 'total_scanned': '11707'}, {'alpha2': u'AT', 'alpha3': u'AUT', 'c': u'Austria', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '31'}, {'alpha2': u'JP', 'alpha3': u'JPN', 'c': u'Japan', 'n': '12', 'comparative_grade': 0.022013134691650168, 'total_scanned': '11343'}, {'alpha2': u'BR', 'alpha3': u'BRA', 'c': u'Brazil', 'n': '81', 'comparative_grade': 0.14396866498247782, 'total_scanned': '11707'}, {'alpha2': u'PA', 'alpha3': u'PAN', 'c': u'Panama', 'n': '9', 'comparative_grade': 0.07581831583220278, 'total_scanned': '2470'}, {'alpha2': u'CR', 'alpha3': u'CRI', 'c': u'Costa Rica', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '8930'}, {'alpha2': u'IE', 'alpha3': u'IRL', 'c': u'Ireland', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '59'}, {'alpha2': u'NG', 'alpha3': u'NGA', 'c': u'Nigeria', 'n': '6', 'comparative_grade': 0.016903262036784987, 'total_scanned': '7386'}, {'alpha2': u'EC', 'alpha3': u'ECU', 'c': u'Ecuador', 'n': '72', 'comparative_grade': 0.12819114578970883, 'total_scanned': '11687'}, {'alpha2': u'BD', 'alpha3': u'BGD', 'c': u'Bangladesh', 'n': '8', 'comparative_grade': 0.023119906185869243, 'total_scanned': '7200'}, {'alpha2': u'BY', 'alpha3': u'BLR', 'c': u'Belarus', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '4773'}, {'alpha2': u'IR', 'alpha3': u'IRN', 'c': u'Iran', 'n': '3354', 'comparative_grade': 1, 'total_scanned': '11593'}, {'alpha2': u'CL', 'alpha3': u'CHL', 'c': u'Chile', 'n': '41', 'comparative_grade': 0.07339337046271292, 'total_scanned': '11624'}, {'alpha2': u'TH', 'alpha3': u'THA', 'c': u'Thailand', 'n': '91', 'comparative_grade': 0.16170113720091298, 'total_scanned': '11710'}, {'alpha2': u'IQ', 'alpha3': u'IRQ', 'c': u'Iraq', 'n': '307', 'comparative_grade': 0.545659014192848, 'total_scanned': '11707'}, {'alpha2': u'HK', 'alpha3': u'HKG', 'c': u'Hong Kong', 'n': '90', 'comparative_grade': 0.16459064871290285, 'total_scanned': '11378'}, {'alpha2': u'GE', 'alpha3': u'GEO', 'c': u'Georgia', 'n': '1', 'comparative_grade': 0.008380151255449988, 'total_scanned': '2483'}, {'alpha2': u'DK', 'alpha3': u'DNK', 'c': u'Denmark', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '34'}, {'alpha2': u'PH', 'alpha3': u'PHL', 'c': u'Philippines', 'n': '1', 'comparative_grade': 0.00362444096277344, 'total_scanned': '5741'}, {'alpha2': u'MD', 'alpha3': u'MDA', 'c': u'Moldova', 'n': '1', 'comparative_grade': 0.005853140806549176, 'total_scanned': '3555'}, {'alpha2': u'HR', 'alpha3': u'HRV', 'c': u'Croatia', 'n': '1', 'comparative_grade': 0.007219956824178459, 'total_scanned': '2882'}, {'alpha2': u'CH', 'alpha3': u'CHE', 'c': u'Switzerland', 'n': '5', 'comparative_grade': 0.01626889411046311, 'total_scanned': '6395'}, {'alpha2': u'SC', 'alpha3': u'SYC', 'c': u'Seychelles', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '31'}, {'alpha2': u'EE', 'alpha3': u'EST', 'c': u'Estonia', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '54'}, {'alpha2': u'LB', 'alpha3': u'LBN', 'c': u'Lebanon', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '1693'}, {'alpha2': u'TN', 'alpha3': u'TUN', 'c': u'Tunisia', 'n': '155', 'comparative_grade': 0.2754955934849884, 'total_scanned': '11707'}, {'alpha2': u'CO', 'alpha3': u'COL', 'c': u'Colombia', 'n': '96', 'comparative_grade': 0.17067326507682012, 'total_scanned': '11704'}, {'alpha2': u'BI', 'alpha3': u'BDI', 'c': u'Burundi', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '3'}, {'alpha2': u'TW', 'alpha3': u'TWN', 'c': u'Taiwan', 'n': '17', 'comparative_grade': 0.040537997323378344, 'total_scanned': '8726'}, {'alpha2': u'IT', 'alpha3': u'ITA', 'c': u'Italy', 'n': '379', 'comparative_grade': 0.7, 'total_scanned': '11266'}, {'alpha2': u'SD', 'alpha3': u'SDN', 'c': u'Sudan', 'n': '6', 'comparative_grade': 0.017953335260813046, 'total_scanned': '6954'}, {'alpha2': u'NP', 'alpha3': u'NPL', 'c': u'Nepal', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '92'}, {'alpha2': u'NL', 'alpha3': u'NLD', 'c': u'Netherlands', 'n': '53', 'comparative_grade': 0.09420171906260895, 'total_scanned': '11707'}, {'alpha2': u'VE', 'alpha3': u'VEN', 'c': u'Venezuela', 'n': '8', 'comparative_grade': 0.018204650540054525, 'total_scanned': '9144'}, {'alpha2': u'IL', 'alpha3': u'ISR', 'c': u'Israel', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '278'}, {'alpha2': u'ZM', 'alpha3': u'ZMB', 'c': u'Zambia', 'n': '1', 'comparative_grade': 0.00748755507998644, 'total_scanned': '2779'}, {'alpha2': u'PG', 'alpha3': u'PNG', 'c': u'Papua New Guinea', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '115'}, {'alpha2': u'ZW', 'alpha3': u'ZWE', 'c': u'Zimbabwe', 'n': '6', 'comparative_grade': 0.012135254024464807, 'total_scanned': '10288'}, {'alpha2': u'DE', 'alpha3': u'DEU', 'c': u'Germany', 'n': '8', 'comparative_grade': 0.019446650062880672, 'total_scanned': '8560'}, {'alpha2': u'KZ', 'alpha3': u'KAZ', 'c': u'Kazakhstan', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '1077'}, {'alpha2': u'PL', 'alpha3': u'POL', 'c': u'Poland', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '865'}, {'alpha2': u'MK', 'alpha3': u'MKD', 'c': u'Macedonia', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '31'}, {'alpha2': u'LV', 'alpha3': u'LVA', 'c': u'Latvia', 'n': '5', 'comparative_grade': 0.012578839056512102, 'total_scanned': '8271'}, {'alpha2': u'HU', 'alpha3': u'HUN', 'c': u'Hungary', 'n': '177', 'comparative_grade': 0.31459819385059967, 'total_scanned': '11707'}, {'alpha2': u'HN', 'alpha3': u'HND', 'c': u'Honduras', 'n': '2', 'comparative_grade': 0.004884487222366741, 'total_scanned': '8520'}, {'alpha2': u'MM', 'alpha3': u'MMR', 'c': u'Myanmar', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '690'}, {'alpha2': u'MX', 'alpha3': u'MEX', 'c': u'Mexico', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '729'}, {'alpha2': u'EG', 'alpha3': u'EGY', 'c': u'Egypt', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '2969'}, {'alpha2': u'RS', 'alpha3': u'SRB', 'c': u'Serbia', 'n': '15', 'comparative_grade': 0.036924019106735456, 'total_scanned': '8453'}, {'alpha2': u'GB', 'alpha3': u'GBR', 'c': u'United Kingdom', 'n': '61', 'comparative_grade': 0.10842084646828576, 'total_scanned': '11707'}, {'alpha2': u'CD', 'alpha3': u'COD', 'c': u'Congo', 'n': '144', 'comparative_grade': 0.27388846816166856, 'total_scanned': '10940'}, {'alpha2': u'GR', 'alpha3': u'GRC', 'c': u'Greece', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '414'}, {'alpha2': u'PY', 'alpha3': u'PRY', 'c': u'Paraguay', 'n': '143', 'comparative_grade': 0.25416690237647316, 'total_scanned': '11707'}, {'alpha2': u'BW', 'alpha3': u'BWA', 'c': u'Botswana', 'n': '0', 'comparative_grade': 0.0, 'total_scanned': '29'}]
		#decidedCountry=Country.objects.order_by('name').distinct('name', 'alpha2', 'alpha3')
		#for x in decidedCountry:
		#	numberOfCountries = UrlDecision.objects.filter(country__name=x.name).select_related().count()
		#	if not numberOfCountries:
		#		continue
		#	numOfBlocked =  UrlDecision.objects.filter(country__name=x.name, decision =3).select_related().count()
		'''countryQuery = UrlDecision.objects.select_related().values('country__name', 'country__alpha2', 'country__alpha3').annotate(count=Count('country__name'))
		decisionQuery = UrlDecision.objects.filter(decision=3).select_related().values('country__name', 'country__alpha2', 'country__alpha3').annotate(count=Count('country__name'))

		def list_to_dict(l, key):
			return {d[key] : d for d in l}

		countries = list_to_dict(countryQuery, 'country__name')
		decisions = list_to_dict(decisionQuery, 'country__name')
		for countryName, countryDict in countries.iteritems():
			numOfBlocked = decisions.get(countryName, {}).get('count', 0)
			numOfCountries = countryDict.get('count', 0)

			# num = UrlDecision.objects.filter(country__name=x.name).select_related()
			# numberOfCountries = num.count()
			# if not numberOfCountries:
			# 	continue
			# num = len([va for va in num if va.decision()==3
			if numOfCountries>0:
				if numOfBlocked>800:
					cgrade= 1
				else:
					cgrade = float(numOfBlocked)/numOfCountries
				terms.append({'comparative_grade': cgrade,
          'total_scanned': str(numOfCountries) ,
          'n':str(numOfBlocked),
          'c':countryDict['country__name'],
          'alpha2': countryDict['country__alpha2'],
          'alpha3': countryDict['country__alpha3']})

		seq= [x['comparative_grade'] for x in terms if x['comparative_grade']!=1]
		if seq:
			mseq = max(seq)
			for d in terms:
				if d['comparative_grade']==1:
					continue
				d['comparative_grade'] /= (mseq*(10.0/7))'''
			
		result['terms']=terms

		'''data={}
		fills = {0: 'Hdfbfa2', 1: 'Hd5aa95', 2:'Hca9587',3:'Hc08079',4:'Hb56a6b', 5:'Haa555d',6:'Ha0404f',7:'H952b42',8:'H8b1534',9:'H800026'}

		for d in terms:
			if 0.1 > d['comparative_grade'] >= 0 : data[d['alpha3']] = {"fillKey": fills[0]}
			if 0.2 > d['comparative_grade'] > 0.1 : data[d['alpha3']] = {"fillKey": fills[1]}
			if 0.3 > d['comparative_grade'] > 0.2 : data[d['alpha3']] = {"fillKey": fills[2]}
			if 0.4 > d['comparative_grade'] > 0.3 : data[d['alpha3']] = {"fillKey": fills[3]}
			if 0.5 > d['comparative_grade'] > 0.4 : data[d['alpha3']] = {"fillKey": fills[4]}
			if 0.6 > d['comparative_grade'] > 0.5 : data[d['alpha3']] = {"fillKey": fills[5]}
			if 0.7 > d['comparative_grade'] > 0.6 : data[d['alpha3']] = {"fillKey": fills[6]}
			if 0.8 > d['comparative_grade'] > 0.7 : data[d['alpha3']] = {"fillKey": fills[7]}
			if 0.9 > d['comparative_grade'] > 0.8 : data[d['alpha3']] = {"fillKey": fills[8]}
			if d['comparative_grade'] > 0.9 : data[d['alpha3']] = {"fillKey": fills[9]}

		#terms.append({'n':"How many", 'c':'in your country?'})
		result['data']=data'''

		'''lastReport = UrlReport.objects.latest('epoch')
		dateString =  datetime.fromtimestamp(lastReport.epoch).strftime('%Y-%m-%d')
		try:
			countryString = lastReport.uid.chosen_country.name
		except:
			countryString = "United States"
		result['last_reporter'] = "{0} {1}".format(dateString, countryString)'''
		result['last_reporter']="2014-08-28 South Korea"
		result['hard'] = True
		result['server_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		#top_news=News.objects.all()[:10]
		#result['news']= [{"news_title": n.title, "description": n.description, "link":n.getUrl(), "agency":n.agency} for n in top_news]
		
		return HttpResponse(json.dumps(result, indent=2), content_type="application/json")
	else:
		return HttpResponse(json.dumps({'status':'ERROR', 'message':'wrong params.'}, indent=2), content_type="application/json")
