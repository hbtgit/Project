import ifcopenshell
from imports import *

# class IFCProcessor:

#     def __init__(self, ifc_path):
#         self.ifc_path = ifc_path
#         self.ifc_file = None if not ifc_path else ifcopenshell.open(ifc_path)

#     def extract_element_counts(self):
#         return {
#             'IfcBeam': len(self.ifc_file.by_type('IfcBeam')),
#             'IfcColumn': len(self.ifc_file.by_type('IfcColumn'))
#         }

#     def extract_ifc_data(self):
#         total_weight = 0.0
#         for quantity in self.ifc_file.by_type('IfcQuantityWeight'):
#             if quantity:
#                 total_weight += quantity.WeightValue
#         return round(total_weight, 2)

#     def extract_section_types(self):
#         section_types = set()
#         for element in self.ifc_file.by_type('IfcStructuralProfileProperties'):
#             section_types.add(element.ProfileName)
#         for element in self.ifc_file.by_type('IfcCShapeProfileDef'):
#             section_types.add(element.ProfileName)
#         return section_types

#     def extract_aux_data(self):
#         aux_data = {}
#         for element in self.ifc_file.by_type('IfcStructuralProfileProperties'):
#             section_name = element.ProfileName
#             if section_name not in aux_data:
#                 aux_data[section_name] = {'count': 0, 'total_weight': 0.0}
#             aux_data[section_name]['count'] += 1
#         for element in self.ifc_file.by_type('IfcQuantityWeight'):
#             section_name = element.Name
#             if section_name in aux_data:
#                 aux_data[section_name]['total_weight'] += element.WeightValue
#         for key in aux_data:
#             aux_data[key]['total_weight'] = round(aux_data[key]['total_weight'], 2)
#         total_stud_count = sum(data['count'] for data in aux_data.values())
#         return total_stud_count, aux_data

#     def extract_floor_data(self):
#         return len(self.ifc_file.by_type('IfcBuildingStorey'))

#     def extract_forces_moments(self):
#         forces, moments = {}, {}
#         schema = self.ifc_file.schema
#         if schema == "IFC2X3":
#             print("Using schema IFC2X3")
#             return forces, moments
#         elif schema.startswith("IFC4"):
#             print("Using schema IFC4")
#             force_pattern = re.compile(r'IFCFORCEVECTOR\(([^,]+),([^,]+),([^,]+)\);')
#             moment_pattern = re.compile(r'IFCMOMENTVECTOR\(([^,]+),([^,]+),([^,]+)\);')
#             floor_pattern = re.compile(r'#\d+=\s*IFCBUILDINGSTOREY\(([^,]+),')
#             current_floor = "Foundation"

#             for line in open(self.ifc_path, 'r'):
#                 floor_match = floor_pattern.search(line)
#                 if floor_match:
#                     current_floor = floor_match.group(1).strip("'")
#                     if current_floor not in forces:
#                         forces[current_floor] = np.zeros(3)
#                         moments[current_floor] = np.zeros(3)
#                 force_match = force_pattern.search(line)
#                 if force_match:
#                     force_values = list(map(float, force_match.groups()))
#                     forces[current_floor] += np.array(force_values)
#                 moment_match = moment_pattern.search(line)
#                 if moment_match:
#                     moment_values = list(map(float, moment_match.groups()))
#                     moments[current_floor] += np.array(moment_values)
#             return forces, moments
#         else:
#             raise ValueError(f"Unsupported IFC schema: {schema}")

# def parse_ifc_file(self):
#     coordinates = []
#     for point in self.ifc_file.by_type('IfcCartesianPoint'):
#         coord_tuple = tuple(point.Coordinates)
#         if len(coord_tuple) == 3:
#             coordinates.append(tuple(round(x / 12, 2) for x in coord_tuple))
#     return coordinates




class IFCProcessor:
    def __init__(self, ifc_path):
        self.ifc_path = ifc_path
        self.ifc_file = None if not ifc_path else ifcopenshell.open(ifc_path)

    def extract_element_counts(self):
        if not self.ifc_file:
            raise ValueError("IFC file is not loaded.")
        return {
            'IfcBeam': len(self.ifc_file.by_type('IfcBeam')),
            'IfcColumn': len(self.ifc_file.by_type('IfcColumn'))
        }

    def extract_ifc_data(self):
        if not self.ifc_file:
            raise ValueError("IFC file is not loaded.")
        total_weight = 0.0
        for quantity in self.ifc_file.by_type('IfcQuantityWeight'):
            if quantity:
                total_weight += quantity.WeightValue
        return round(total_weight, 2)

    def extract_section_types(self):
        if not self.ifc_file:
            raise ValueError("IFC file is not loaded.")
        section_types = set()
        for element in self.ifc_file.by_type('IfcStructuralProfileProperties'):
            section_types.add(element.ProfileName)
        for element in self.ifc_file.by_type('IfcCShapeProfileDef'):
            section_types.add(element.ProfileName)
        return section_types

    def extract_aux_data(self):
        if not self.ifc_file:
            raise ValueError("IFC file is not loaded.")
        aux_data = {}
        for element in self.ifc_file.by_type('IfcStructuralProfileProperties'):
            section_name = element.ProfileName
            if section_name not in aux_data:
                aux_data[section_name] = {'count': 0, 'total_weight': 0.0}
            aux_data[section_name]['count'] += 1
        for element in self.ifc_file.by_type('IfcQuantityWeight'):
            section_name = element.Name
            if section_name in aux_data:
                aux_data[section_name]['total_weight'] += element.WeightValue
        for key in aux_data:
            aux_data[key]['total_weight'] = round(aux_data[key]['total_weight'], 2)
        total_stud_count = sum(data['count'] for data in aux_data.values())
        return total_stud_count, aux_data

    def extract_floor_data(self):
        if not self.ifc_file:
            raise ValueError("IFC file is not loaded.")
        return len(self.ifc_file.by_type('IfcBuildingStorey'))
    

    def extract_forces_moments(self):
        if not self.ifc_file:
            raise ValueError("IFC file is not loaded.")
        forces, moments = {}, {}
        schema = self.ifc_file.schema
        if schema == "IFC2X3":
            print("Using schema IFC2X3")
            return forces, moments
        elif schema.startswith("IFC4"):
            print("Using schema IFC4")
            force_pattern = re.compile(r'IFCFORCEVECTOR\(([^,]+),([^,]+),([^,]+)\);')
            moment_pattern = re.compile(r'IFCMOMENTVECTOR\(([^,]+),([^,]+),([^,]+)\);')
            floor_pattern = re.compile(r'#\d+=\s*IFCBUILDINGSTOREY\(([^,]+),')
            current_floor = "Foundation"

            for line in open(self.ifc_path, 'r'):
                floor_match = floor_pattern.search(line)
                if floor_match:
                    current_floor = floor_match.group(1).strip("'")
                    if current_floor not in forces:
                        forces[current_floor] = np.zeros(3)
                        moments[current_floor] = np.zeros(3)
                force_match = force_pattern.search(line)
                if force_match:
                    force_values = list(map(float, force_match.groups()))
                    forces[current_floor] += np.array(force_values)
                moment_match = moment_pattern.search(line)
                if moment_match:
                    moment_values = list(map(float, moment_match.groups()))
                    moments[current_floor] += np.array(moment_values)
            return forces, moments
        else:
            raise ValueError(f"Unsupported IFC schema: {schema}")

    def parse_ifc_file(self):
        if not self.ifc_file:
            raise ValueError("IFC file is not loaded.")
        coordinates = []
        for point in self.ifc_file.by_type('IfcCartesianPoint'):
            coord_tuple = tuple(point.Coordinates)
            if len(coord_tuple) == 3:
                coordinates.append(tuple(round(x / 12, 2) for x in coord_tuple))
        return coordinates
        # return "Coordinates"

        