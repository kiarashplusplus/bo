from django.db import models
from urlparse import urlparse, parse_qs
from django.core.validators import URLValidator
from datetime import datetime

_version = 1

_db_prefix = "bo_"

def lower_db_name(cls):
    cls._meta.db_table = _db_prefix + cls.__name__.lower()
    return cls

@lower_db_name
class ReporterUID(models.Model):

	uid = models.AutoField(primary_key=True)
	first_request = models.DateTimeField(default=datetime.now, auto_now_add=True)	
	chosen_country = models.ForeignKey('Country', related_name='chosen_country')
	email = models.TextField(blank=True, null=True)
	client = models.TextField(blank=True, null=True)
	ipidentity =  models.ForeignKey('IPidentity')


@lower_db_name
class IPidentity(models.Model):
	ip_add=models.GenericIPAddressField()
	country=models.ForeignKey('Country', related_name='country', blank=True, null=True)
	isp=models.TextField(blank=True, null=True)
	org=models.TextField(blank=True, null=True)
	region=models.TextField(blank=True, null=True)
	city=models.TextField(blank=True, null=True)
	zipcode=models.TextField(blank=True, null=True)
	lat=models.TextField(blank=True, null=True)
	lon=models.TextField(blank=True, null=True)

@lower_db_name
class UrlReport(models.Model):
	ipidentity = models.ForeignKey('IPidentity')
	uid = models.ForeignKey('ReporterUID', null=True, blank=True, default = None)
	url=models.ForeignKey('Url')
	epoch=models.IntegerField(blank=True, null=True)
	final_url=models.TextField(blank=True, null=True)
	length=models.IntegerField(blank=True, null=True)
	status_code=models.IntegerField(blank=True, null=True)
	elapsed=models.FloatField(blank=True, null=True)
	history=models.TextField(blank=True, null=True)
	headers=models.TextField(blank=True, null=True)
	cookies=models.TextField(blank=True, null=True)
	content=models.ForeignKey('PageContent',blank=True, null = True)

@lower_db_name
class ReportDecision(models.Model):
	report=models.ForeignKey('UrlReport')
	decision=models.IntegerField(default=100)  #down -> 11, timeout -> 0, blocked_small -> 31, blocked_redirected -> 32, open->1 
	flag=models.IntegerField(default=0)  #default 0, suspicious (not procesed) 1, approved 2, rejected 3, skipped -1

@lower_db_name
class UrlDecision(models.Model):
	country=models.ForeignKey('Country')
	url=models.ForeignKey('Url')
	proxydecision = models.IntegerField(default=100)  #0timeout #1open #2partially #3blocked #5 unknown #default  
	volunteerdecision = models.IntegerField(default=100)  #0timeout #1open #2partially #3blocked #5 unknown #default  
	decision = models.IntegerField(default=100)  #0timeout #1open #2partially #3blocked #5 unknown #default
	
@lower_db_name
class PageContent(models.Model):
	content=models.TextField(blank=True, null=True)

@lower_db_name
class Country(models.Model):
	alpha2=models.CharField(max_length=2)
	alpha3=models.CharField(max_length=3)
	name=models.TextField()
	official_name=models.TextField(blank=True, null=True)
	internet_code= models.TextField(blank=True, null=True)
	population=models.TextField(blank=True, null=True)
	population_with_internet=models.TextField(blank=True, null=True)
	upload_speed=models.TextField(blank=True, null=True)
	download_speed=models.TextField(blank=True, null=True)
	press_freedom_rank=models.IntegerField(blank=True, null=True)
	median_age=models.TextField(blank=True, null=True)

	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.name

@lower_db_name
class Word(models.Model):
	name=models.TextField()
	count=models.IntegerField(default=0)

@lower_db_name
class Url(models.Model):
	address=models.TextField(validators=[URLValidator()])
	base_url= models.ForeignKey('self', blank=True, null=True)

	category=models.TextField(blank=True, null=True, default='Unkown')
	language=models.TextField(blank=True, null=True)

	company_name=models.TextField(blank=True, null=True)
	location=models.TextField(blank=True, null=True)
	global_rank=models.IntegerField(blank=True, null=True)
	
	words_used=models.ManyToManyField(Word,blank=True, null=True, db_table = _db_prefix+"url_words_used")
	screenshot=models.TextField(blank=True, null=True)
	group=models.IntegerField(blank=True, null=True, default=0)  #2 need to be reviewed. #5 for no us data. #6 for moderation removed

	def save(self, *args, **kwargs): 
		self.full_clean()
		if self.address[-1]=='/': self.address=self.address[:-1]
		o = urlparse(self.address)
		base=o.scheme + "://" + o.netloc
		if not self.address==base:
			base_url,_=Url.objects.get_or_create(address=base)
			self.base_url=base_url
		super(Url, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.address

@lower_db_name
class News(models.Model):
	link_to_news=models.TextField(validators=[URLValidator()])
	title=models.TextField(blank=True, null=True)
	description=models.TextField(blank=True, null=True)
	agency=models.TextField(blank=True, null=True)
	country=models.ForeignKey('Country', blank=True, null=True)
	url=models.ForeignKey('Url', limit_choices_to={'base_url': None}, blank=True, null=True)
	published_date=models.DateField(blank=True, null=True)
	saved_date=models.DateTimeField(auto_now_add=True)

	def save(self, *args, **kwargs): 
		self.full_clean()
		super(News, self).save(*args, **kwargs)

	def getUrl(self, *args, **kwargs):
		return parse_qs(urlparse(self.link_to_news).query)['url']

	class Meta:
		ordering = ['-published_date']

	def __unicode__(self):
		return self.title+"----"+str(self.published_date)+"----"+str(self.country)+"----"+str(self.url)


