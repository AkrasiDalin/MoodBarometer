# Author Dalin Akrasi
# Student no.1528923
#
#
#
#

import re
def tokenize(string):
    return re.findall("([a-zA-Z'-]+)",string)

def filterTokens(tokens_array):
    return [x for x in tokens_array if len(x) > 2]
