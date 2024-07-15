import numpy as np
from imports import *

class LoadCalculator:
    @staticmethod
    def calculate_beam_column_weight(ifc_processor):
        total_beam_weight, total_column_weight = 0.0, 0.0

        def get_weight_value(element, attribute_names):
            for attr_name in attribute_names:
                attr_value = getattr(element, attr_name, None)
                if attr_value:
                    return attr_value
            return 0.0

        weight_attributes = ['GrossWeight', 'WeightValue']

        for beam in ifc_processor.ifc_file.by_type('IfcBeam'):
            for quantity in beam.IsDefinedBy:
                if quantity.is_a('IfcRelDefinesByProperties'):
                    prop_set = quantity.RelatingPropertyDefinition
                    if prop_set.is_a('IfcElementQuantity'):
                        for quantity in prop_set.Quantities:
                            if quantity.is_a('IfcQuantityWeight') or quantity.Name == 'Gross Weight':
                                total_beam_weight += get_weight_value(quantity, weight_attributes)

        for column in ifc_processor.ifc_file.by_type('IfcColumn'):
            for quantity in column.IsDefinedBy:
                if quantity.is_a('IfcRelDefinesByProperties'):
                    prop_set = quantity.RelatingPropertyDefinition
                    if prop_set.is_a('IfcElementQuantity'):
                        for quantity in prop_set.Quantities:
                            if quantity.is_a('IfcQuantityWeight') or quantity.Name == 'Gross Weight':
                                total_column_weight += get_weight_value(quantity, weight_attributes)

        return round(total_beam_weight, 2), round(total_column_weight, 2)

    @staticmethod
    def calculate_area_from_coords(coord_list):
        coords = np.array(coord_list)

        def triangulation_area(points):
            if len(points) < 3:
                return 0.0
            tri = Delaunay(points)
            area = 0.0
            for simplex in tri.simplices:
                pts = points[simplex]
                a = np.linalg.norm(pts[0] - pts[1])
                b = np.linalg.norm(pts[1] - pts[2])
                c = np.linalg.norm(pts[2] - pts[0])
                s = (a + b + c) / 2
                area += np.sqrt(s * (s - a) * (s - b) * (s - c))
            return round(area, 1)

        area_xy = triangulation_area(coords[:, [0, 1]])
        area_yz = triangulation_area(coords[:, [1, 2]])
        area_xz = triangulation_area(coords[:, [0, 2]])

        return area_xy, area_yz, area_xz

    @staticmethod
    def calculate_perimeter(coords):
        if len(coords) < 3:
            return 0.0
        hull = ConvexHull(coords)
        perimeter = 0.0
        for simplex in hull.simplices:
            p1 = np.array(coords[simplex[0]])
            p2 = np.array(coords[simplex[1]])
            perimeter += np.linalg.norm(p1 - p2)
        return round(perimeter / 12, 1)

    @staticmethod
    def calculate_footing_perimeter(coords):
        if len(coords) < 3:
            return []

        hull = ConvexHull(coords)
        perimeter_coords = [coords[vertex] for vertex in hull.vertices]

        return perimeter_coords

    @staticmethod
    def calculate_linear_load(perimeter, roof_uplift, roof_downpressure):
        net_pressure = roof_downpressure - roof_uplift
        return round(net_pressure * perimeter, 2)

    @staticmethod
    def calculate_wall_moments(wind_force, height):
        return round(wind_force * height, 2)

    @staticmethod
    def calculate_roof_perimeter(coordinates):
        if not coordinates:
            return 0.0

        z_vals = [coord[2] for coord in coordinates]
        max_z = max(z_vals)
        roof_coords = [coord[:2] for coord in coordinates if coord[2] == max_z]

        if len(roof_coords) < 3:
            return 0.0

        perimeter = 0.0
        num_points = len(roof_coords)

        for i in range(num_points):
            x1, y1 = roof_coords[i]
            x2, y2 = roof_coords[(i + 1) % num_points]
            distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            perimeter += distance

        return round(perimeter, 2)

    @staticmethod
    def calculate_load_area(coords, snow_load, dead_load):
        xy_area, _, _ = LoadCalculator.calculate_area_from_coords(coords)
        total_load = (snow_load + dead_load) * xy_area
        return round(total_load, 2)
