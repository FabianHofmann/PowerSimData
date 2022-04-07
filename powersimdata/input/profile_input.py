import pandas as pd

from powersimdata.input.input_base import InputBase

profile_kind = {
    "demand",
    "hydro",
    "solar",
    "wind",
    "demand_flexibility_up",
    "demand_flexibility_dn",
    "demand_flexibility_cost_up",
    "demand_flexibility_cost_dn",
}


class ProfileInput(InputBase):
    def __init__(self):
        """Constructor."""
        super().__init__()
        self._file_extension = {k: "csv" for k in profile_kind}

    def _get_file_path(self, scenario_info, field_name):
        """Get the file name and relative path for the given profile and
        scenario.

        :param dict scenario_info: metadata for a scenario.
        :param str field_name: the kind of profile.
        :return: (*tuple*) -- file name and list of path components.
        """
        if "demand_flexibility" in field_name:
            version = scenario_info[field_name]
        else:
            version = scenario_info["base_" + field_name]
        file_name = field_name + "_" + version + ".csv"
        grid_model = scenario_info["grid_model"]
        return "/".join(["raw", grid_model, file_name])

    def _read(self, f, path):
        data = pd.read_csv(f, index_col=0, parse_dates=True)
        if "demand_flexibility" in path:
            data.columns = data.columns.astype(str)
        else:
            data.columns = data.columns.astype(int)
        return data

    def get_profile_version(self, grid_model, kind):
        """Returns available raw profile from blob storage or local disk.

        :param str grid_model: grid model.
        :param str kind: *'demand'*, *'hydro'*, *'solar'*, *'wind'*,
            *'demand_flexibility_up'*, *'demand_flexibility_dn'*,
            *'demand_flexibility_cost_up'*, or *'demand_flexibility_cost_dn'*.
        :return: (*list*) -- available profile version.
        """
        return self.data_access.get_profile_version(grid_model, kind)
