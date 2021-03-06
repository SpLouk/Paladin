#!/usr/bin/env python

import argparse
import json
import os
import requests
import quest_driver

def get_course_info(term, subject, course_number, api_key):
  url = 'https://api.uwaterloo.ca/v2/terms/{term}/{subject}/enrollment.json?key={key}'.format(term=term, subject=subject, key=api_key)
  response = json.loads(requests.get(url).text)

  lectures = []
  for lec in response.get('data'):
    if lec.get('catalog_number') == course_number and lec.get('section').startswith('LEC'):
      lectures.append(lec)
  return lectures

def main():
  parser = argparse.ArgumentParser(description='Pull class info form the UW API. Automatically enroll in classes')
  parser.add_argument('-t', '--term', help='School term', default='1179', required=False)
  parser.add_argument('-s', '--subject', help='School subject', default='CS', required=False)
  parser.add_argument('-n', '--number', help='Course number', required=True)
  parser.add_argument('-e', '--enroll', help='Attempt to enroll if course has openings', action='store_true', default=False)
  parser.add_argument('-c', '--credentials', help='JSON file with UW API key and Quest login credentials if enroll is true', required=True)
  args = parser.parse_args()

  credentials = json.loads(open(os.path.expanduser(args.credentials)).read())
  lectures = get_course_info(args.term, args.subject, args.number, credentials.get('api_key'))
  for lec in lectures:
    if args.enroll:
      if lec.get('enrollment_total') < lec.get('enrollment_capacity'):
        print 'Attempting to enroll in course {0}.'.format(lec.get('class_number'))
        res = quest_driver.add_class(credentials.get('username'), credentials.get('password'), lec.get('class_number'))
        if res:
          print 'Success! You are now enrolled in {0}.'.format(lec.get('class_number'))
          return
        else:
          print 'Could not enroll.'
      else:
        print '{0} is full.'.format(lec.get('class_number'))
    else:
      print '\n{0} {1} ({2})'.format(lec.get('subject'), lec.get('catalog_number'), lec.get('class_number'))
      print 'Enrollment: {0}/{1}'.format(lec.get('enrollment_total'), lec.get('enrollment_capacity'))
      print 'Last Updated: {0}'.format(lec.get('last_updated'))

if __name__ == "__main__":
  main()
