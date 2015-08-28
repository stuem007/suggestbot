#!/usr/bin/env python
# -*- coding: utf-8  -*-
'''
Text recommender that uses CirrusSearch/ElasticSearch
and Borda count rank aggregation to recommend articles.
'''
import os
import sys
import codecs
import re
import operator
import itertools
import collections

#from Config import SuggestBotConfig

import logging

import pywikibot

class APITextRecommender:
    def __init__(self, config=None):
        """
        Instantiate an object of this class.

        @param config: SuggestBot configuration to use
        @type config: Config.SuggestBotConfig
        """

        '''self.config = config
        if self.config is None:
            self.config = SuggestBotConfig()'''

    def get_recs(self, user, lang, articles, params):
        """
        Find articles matching a given set of articles for a given user.

        @param user: username of the user we are recommending articles to
        @type user: unicode

        @param lang: language code of the Wikipedia we're recommending for
        @type lang: unicode

        @param articles: the articles the user has recently edited
        @type articles: list

        @param params: parameters for the recommendation
                       key:'nrecs', value:int => number of recs returned
        @type params: dict
        """

        # number of recommendations we'll return
        nrecs = 500; # default
        if 'nrecs' in params:
            nrecs = params['nrecs']

        # temporary result set
        recs = {};

        # statistics on timing
        numArticles = len(articles)

        # print got request info
        logging.info(u"got request for user {lang}:{username} to find {nrecs} recommend articles based on {num} articles".format(lang=lang, username=user, nrecs=nrecs, num=numArticles).encode('utf-8'))

        # initialize Pywikibot site
        site = pywikibot.Site(lang)

        # dict of resulting recommendations mapping titles to Borda scores
        # (as ints, defaults are 0)
        recs = collections.defaultdict(int)

        # query parameters:
        # action=query
        # list=search
        # srsearch=morelike:{title}
        # srnamespace=0 (is the default)
        # srlimit=50 (tested by trial & error, bots can get <= 500)
        # format=json

        # FIXME: start timing
        
        for page_title in articles:
            q = pywikibot.data.api.Request(site=site,
                                           action=u'query')
            q['list'] = u'search'
            # q['srbackend'] = u'CirrusSearch'
            q['srnamespace'] = 0
            # FIXME: add quotes around title and escape quotes in title?
            q['srsearch'] = u'morelike:{title}'.format(title=page_title)
            q['srlimit'] = 100
            reqdata = q.submit()

            if not u'query' in reqdata \
               or not u'search' in reqdata[u'query']:
                logging.warning(u'no results for query on {title}'.format(title=page_title).encode('utf-8'))
            else:
                results = reqdata['query']['search']
                # calculate a Borda score for each article (len(list) - rank)
                # and throw it into the result set.
                n = len(results)
                score = itertools.count(n, step=-1)
                for article in results:
                    s = next(score)
                    recs[article[u'title']] += s
                
                logging.info(u'completed fetching recommendations for {title}'.format(title=page_title).encode('utf-8'))
                logging.info(u'number of recommendations currently {0}'.format(len(recs)))

        # FIXME: end timing, write out if verbose

        # take out edits from results
        for page_title in articles:
            try:
                del(recs[page_title])
            except KeyError:
                pass

        # sort the results and iterate through to create a list of dictionaries
        resultRecs = [];
        for (pageTitle, score) in sorted(recs.items(),
                                         key=operator.itemgetter(1),
                                         reverse=True)[:nrecs]:
            resultRecs.append({'item': pageTitle,
                               'value': score});

        logging.info(u"returning {n} recommendations.\n".format(n=len(resultRecs)))
        logging.info(u"completed getting recs".encode('utf-8'))

        # OK, done, return
        return resultRecs
