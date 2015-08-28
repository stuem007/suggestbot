from APITextRecommender import APITextRecommender


class ItemRecommender:
    def __init__(self, lang='en', revtable='revision_userindex',
                 nrecs=100,
                 exp_threshold=18):
        '''
        Instantiate an object for recommending collaborators.

        :param lang: default language we are recommeding for
        :type lang: str

        :param revtable: name of the table which holds revision data.
                         Because we query using usernames, the default
                         should be "revision_userindex" to use indexes properly.
        :type revtable: str

        :param nrecs: default number of recommended users
        :type nrecs: int

        :param exp_threshold: threshold for labelling user as experienced
        :type exp_threshold: int
        '''
        
        self.lang = lang
        self.revtable= revtable
        self.nrecs = nrecs
        self.exp_thresh = exp_threshold
        
    def recommend(self, contribs, username, lang, cutoff,
                  namespaces=["0"], nrecs=100):

        '''
        Find `nrecs` number of neighbours for a given user based on
        the overlap between their contributions.

        :param contribs: The user's contributions
        :type contribs: list

        :param username: Username of the user we're recommending for
        :type username: str

        :param lang: Language code of the Wikipedia we're working on
        :type lang: str

        :param cutoff: Date and time from when to start looking for revisions
        :type cutoff: datetime.datetime

        :param namespaces: Namespaces to base comparisons on
        :type namespaces: list of str

        :param nrecs: Number of recommendations we seek
        :type nrecs: int
        '''
        
        # Override default variables with supplied parameters
        self.cutoff = cutoff
        self.lang = lang
        self.nrecs = nrecs
        
        text_recommender = APITextRecommender()
        
        recs = text_recommender.get_recs(username, lang, contribs, {'nrecs':nrecs})
        
        return recs
            
            
            
            
