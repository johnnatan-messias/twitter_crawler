class EventType(object):
    SEARCH_TWEET = {'type': 'search', 'path': '/search/tweets'}
    SEARCH_USER = {'type': 'users', 'path': '/users/search'}
    FRIENDS_ID = {'type': 'friends', 'path': '/friends/ids'}
    RETWEETS_ID = {'type': 'statuses', 'path': '/statuses/retweets/:id'}
