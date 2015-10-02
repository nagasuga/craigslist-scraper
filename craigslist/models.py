from collections import namedtuple


Entry = namedtuple('Entry',
                   ['updated', 'summary', 'url', 'title', 'id', 'published',
                    'image'],
                   verbose=True)
