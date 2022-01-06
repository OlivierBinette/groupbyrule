from abc import ABC, abstractmethod


class Comparator(ABC):

    @abstractmethod
    def compare(e1, e2):
        """
        Comparison between two elements.

        Parameters
        ----------
        e1:
            element to compare from.
        e1:
            element to compare to.

        Returns
        -------
        Number indicating similarity level between the two elements. This is not necessarily normalized or symmetric.
        """
        pass

    @abstractmethod
    def elementwise(l1, l2):
        """
        Pairwise comparisons between two lists.

        Parameters
        ----------
        l1: list
            List of elements to compare from.
        l2: list
            List of elements to compare to.

        Returns
        -------
        Matrix of dimension len(l1)xlen(l2), where each row corresponds to an element of l1 and each column corresponds to an element of l2.
        """
        pass
