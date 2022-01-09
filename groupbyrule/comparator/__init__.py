try:  # C++ imports
    from groupbyrule.comparator._comparator import Comparator, StringComparator
    from groupbyrule.comparator._levenshtein import Levenshtein
    from groupbyrule.comparator._lcs import LCSDistance
except:
    import warnings
    warnings.warn(
        "Could not load C++ shared library. Using pure Python implementation instead.")
    from .comparator import Comparator, StringComparator
    from .levenhstein import Levenshtein
    from .lcs import LCSDistance
