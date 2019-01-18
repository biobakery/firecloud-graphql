
# Firecloud GraphQl

To install: 
`` $ pip install firecloud flask graphene>=2.0.0 flask-graphql ``

To run:
`` $ python server.py ``

* Remember to set the env variable to the service account key location.
* `$ export GOOGLE_APPLICATION_CREDENTIALS=~/compute_engine_service_account_key/biom-mass-8dc9ab934396.json`
* Also if using install with virtual env source it first.
* `$ source ~/firecloud-tools/.firecloud-tools/venv/bin/activate `

Examples (prior to stub for gcd changes):

* An example query is
```
{ entitiesWithType(namespace:"biom-mass-firecloud-lauren",workspace:"test_api") {
  attributes 
 }
}
```

* Get example with url
```
$ wget "http://34.73.242.142:5000/graphql?query=%7B%20entitiesWithType(namespace%3A%22biom-mass-firecloud-lauren%22%2Cworkspace%3A%22test_api%22)%20%7B%0A%20%20attributes%20%0A%20%7D%0A%7D"
```

* Example output is

```
{"data":{"entitiesWithType":[{"attributes":"X(nickname=u'father', family=u'CEU_Trio')"},{"attributes":"X(nickname=u'mother', f
amily=u'CEU_Trio')"},{"attributes":"X(nickname=u'son', family=u'CEU_Trio')"}]}}
```
