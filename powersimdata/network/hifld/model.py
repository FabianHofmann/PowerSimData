import os

from powersimdata.input.abstract_grid import AbstractGrid
from powersimdata.network.constants.storage import storage


class HIFLD(AbstractGrid):
    """HIFLD network.

    :param str/iterable interconnect: interconnect name(s).
    """

    def __init__(self, interconnect):
        """Constructor."""
        model = "hifld"
        super().__init__()

        self._set_data_loc(os.path.dirname(__file__))
        self._build_network(interconnect, model)
        self.storage.update(storage[model])
