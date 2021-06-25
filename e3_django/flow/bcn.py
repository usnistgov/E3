class PV:
    def discount(self, v, t, d, n=None):
        """
        Override in subclass to provide different discounting strategies.

        :return: A list of discounted values over time.
        """


class SPV(PV):
    def discount(self, F_t, t, d, n=None):
        return F_t / ((1 + d) ^ t)


class UPV(PV):
    def discount(self, A_0, t, d, n=0):
        return A_0 * (((1 + d) ^ n - 1) / (d * (1 + d) ^ t))
