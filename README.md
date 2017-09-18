# PALADIN

## Conquer the University of Waterloo's Quest system

This program will tell you information about courses offered at the University of Waterloo,
and automatically enroll you in them.

All you need to do is supply a valid University of Waterloo API key. You can register
for one [here](https://uwaterloo.ca/api/register)

Example

```
./paladin.py -s CS -n 350 -c credentials.json

CS 350 (5943)
Enrollment: 76/75
Last Updated: 2017-09-14T13:01:17-04:00

CS 350 (6175)
Enrollment: 76/75
Last Updated: 2017-09-14T13:01:17-04:00

CS 350 (6225)
Enrollment: 75/75
Last Updated: 2017-09-14T13:01:17-04:00

CS 350 (6520)
Enrollment: 76/75
Last Updated: 2017-09-14T13:01:17-04:00

CS 350 (6521)
Enrollment: 75/75
Last Updated: 2017-09-14T13:01:17-04:00
```

## Installation

1. Install [Selenium](http://selenium-python.readthedocs.io/installation.html)
2. Clone this repo `git clone git@github.com:SpLouk/Paladin.git`
3. run `./paladin.py --help` to get started

## Auto-Enroll

If you would like to auto enroll in any available section of a given class, use the `-e` option,
and supply a username and password in your credentials.json file.

Example with auto-enroll:
```
./paladin.py -s ENGL -n 109 -e -c credentials.json 

3141 is full.
Attempting to enroll in course 3763.
Could not enroll.
3764 is full.
3765 is full.
3766 is full.
3767 is full.
3768 is full.
Attempting to enroll in course 3769.
Success! You are now enrolled in 3769.
```

## Credential File

Format of credentials.json:
```
{
  "username": "USERID",
  "password": "XXXX",
  "api_key": "00000000000000000000000000000000"
}
```
