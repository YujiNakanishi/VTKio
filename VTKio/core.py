import numpy as np

"""
---version2---
version2形式のVTKジオメトリに関するクラス

att:
    geom_type -> <str> VTKジオメトリフォーマット名
    point_data -> <list:dict> 節点物理量データ。dictのkeyは下記の通り。
        "name" -> <str> 物理量名
        "values" -> <np.ndarray, (n, ) or (n, D)> 各節点の物理量。ここでnは節点数。ベクトルデータとスカラーデータにのみ対応。
        "type" -> <str> ("scalar", "vector") 物理量のタイプ
    cell_data -> <list> 節点物理量データ。dictのkeyはpoint_dataと同様。

Note:
    geom.pyにあるクラスに継承されることを想定
"""
class version2:
    geom_type = None

    def __init__(self, point_data = [], cell_data = []):
        self.point_data = point_data
        self.cell_data = cell_data

    """version情報を返す"""
    @property
    def __version__(self) -> int: return 2
    
    """次元数を返す"""
    @property
    def dim(self) -> int: raise NotImplementedError
    
    """節点数を返す"""
    @property
    def num_points(self) -> int: raise NotImplementedError
    
    """セル数を返す"""
    @property
    def num_cells(self) -> int: raise NotImplementedError

    """
    節点物理量の追加

    input:
        name -> <str> 物理量名
        values -> <np.ndarray:float:(num_points, ) or (num_points, dim)> 各節点の物理量

    Note:
        行っていることはpoint_data(list)にdictをappendしているに過ぎない。
        ただ、dictの構造(どういったkeyを持っているか)を本モジュール利用者が意識させないために、本関数を用意。
        つまり、「どういったkeyを有するdictをappendさせるか?」と考えさせるよりも、引数として必要情報を明示させた。
    """
    def add_pointdata(self, name : str, values : np.ndarray) -> None:
        assert len(values) == self.num_points
        if len(values.shape) == 1:
            self.point_data.append({"name" : name, "values" : values, "type" : "scalar"})
        else:
            self.point_data.append({"name" : name, "values" : values, "type" : "vector"})
    
    """
    セル物理量の追加

    input:
        name -> <str> 物理量名
        values -> <np.ndarray:float:(num_cells, ) or (num_cells, dim)> 各節点の物理量
    
    Note:
        関数"add_pointdata"と同様に、cell_dataにdictをappendさせる代わりに、本関数を用意。
    """
    def add_celldata(self, name : str, values : np.ndarray) -> None:
        assert len(values) == self.num_cells
        if len(values.shape) == 1:
            self.cell_data.append({"name" : name, "values" : values, "type" : "scalar"})
        else:
            self.cell_data.append({"name" : name, "values" : values, "type" : "vector"})


    """DATASET部分の記述"""
    def write_dataset(self, filename : str):
        raise NotImplementedError
    
    """SCALARS部分の記述"""
    def write_scalar(self, name : str, values : np.ndarray, filename : str):
        with open(filename, "a") as file:
            file.write("SCALARS {} float 1\n".format(name))
            file.write("LOOKUP_TABLE default\n")
            for v in values:
                file.write("{}\n".format(v))
    
    """
    下記のようにnp.ndarrayからstrを返す

    >>a = np.array([1,2,3])
    >>np2str(a)
    "1 2 3\n"
    """
    def np2str(self, L : np.ndarray):
        s = str(L[0])
        for l in L[1:]:
            s += " " + str(l)
        
        return s + "\n"
    
    """VECTORS部分の記述"""
    def write_vector(self, name : str, values : np.ndarray, filename : str):
        _values = np.concatenate((values, np.zeros((len(values), 1))), axis = 1) if self.dim == 2 else values
        
        with open(filename, "a") as file:
            file.write("VECTORS {} float\n".format(name))
            for v in _values:
                file.write(self.np2str(v))

    """POINT_DATAの記述"""
    def write_pointdata(self, filename : str):
        if not self.point_data: return
        with open(filename, "a") as file:
            file.write("POINT_DATA {}\n".format(self.num_points))
        
        for point_data in self.point_data:
            if point_data["type"] == "scalar":
                self.write_scalar(point_data["name"], point_data["values"], filename)
            else:
                self.write_vector(point_data["name"], point_data["values"], filename)
    
    """CELL_DATAの記述"""
    def write_celldata(self, filename : str):
        if not self.cell_data: return
        with open(filename, "a") as file:
            file.write("CELL_DATA {}\n".format(self.num_cells))

        for cell_data in self.cell_data:
            if cell_data["type"] == "scalar":
                self.write_scalar(cell_data["name"], cell_data["values"], filename)
            else:
                self.write_vector(cell_data["name"], cell_data["values"], filename)

    
    """
    vtkファイルの書き込み

    input:
        filename -> <str>ファイル名
    """
    def write(self, filename : str) -> None:
        with open(filename, "w") as file:
            file.write("# vtk DataFile Version 2.0\n")
            file.write("VTKio\n")
            file.write("ASCII\n")
            file.write("DATASET {}\n".format(self.geom_type))
        self.write_dataset(filename)
        self.write_pointdata(filename)
        self.write_celldata(filename)