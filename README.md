# VTKio
VTKio is a python module for "i"nput/"o"utput of "VTK". Even though there are many great modules for some geometry file formats including VTK (e.g., pyVista), VTKio is much simpler module than others.  

VTKio can handle STRUCTURED_POINTS and UNSTRUCTURED_GRIDS now.

## Features
VTKio is for VTK version 2 legacy file foramt. However, this will be able to be used for other versions.  

VTKio module is organized by mainly two python code written below.
### core.py
Fundamental functions and classes are defined in "core.py" file. If functions are called from other files in VTKio, or a classes are inherited, you had write these here. Now, only version2 class which is a fundamental class in VTKio is defined.

### geom.py
classes for STRUCTURED_POINTS and UNSTRUCTURED_GRIDS are defined in "geom.py". If you want other geometry formats, you should define new class with inheriting version2 in core.py.

## Examples
### structured_points
```python
import VTKio
import numpy as np

##### Define a geomtry
nx, ny, nx = 10, 10, 10
num_grids = (nx, ny, nz)
origin = (0., 0., 0.)
spacing = (1., 1., 1.)
g = VTKio.structured_points(num_grids, origin, spacing)

##### add scalar point data
g.add_pointdata("point_scalar", np.random.rand(nx, ny, nz))

##### add vector point data
g.add_pointdata("point_vector", np.random.rand(nx, ny, nz, 3))

##### add scalar cell data
g.add_celldata("cell_scalar", np.random.rand(nx-1, ny-1, nz-1))

g.write("test.vtk")
```
### point_cloud
```python
import VTKio
import numpy as np

##### Define a geomtry
points = np.random.rand(100, 3)
geom = VTKio.point_cloud(points)

geom.write("test.vtk")
```