import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend

import ifcopenshell
import re
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay, ConvexHull
import os
from fpdf import FPDF
import tkinter as tk
from tkinter import simpledialog

## Function to collect live load data
# def live_load_widget(floor_count):
#     live_loads = []

#     # Create the main window
#     root = tk.Tk()
#     root.withdraw()  # Hide the main window

#     # Loop through each floor and get user input for live loads
#     for floor in range(1, floor_count + 1):
#         load_info = {}
#         load_info['floor'] = floor
        
#         # Prompt for percentage load type
#         load_info['percentage_load'] = simpledialog.askfloat(
#             f"Floor {floor}",
#             f"Enter the live load as a percentage for floor {floor}:"
#         )

#         # Prompt for area load type
#         load_info['area_load'] = simpledialog.askfloat(
#             f"Floor {floor}",
#             f"Enter the live load as an area (in square feet) for floor {floor}:"
#         )

#         live_loads.append(load_info)

#     # Destroy the main window after getting inputs
#     root.destroy()

#     return live_loads
def live_load_widget(length, width, occupancy_type, importance_factor,floor_count
                     ):
    """
    Calculates the live loads for a given building area.

    Parameters:
    length (float): The length of the building area in meters.
    width (float): The width of the building area in meters.
    occupancy_type (str): The type of occupancy for the building area.
    importance_factor (float): The importance factor for the building area.

    Returns:
    float: The calculated live load in kN/m^2.
    """
    live_loads = []

    # Create the main window
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Loop through each floor and get user input for live loads
    for floor in range(1, floor_count + 1):
        load_info = {}
        load_info['floor'] = floor
        
        # Prompt for percentage load type
        load_info['percentage_load'] = simpledialog.askfloat(
            f"Floor {floor}",
            f"Enter the live load as a percentage for floor {floor}:"
        )

        # Prompt for area load type
        load_info['area_load'] = simpledialog.askfloat(
            f"Floor {floor}",
            f"Enter the live load as an area (in square feet) for floor {floor}:"
        )

        live_loads.append(load_info)

    # Destroy the main window after getting inputs
    root.destroy()
    live_load = calculate_live_loads(length, width, occupancy_type, importance_factor)
    return live_load

def calculate_live_loads(length, width, occupancy_type, importance_factor):
    """
    Calculates the live loads for a given building area.

    Parameters:
    length (float): The length of the building area in meters.
    width (float): The width of the building area in meters.
    occupancy_type (str): The type of occupancy for the building area.
    importance_factor (float): The importance factor for the building area.

    Returns:
    float: The calculated live load in kN/m^2.
    """
    # Implement the live load calculation logic here
    # Based on the provided parameters and relevant standards/regulations
    live_load = 5.0  # Example calculation
    return live_load


# Function to explore IFC properties (remains unchanged)
def explore_ifc_properties(ifc_path):
    import ifcopenshell
    ifc_file = ifcopenshell.open(ifc_path)

    for element in ifc_file.by_type('IfcElement'):
        material_set = element.IsDefinedBy
        if material_set:
            for definition in material_set:
                if definition.is_a('IfcRelDefinesByProperties'):
                    property_set = definition.RelatingPropertyDefinition
                    if property_set.is_a('IfcPropertySet'):
                        print(f"Element: {element.GlobalId}")
                        for prop in property_set.HasProperties:
                            if prop.is_a('IfcPropertySingleValue'):
                                print(f"Property Name: {prop.Name}, Value: {prop.NominalValue}")

# Function to extract element counts (remains unchanged)
def extract_element_counts(ifc_path):
    ifc_file = ifcopenshell.open(ifc_path)
    element_counts = {
        'IfcBeam': len(ifc_file.by_type('IfcBeam')),
        'IfcColumn': len(ifc_file.by_type('IfcColumn'))
    }
    return element_counts

# Function to extract IFC data (remains unchanged)
def extract_ifc_data(ifc_path):
    total_weight = 0.0
    ifc_file = ifcopenshell.open(ifc_path)
    for quantity in ifc_file.by_type('IfcQuantityWeight'):
        if quantity:
            total_weight += quantity.WeightValue
    return round(total_weight, 2)

# Function to extract section types (remains unchanged)
def extract_section_types(ifc_path):
    section_types = set()
    ifc_file = ifcopenshell.open(ifc_path)
    for element in ifc_file.by_type('IfcStructuralProfileProperties'):
        section_types.add(element.ProfileName)
    for element in ifc_file.by_type('IfcCShapeProfileDef'):
        section_types.add(element.ProfileName)
    return section_types

# Function to extract auxiliary data (remains unchanged)
def extract_Aux_data(ifc_path):
    Aux_data = {}
    ifc_file = ifcopenshell.open(ifc_path)
    for element in ifc_file.by_type('IfcStructuralProfileProperties'):
        section_name = element.ProfileName
        if section_name not in Aux_data:
            Aux_data[section_name] = {'count': 0, 'total_weight': 0.0}
        Aux_data[section_name]['count'] += 1
    for element in ifc_file.by_type('IfcQuantityWeight'):
        section_name = element.Name
        if section_name in Aux_data:
            Aux_data[section_name]['total_weight'] += element.WeightValue
    for key in Aux_data:
        Aux_data[key]['total_weight'] = round(Aux_data[key]['total_weight'], 2)
    total_stud_count = sum(data['count'] for data in Aux_data.values())
    return total_stud_count, Aux_data

# Function to extract floor data (remains unchanged)
def extract_floor_data(ifc_path):
    ifc_file = ifcopenshell.open(ifc_path)
    floors = len(ifc_file.by_type('IfcBuildingStorey'))
    return floors

# Function to extract forces and moments (remains unchanged)
def extract_forces_moments(ifc_path):
    forces = {}
    moments = {}

    ifc_file = ifcopenshell.open(ifc_path)
    schema = ifc_file.schema

    if schema == "IFC2X3":
        print("Using schema IFC2X3")
        return forces, moments
    elif schema.startswith("IFC4"):
        print("Using schema IFC4")
        force_pattern = re.compile(r'IFCFORCEVECTOR\(([^,]+),([^,]+),([^,]+)\);')
        moment_pattern = re.compile(r'IFCMOMENTVECTOR\(([^,]+),([^,]+),([^,]+)\);')
        floor_pattern = re.compile(r'#\d+=\s*IFCBUILDINGSTOREY\(([^,]+),')

        current_floor = "Foundation"

        for line in open(ifc_path, 'r'):
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

# Function to parse IFC file (remains unchanged)
def parse_ifc_file(ifc_path):
    coordinates = []
    ifc_file = ifcopenshell.open(ifc_path)
    for point in ifc_file.by_type('IfcCartesianPoint'):
        coord_tuple = tuple(point.Coordinates)
        if len(coord_tuple) == 3 and coord_tuple != (0.0, 0.0, 0.0):
            coordinates.append(tuple(round(x / 12, 2) for x in coord_tuple))
    return coordinates

# Function to calculate beam and column weight (remains unchanged)
def calculate_beam_column_weight(ifc_path):
    total_beam_weight = 0.0
    total_column_weight = 0.0

    ifc_file = ifcopenshell.open(ifc_path)

    def get_weight_value(element, attribute_names):
        for attr_name in attribute_names:
            attr_value = getattr(element, attr_name, None)
            if attr_value:
                return attr_value
        return 0.0

    weight_attributes = ['GrossWeight', 'WeightValue']

    for beam in ifc_file.by_type('IfcBeam'):
        for quantity in beam.IsDefinedBy:
            if quantity.is_a('IfcRelDefinesByProperties'):
                prop_set = quantity.RelatingPropertyDefinition
                if prop_set.is_a('IfcElementQuantity'):
                    for quantity in prop_set.Quantities:
                        if quantity.is_a('IfcQuantityWeight') or quantity.Name == 'Gross Weight':
                            total_beam_weight += get_weight_value(quantity, weight_attributes)

    for column in ifc_file.by_type('IfcColumn'):
        for quantity in column.IsDefinedBy:
            if quantity.is_a('IfcRelDefinesByProperties'):
                prop_set = quantity.RelatingPropertyDefinition
                if prop_set.is_a('IfcElementQuantity'):
                    for quantity in prop_set.Quantities:
                        if quantity.is_a('IfcQuantityWeight') or quantity.Name == 'Gross Weight':
                            total_column_weight += get_weight_value(quantity, weight_attributes)

    return round(total_beam_weight, 2), round(total_column_weight, 2)

# Function to calculate area from coordinates (remains unchanged)
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
        return round(area, 2)

    if len(coords[0]) == 2:
        area = triangulation_area(coords)
    elif len(coords[0]) == 3:
        unique_z = np.unique(coords[:, 2])
        if len(unique_z) == 1:
            coords_2d = coords[:, :2]
            area = triangulation_area(coords_2d)
        else:
            area = sum(triangulation_area(coords[coords[:, 2] == z][:, :2]) for z in unique_z)
    else:
        raise ValueError("Invalid coordinate dimensions")

    return area

# Function to create PDF report
def create_pdf_report(output_path, analysis_results, live_loads):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for key, value in analysis_results.items():
        if isinstance(value, dict):
            pdf.cell(0, 10, key, ln=True, align='L')
            for sub_key, sub_value in value.items():
                pdf.cell(0, 10, f"  {sub_key}: {sub_value}", ln=True, align='L')
        else:
            pdf.cell(0, 10, f"{key}: {value}", ln=True, align='L')

    # Add live load data to the PDF
    pdf.add_page()
    pdf.cell(0, 10, "Live Load Data", ln=True, align='C')
    for load in live_loads:
        floor = load['floor']
        percentage_load = load['percentage_load']
        area_load = load['area_load']
        pdf.cell(0, 10, f"Floor {floor}:", ln=True, align='L')
        pdf.cell(0, 10, f"  Percentage Load: {percentage_load}%", ln=True, align='L')
        pdf.cell(0, 10, f"  Area Load: {area_load} sq.ft.", ln=True, align='L')

    pdf.output(output_path)

# Main workflow to analyze IFC file and create the PDF report
def main(ifc_path, output_pdf_path):
    coordinates = parse_ifc_file(ifc_path)
    area = calculate_area_from_coords(coordinates)
    element_counts = extract_element_counts(ifc_path)
    total_weight = extract_ifc_data(ifc_path)
    section_types = extract_section_types(ifc_path)
    total_stud_count, aux_data = extract_Aux_data(ifc_path)
    floors = extract_floor_data(ifc_path)
    forces, moments = extract_forces_moments(ifc_path)
    total_beam_weight, total_column_weight = calculate_beam_column_weight(ifc_path)
    live_loads = live_load_widget(floors)  # Collect live load data

    analysis_results = {
        'Area (sq.ft)': area,
        'Element Counts': element_counts,
        'Total Weight (lbs)': total_weight,
        'Section Types': section_types,
        'Total Stud Count': total_stud_count,
        'Auxiliary Data': aux_data,
        'Floor Count': floors,
        'Total Beam Weight (lbs)': total_beam_weight,
        'Total Column Weight (lbs)': total_column_weight,
        'Forces (lbs)': forces,
        'Moments (lbs*ft)': moments
    }

    create_pdf_report(output_pdf_path, analysis_results, live_loads)

# Example usage
ifc_path = 'path_to_your_ifc_file.ifc'
output_pdf_path = 'auxiliary_report.pdf'
main(ifc_path, output_pdf_path)
