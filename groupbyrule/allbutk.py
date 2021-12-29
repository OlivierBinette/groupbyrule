from .any import Any
from .match import Match
import itertools


class AllButK(Any):

    def __init__(self, *args, k=0, level="groups"):
        rules = [Match(*x, level=level)
                 for x in itertools.combinations(args, len(args)-k)]
        super().__init__(*rules)
