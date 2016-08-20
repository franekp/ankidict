import sys
import os

sys.path = [
    os.path.dirname(__file__),
    os.path.join(os.path.dirname(__file__), 'thirdparty'),
] + sys.path

# sys.path.append(os.path.dirname(__file__))
# sys.path.append(os.path.join(os.path.dirname(__file__), 'thirdparty'))
