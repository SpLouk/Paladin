#!/usr/bin/env python

import argparse
import json
import os
import requests

with open('api_key') as f:
  API_KEY = f.readline().strip()

def get_course_info(term, subject, course_number):
  URL = 'https://api.uwaterloo.ca/v2/terms/{term}/{subject}/enrollment.json?key={key}'.format(term=term, subject=subject, key=API_KEY)
  response = json.loads(requests.get(URL).text)

  lectures = []
  for lec in response.get('data'):
    if lec.get('catalog_number') == course_number and lec.get('section').startswith('LEC'):
      lectures.append(lec)
  return lectures

def main():
  parser = argparse.ArgumentParser(description='Interact with UW API')
  parser.add_argument('-t', '--term', help='School term', default='1179', required=False)
  parser.add_argument('-s', '--subject', help='School subject', default='CS', required=False)
  parser.add_argument('-c', '--code', help='Course code', required=True)
  args = parser.parse_args()
  lectures = get_course_info(args.term, args.subject, args.code)
  for lec in lectures:
    print '{0} / {1}'.format(lec.get('enrollment_total'), lec.get('enrollment_capacity'))

if __name__ == "__main__":
  main()
