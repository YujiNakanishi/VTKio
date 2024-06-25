import numpy as np

"""
---version2---
version2形式のVTKジオメトリに関するクラス

att:
    geom_type -> <str> VTKジオメトリフォーマット名
"""
class version2:
    geom_type = None

    def __init__(self, point_data = [], cell_data = []):
        self.point_data = point_data
        self.cell_data = cell_data

    @property
    def __version__(self) -> int: return 2
    @property
    def dim(self) -> int: raise NotImplementedError
    @property
    def num_points(self) -> int: raise NotImplementedError
    @property
    def num_cells(self) -> int: raise NotImplementedError

    def add_pointdata(self, name : str, values : np.ndarray):
        assert len(values) == self.num_points
        if len(values.shape) == 1:
            self.point_data.append({"name" : name, "values" : values, "type" : "scalar"})
        else:
            self.point_data.append({"name" : name, "values" : values, "type" : "vector"})
    
    def add_celldata(self, name : str, values : np.ndarray):
        assert len(values) == self.num_cells
        if len(values.shape) == 1:
            self.cell_data.append({"name" : name, "values" : values, "type" : "scalar"})
        else:
            self.cell_data.append({"name" : name, "values" : values, "type" : "vector"})


    """
    DATASET部分の記述
    """
    def write_dataset(self, filename : str):
        raise NotImplementedError
    
    def write_scalar(self, name : str, values : np.ndarray, filename : str):
        with open(filename, "a") as file:
            file.write("SCALARS {} float 1\n".format(name))
            file.write("LOOKUP_TABLE default\n")
            for v in values:
                file.write("{}\n".format(v))
    
    def np2str(self, L : np.ndarray):
        s = str(L[0])
        for l in L[1:]:
            s += " " + str(l)
        
        return s + "\n"
    
    def write_vector(self, name : str, values : np.ndarray, filename : str):
        _values = np.concatenate((values, np.zeros((len(values), 1))), axis = 1) if self.dim == 2 else values
        
        with open(filename, "a") as file:
            file.write("VECTORS {} float\n".format(name))
            for v in _values:
                file.write(self.np2str(v))


    def write_pointdata(self, filename : str):
        if not self.point_data: return
        with open(filename, "a") as file:
            file.write("POINT_DATA {}\n".format(self.num_points))
        
        for point_data in self.point_data:
            if point_data["type"] == "scalar":
                self.write_scalar(point_data["name"], point_data["values"], filename)
            else:
                self.write_vector(point_data["name"], point_data["values"], filename)
    
    def write_celldata(self, filename : str):
        if not self.cell_data: return
        with open(filename, "a") as file:
            file.write("CELL_DATA {}\n".format(self.num_cells))

        for cell_data in self.cell_data:
            if cell_data["type"] == "scalar":
                self.write_scalar(cell_data["name"], cell_data["values"], filename)
            else:
                self.write_vector(cell_data["name"], cell_data["values"], filename)

    
    def write(self, filename : str):
        with open(filename, "w") as file:
            file.write("# vtk DataFile Version 2.0\n")
            file.write("VTKio\n")
            file.write("ASCII\n")
            file.write("DATASET {}\n".format(self.geom_type))
        self.write_dataset(filename)
        self.write_pointdata(filename)
        self.write_celldata(filename)
