import numpy as np
from VTKio.core import *

class structured_points(version2):
    geom_type = "STRUCTURED_POINTS"
    def __init__(self, num_grids : tuple, origin : tuple = None, spacing : tuple = None, point_data = [], cell_data = []):
        super().__init__(point_data, cell_data)
        self.num_grids = num_grids
        self.origin = (0.,)*self.dim if origin is None else origin
        self.spacing = (1., )*self.dim if spacing is None else spacing
    
    @property
    def dim(self): return len(self.num_grids)
    @property
    def num_points(self):
        n = 1
        for g in self.num_grids: n *= g
        return n
    @property
    def num_cells(self):
        n = 1
        for g in self.num_grids: n *= (g - 1)
        return n
    
    def add_pointdata(self, name : str, values : np.ndarray):
        """
        structured_pointsに限りvaluesを(num_points, *)ではなく、(x, y, z, *)のshapeで定義。
        """
        assert values.shape[:self.dim] == self.num_grids
        if len(values.shape) == self.dim:
            self.point_data.append({"name" : name, "values" : values, "type" : "scalar"})
        else:
            self.point_data.append({"name" : name, "values" : values, "type" : "vector"})
    
    def add_celldata(self, name : str, values : np.ndarray):
        """
        add_pointdataと同様に、valuesの定義が他と異なる。
        """
        assert values.shape[:self.dim] == tuple((ng - 1 for ng in self.num_grids))
        if len(values.shape) == self.dim:
            self.cell_data.append({"name" : name, "values" : values, "type" : "scalar"})
        else:
            self.cell_data.append({"name" : name, "values" : values, "type" : "vector"})

    
    def write_scalar(self, name : str, values : np.ndarray, filename : str):
        _values = (values.T).flatten()
        with open(filename, "a") as file:
            file.write("SCALARS {} float 1\n".format(name))
            file.write("LOOKUP_TABLE default\n")
            for v in _values:
                file.write("{}\n".format(v))
    
    def write_vector(self, name : str, values : np.ndarray, filename : str):
        if self.dim == 2:
            _values = (values.transpose((1, 0, 2))).reshape((-1, 2))
            _values = np.concatenate(
                (_values, np.zeros((len(_values), 1))),
                axis = 1
                )
        else:
            _values = (values.transpose((2, 1, 0, 3))).reshape((-1, 3))
        with open(filename, "a") as file:
            file.write("VECTORS {} float\n".format(name))
            for v in _values:
                file.write(self.np2str(v))
    
    def write_dataset(self, filename : str):
        if self.dim == 2:
            num_grids = (self.num_grids[0], self.num_grids[1], 1)
            origin = (self.origin[0], self.origin[1], 0.)
            spacing = (self.spacing[0], self.spacing[1], 0.)
        else:
            num_grids = self.num_grids
            origin = self.origin
            spacing = self.spacing
        
        with open(filename, "a") as file:
            file.write("DIMENSIONS {0} {1} {2}\n".format(num_grids[0], num_grids[1], num_grids[2]))
            file.write("ORIGIN {0} {1} {2}\n".format(origin[0], origin[1], origin[2]))
            file.write("SPACING {0} {1} {2}\n".format(spacing[0], spacing[1], spacing[2]))