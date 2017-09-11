# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from redis import Redis

import datetime as dt
import json
import requests

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

candidates = [
    {
        'id': 'rauner',
        'name': u'Bruce Rauner',
        'party': 'r',
        'committeeId': 25185
    },
    {
        'id': 'biss',
        'name': u'Daniel Biss',
        'party': 'd',
        'committeeId': 23971
    },
    {
        'id': 'daiber',
        'name': u'Bob Daiber',
        'party': 'd',
        'committeeId': 32591
    },
    {
        'id': 'drury',
        'name': u'Scott Drury',
        'party': 'd',
        'committeeId': 23682
    },
    {
        'id': 'hardiman',
        'name': u'Tio Hardiman',
        'party': 'd',
        'committeeId': ''
   },
    {
        'id': 'kennedy',
        'name': u'Chris Kennedy',
        'party': 'd',
        'committeeId': 32590
    },
    {
        'id': 'paterakis',
        'name': u'Alex Paterakis',
        'party': 'd',
        'committeeId': 32289
    },
    {
        'id': 'pawar',
        'name': u'Ameya Pawar',
        'party': 'd',
        'committeeId': 32469
    },
    {
        'id': 'biss',
        'name': u'Daniel Biss',
        'party': 'd',
        'committeeId': 23971
    },
    {
        'id': 'pritzker',
        'name': u'J.B. Pritzker',
        'party': 'd',
        'committeeId': 32762
    },
]

# how long our cached items last
redisDuration = 3600 # one hour
# assume there will never be more than 1,000,000 expenditures (but you never know, amirite?)
apiLimit = 1000000
dateFormat = '%Y-%m-%dT%H:%M:%S'

def calculateSpendingDays(firstExpenditure):
    now = dt.datetime.now()
    then = dt.datetime.strptime(firstExpenditure, dateFormat)

    diff = now - then

    return diff.days


def calculateSpentPerDay(days, total):
    return total / days


def calculateSpentPerSecond(perDay):
    return perDay / 86400


# convenience during development/testing
@app.route('/clear', methods=['GET'])
def clear():
    for c in candidates:
        redis.delete(c.get('id'))

    return 'cache cleared'


@app.route('/candidate/<string:candidate_nick>', methods=['GET'])
@cross_origin()
def get_candidate(candidate_nick):
    # find a matching committee_id
    committeeId = None

    # default to error message
    responseJSON = { 'error': 'Candidate not found' }

    for c in candidates:
        if c.get('id') == candidate_nick:
            committeeId = c.get('committeeId')
            break

    if committeeId:
        # try to pull data from redis
        cachedJSON = redis.get(candidate_nick)

        # if data found in redis, use it
        if cachedJSON:
            responseJSON = json.loads(cachedJSON)
        # if data not found in redis:
        else:
            # make API call
            response = requests.get('https://www.illinoissunshine.org/api/expenditures/?limit={}&committee_id={}'.format(apiLimit, committeeId))

            apiData = json.loads(json.dumps(response.json()))

            total = 0.0

            for expenditure in apiData['objects'][0]['expenditures']:
                total = total + float(expenditure['amount'])

            firstExpenditure = apiData['objects'][0]['expenditures'][-1]['expended_date']
            spendingDays = calculateSpendingDays(firstExpenditure)
            spentPerDay = calculateSpentPerDay(spendingDays, total)

            responseJSON = {
                'total': "{0:.2f}".format(total),
                'expendituresCount': len(apiData['objects'][0]['expenditures']),
                'firstExpenditure': firstExpenditure,
                'spendingDays': spendingDays,
                'spentPerDay': "{0:.2f}".format(spentPerDay),
                'spentPerSecond': "{0:.2f}".format(calculateSpentPerSecond(spentPerDay)),
                'timestamp': dt.datetime.strftime(dt.datetime.now(), dateFormat)
            }

            # store API call results in redis for one hour
            redis.setex(candidate_nick, json.dumps(responseJSON), redisDuration)

    # return JSON data about requested candidate *or* error message
    return jsonify(responseJSON)


# might as well have something on the home page, eh?
@app.route('/')
def index():
    hits = redis.get('indexhits')

    if (hits and int(hits) > 100):
        strang = 'You know why you visited this time, but what do you think the other {} visits were about?'.format(hits - 1)
    else:
        strang = 'My, how nice of you to visit.'

    redis.incr('indexhits')

    return strang


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
