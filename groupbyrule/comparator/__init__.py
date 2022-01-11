try:  # C++ imports
    from groupbyrule.comparator._comparator import Comparator, StringComparator
    from groupbyrule.comparator._levenshtein import Levenshtein
    from groupbyrule.comparator._lcs import LCSDistance
    from groupbyrule.comparator._dameraulevenshtein import DamerauLevenshtein
    from groupbyrule.comparator._jaro import Jaro
    from groupbyrule.comparator._jarowinkler import JaroWinkler
except:
    import warnings
    warnings.warn(
        "Could not load C++ shared library. Using pure Python implementation instead.")
    from .comparator import Comparator, StringComparator
    from .levenhstein import Levenshtein
    from .lcs import LCSDistance
    from .dameraulevenshtein import DamerauLevenshtein
    from .jaro import Jaro
    from .jarowinkler import JaroWinkler
