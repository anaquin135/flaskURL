import random
import string

def randomizeKeyword(keyword):
    ADD_LEN = 5
    letters = string.ascii_lowercase
    resultStr = keyword + "-" + ''.join(random.choice(letters) for i in range(ADD_LEN))
    return resultStr