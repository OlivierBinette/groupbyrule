from .any import Any
from .match import Match
import itertools


class AllButK(Any):

    def __init__(self, *args, k=0):
        rules = [Match(*x) for x in itertools.combinations(args, len(args)-k)]
        super().__init__(*rules)
