try:
    from groupbyrule.comparator._comparator import Comparator, StringComparator
    from groupbyrule.comparator._levenshtein import Levenshtein
except:
    from .levenhstein import Comparator, Levenshtein
