"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
import requests
import functools
from requests.status_codes import codes

BASE_URL = 'http://debug.blockedonline.net'
URLS = ['http://blockedonline.com/blocked/data?url_query=google', 'http://blockedonline.com/blocked/data?url=http://images.google.com&v=0', 'http://blockedonline.com/blocked/data?url=http://images.google.com&v=1' ]

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

def assert_response_code(code=codes.OK):
  """
    Helper function to assert a
    certain status code as a response
  """
  def decorator(method):
    @functools.wraps(method)
    def wrapped(self, *args, **kwargs):
      res = method(self, *args, **kwargs)
      self.assertEqual(res.status_code, code)
      return res
    return wrapped
  return decorator

class SimpleTest(TestCase):

  @assert_response_code()
  def test_bs(self):
    for url in URLS:
      url = "%s/%s" % (BASE_URL, url)
      return requests.get(url)
