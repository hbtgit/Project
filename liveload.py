import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend

import ifcopenshell
import re
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay, ConvexHull
from tkinter import Tk, messagebox, Label, Checkbutton, BooleanVar, Entry
from tkinterdnd2 import TkinterDnD, DND_FILES
import os
from fpdf import FPDF
import tkinter as tk
from tkinter import simpledialog

def live_load_widget(floor_count):
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

    return live_loads


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


def extract_element_counts(ifc_path):
    """Extracts the counts of specific elements from an IFC file."""
    ifc_file = ifcopenshell.open(ifc_path)
    element_counts = {
        'IfcBeam': len(ifc_file.by_type('IfcBeam')),
        'IfcColumn': len(ifc_file.by_type('IfcColumn'))
    }
    return element_counts


def extract_ifc_data(ifc_path):
    """Extracts IFC data and calculates the total weight from an IFC file using ifcopenshell."""
    total_weight = 0.0
    ifc_file = ifcopenshell.open(ifc_path)
    for quantity in ifc_file.by_type('IfcQuantityWeight'):
        if quantity:
            total_weight += quantity.WeightValue
    return round(total_weight, 2)

def extract_section_types(ifc_path):
    """Extracts unique section types from an IFC file using ifcopenshell."""
    section_types = set()
    ifc_file = ifcopenshell.open(ifc_path)
    for element in ifc_file.by_type('IfcStructuralProfileProperties'):
        section_types.add(element.ProfileName)
    for element in ifc_file.by_type('IfcCShapeProfileDef'):
        section_types.add(element.ProfileName)
    return section_types

def extract_Aux_data(ifc_path):
    """Extracts auxiliary data (section counts and weights) from an IFC file using ifcopenshell."""
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

def extract_floor_data(ifc_path):
    """Extracts floor data to determine the number of stories in the building using ifcopenshell."""
    ifc_file = ifcopenshell.open(ifc_path)
    floors = len(ifc_file.by_type('IfcBuildingStorey'))
    return floors


def extract_forces_moments(ifc_path):
    """Extracts total forces and moments from an IFC file."""
    forces = {}
    moments = {}

    # Load the IFC file
    ifc_file = ifcopenshell.open(ifc_path)
    
    # Check the schema of the IFC file
    schema = ifc_file.schema

    # Define patterns based on schema
    if schema == "IFC2X3":
        # If the schema is IFC2X3, handle accordingly
        print("Using schema IFC2X3")
        # You may need to use different entity names or extraction methods
        # Currently, there's no direct equivalent for IfcForceVector and IfcMomentVector in IFC2X3
        # Hence, we would need to understand the exact requirement and map them accordingly
        return forces, moments
    elif schema.startswith("IFC4"):
        # If the schema is IFC4 or any of its derivatives
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

def parse_ifc_file(ifc_path):
    """Parses the IFC file to extract 3D coordinates using ifcopenshell."""
    coordinates = []
    ifc_file = ifcopenshell.open(ifc_path)
    for point in ifc_file.by_type('IfcCartesianPoint'):
        coord_tuple = tuple(point.Coordinates)
        if len(coord_tuple) == 3 and (not remove_zero_point_var.get() or coord_tuple != (0.0, 0.0, 0.0)):
            coordinates.append(tuple(round(x / 12, 2) for x in coord_tuple))
    return coordinates

# The rest of the functions remain unchanged
# ...

def calculate_beam_column_weight(ifc_path):
    """Calculate the total weight of beams and columns using 'Gross Weight' or 'IFCQUANTITYLENGTH'."""
    total_beam_weight = 0.0
    total_column_weight = 0.0

    ifc_file = ifcopenshell.open(ifc_path)

    # Helper function to get weight value
    def get_weight_value(element, attribute_names):
        for attr_name in attribute_names:
            attr_value = getattr(element, attr_name, None)
            if attr_value:
                return attr_value
        return 0.0

    # Define attribute names to check for weight values
    weight_attributes = ['GrossWeight', 'WeightValue']

    # Iterate over beams
    for beam in ifc_file.by_type('IfcBeam'):
        for quantity in beam.IsDefinedBy:
            if quantity.is_a('IfcRelDefinesByProperties'):
                prop_set = quantity.RelatingPropertyDefinition
                if prop_set.is_a('IfcElementQuantity'):
                    for quantity in prop_set.Quantities:
                        if quantity.is_a('IfcQuantityWeight') or quantity.Name == 'Gross Weight':
                            total_beam_weight += get_weight_value(quantity, weight_attributes)

    # Iterate over columns
    for column in ifc_file.by_type('IfcColumn'):
        for quantity in column.IsDefinedBy:
            if quantity.is_a('IfcRelDefinesByProperties'):
                prop_set = quantity.RelatingPropertyDefinition
                if prop_set.is_a('IfcElementQuantity'):
                    for quantity in prop_set.Quantities:
                        if quantity.is_a('IfcQuantityWeight') or quantity.Name == 'Gross Weight':
                            total_column_weight += get_weight_value(quantity, weight_attributes)

    return round(total_beam_weight, 2), round(total_column_weight, 2)

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

def calculate_footing_perimeter(coords):
    if len(coords) < 3:
        return []

    hull = ConvexHull(coords)
    perimeter_coords = [coords[vertex] for vertex in hull.vertices]

    return perimeter_coords

def calculate_wind_loads_and_present(wind_force, building_height, roof_perimeter, ifc_path):
    """
    Calculate and present wind loads on the building.
    """
    # Calculate wind pressure (force per unit length)
    wind_pressure = wind_force / roof_perimeter

    # Calculate wall moments due to wind force
    wall_moment = wind_pressure * building_height

    # Prepare the results
    results = {
        'Wind Force': wind_force,
        'Building Height': building_height,
        'Roof Perimeter': roof_perimeter,
        'Wind Pressure': round(wind_pressure, 2),
        'Wall Moment': round(wall_moment, 2)
    }

    # Print the results in a structured format
    print("Wind Load Calculation Results:")
    print(f"Wind Force: {results['Wind Force']} lbs")
    print(f"Building Height: {results['Building Height']} feet")
    print(f"Roof Perimeter: {results['Roof Perimeter']} feet")
    print(f"Wind Pressure: {results['Wind Pressure']} lbs/ft")
    print(f"Wall Moment: {results['Wall Moment']} ft-lbs")

    return results


def plot_coordinates(coordinates, areas, output_path, ifc_file_path):
    if not all(len(coord) == 3 for coord in coordinates):
        raise ValueError("Some coordinates do not have exactly three values.")

    x_vals = [coord[0] for coord in coordinates]
    y_vals = [coord[1] for coord in coordinates]
    z_vals = [coord[2] for coord in coordinates]

    # Determine max height for plot uniformity
    fac = 0.30 * max(max(z_vals), max(x_vals), max(y_vals))
    max_height = max(z_vals)
    max_width = max(y_vals)
    max_length = max(x_vals)

    max_hw = max(max_height, max_width) + fac
    min_hw = min(min(y_vals), min(z_vals)) - fac

    max_lw = max(max_length, max_width) + fac
    min_lw = min(min(y_vals), min(x_vals)) - fac

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 14), constrained_layout=True)
    axes = axes.flatten()  # Flatten the 2x2 grid to 1D for easier indexing

    sns.set(style="whitegrid")
    
    # Font settings
    title_fontsize = 14
    label_fontsize = 12
    tick_fontsize = 10

    # XZ Plane
    axes[0].plot(x_vals, z_vals, color='royalblue', linewidth=1)
    axes[0].set_title('XZ Plane (Feet)', fontsize=title_fontsize)
    axes[0].set_xlabel('X (feet)', fontsize=label_fontsize)
    axes[0].set_ylabel('Z (feet)', fontsize=label_fontsize)
    axes[0].axis('equal')
    axes[0].set_xlim([min_lw, max_lw])
    axes[0].set_ylim([min_hw, max_hw])
    axes[0].tick_params(axis='both', which='major', labelsize=tick_fontsize)

        # YZ Plane
    axes[1].plot(y_vals, z_vals, color='royalblue', linewidth=1)
    axes[1].set_title('YZ Plane (Feet)', fontsize=title_fontsize)
    axes[1].set_xlabel('Y (feet)', fontsize=label_fontsize)
    axes[1].set_ylabel('Z (feet)', fontsize=label_fontsize)
    axes[1].axis('equal')
    axes[1].set_xlim([min_lw, max_lw])
    axes[1].set_ylim([min_hw, max_hw])
    axes[1].tick_params(axis='both', which='major', labelsize=tick_fontsize)

    # XY Plane
    axes[2].plot(x_vals, y_vals, color='royalblue', linewidth=1)
    axes[2].set_title('XY Plane (Feet)', fontsize=title_fontsize)
    axes[2].set_xlabel('X (feet)', fontsize=label_fontsize)
    axes[2].set_ylabel('Y (feet)', fontsize=label_fontsize)
    axes[2].axis('equal')
    axes[2].set_xlim([min_lw, max_lw])
    axes[2].set_ylim([min_hw, max_hw])
    axes[2].tick_params(axis='both', which='major', labelsize=tick_fontsize)

    ww = extract_ifc_data(ifc_file_path)
    perimeter = calculate_perimeter(coordinates)
    footing_perimeter_coords = calculate_footing_perimeter(coordinates)

    # Plot Footing Perimeter

    footing_perimeter_coords = calculate_footing_perimeter(coordinates)

    if footing_perimeter_coords:
        x_vals_fp = [point[0] for point in footing_perimeter_coords] + [footing_perimeter_coords[0][0]]
        y_vals_fp = [point[1] for point in footing_perimeter_coords] + [footing_perimeter_coords[0][1]]
        #axes[2].plot(x_vals_fp, y_vals_fp, color='red', linewidth=1)

    # Aux Info
    axes[3].axis('off')
    axes[3].text(0.1, 0.9, f'XZ Area: {areas[2]} sq. feet', horizontalalignment='left', verticalalignment='center', fontsize=label_fontsize)
    axes[3].text(0.1, 0.8, f'YZ Area: {areas[1]} sq. feet', horizontalalignment='left', verticalalignment='center', fontsize=label_fontsize)
    axes[3].text(0.1, 0.7, f'XY Area: {areas[0]} sq. feet', horizontalalignment='left', verticalalignment='center', fontsize=label_fontsize)
    axes[3].text(0.1, 0.6, f'CFS Weight: {ww} lbs.', horizontalalignment='left', verticalalignment='center', fontsize=label_fontsize)
    axes[3].text(0.1, 0.5, f'Footing Perimeter: {perimeter} feet', horizontalalignment='left', verticalalignment='center', fontsize=label_fontsize)

    plt.savefig(output_path)
    # plt.show()

def calculate_linear_load(perimeter, roof_uplift, roof_downpressure):
    net_pressure = roof_downpressure - roof_uplift
    linear_load = net_pressure * perimeter
    return round(linear_load, 2)

def calculate_wall_moments(wind_force, height):
    moment = wind_force * height
    return round(moment, 2)

def calculate_roof_perimeter(coordinates):
    """Calculate the perimeter of the roof based on the given coordinates."""
    if not coordinates:
        return 0.0
    
    # Extract the Z-axis values
    z_vals = [coord[2] for coord in coordinates]
    
    # Find the maximum Z-axis value (highest elevation)
    max_z = max(z_vals)
    
    # Extract coordinates that are at the highest elevation
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

def calculate_dead_load(ifc_file):
    # Open the IFC file
    model = ifcopenshell.open(ifc_file)

    total_dead_load = 0.0

    for element in model.by_type('IfcElementQuantity'):
        for quantity in element.Quantities:
            if quantity.is_a('IfcQuantityWeight'):
                if 'Dead Load' in quantity.Name or 'DeadLoad' in quantity.Name or 'Gross Weight' in quantity.Name or 'GrossWeight' in quantity.Name:
                    total_dead_load += quantity.WeightValue

    return total_dead_load


def calculate_wind_loads(ifc_file):
    # Open the IFC file
    model = ifcopenshell.open(ifc_file)

    wind_pressure = 0.0
    wall_moment = 0.0

    # List of possible names for wind pressure and wall moment
    wind_pressure_names = ['Wind Pressure', 'WindPressure', 'Wind Load', 'WindLoad', 'Wind_Pressure', 'Wind_Load']
    wall_moment_names = ['Wall Moment', 'WallMoment', 'Wind Moment', 'WindMoment', 'Wall_Moment', 'Wind_Moment']

    for element in model.by_type('IfcElementQuantity'):
        for quantity in element.Quantities:
            # Check for wind pressure
            if any(name in quantity.Name for name in wind_pressure_names):
                if quantity.is_a('IfcQuantityArea'):
                    wind_pressure = quantity.AreaValue
                elif quantity.is_a('IfcQuantityLength'):
                    wind_pressure = quantity.LengthValue
                elif quantity.is_a('IfcQuantityVolume'):
                    wind_pressure = quantity.VolumeValue
                elif quantity.is_a('IfcQuantityForce'):
                    wind_pressure = quantity.ForceValue
                elif quantity.is_a('IfcQuantityPressure'):
                    wind_pressure = quantity.PressureValue

            # Check for wall moment
            if any(name in quantity.Name for name in wall_moment_names):
                if quantity.is_a('IfcQuantityArea'):
                    wall_moment = quantity.AreaValue
                elif quantity.is_a('IfcQuantityLength'):
                    wall_moment = quantity.LengthValue
                elif quantity.is_a('IfcQuantityVolume'):
                    wall_moment = quantity.VolumeValue
                elif quantity.is_a('IfcQuantityForce'):
                    wall_moment = quantity.ForceValue
                elif quantity.is_a('IfcQuantityMoment'):
                    wall_moment = quantity.MomentValue

    return {'Wind Pressure': wind_pressure, 'Wall Moment': wall_moment}

def calculate_snow_load(roof_area, snow_load_per_unit_area):
    """
    Calculate the total snow load on the roof.
    
    :param roof_area: Area of the roof in square feet.
    :param snow_load_per_unit_area: Snow load per unit area in lbs/sq. ft.
    :return: Total snow load in lbs.
    """
    total_snow_load = roof_area * snow_load_per_unit_area
    return round(total_snow_load, 2)

def calculate_ice_load(roof_area, ice_load_per_unit_area):
    """
    Calculate the total ice load on the roof.

    :param roof_area: Area of the roof in square feet.
    :param ice_load_per_unit_area: Ice load per unit area in lbs/sq. ft.
    :return: Total ice load in lbs.
    """
    total_ice_load = roof_area * ice_load_per_unit_area
    return round(total_ice_load, 2)


def create_Aux_pdf(element_counts, output_path, ifc_path, floor_count, forces, moments, perimeter, roof_uplift, roof_downpressure, wind_force, wall_height, roof_perimeter, areas, wind_loads, dead_load, total_column_weight, total_beam_weight, total_snow_load, total_ice_load):
    pdf = FPDF()
    multi_story_msg = "The building is a single story."
    if floor_count > 1:
        multi_story_msg = f"The building has {floor_count} stories."

    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Auxiliary Data", ln=True, align='C')

    for element_type, count in element_counts.items():
        pdf.cell(200, 10, txt=f'{element_type} Count: {count}', ln=True)

    pdf.cell(200, 10, txt=multi_story_msg, ln=True)
    pdf.cell(200, 10, txt=f'Total Beam Weight: {total_beam_weight} lbs', ln=True)
    pdf.cell(200, 10, txt=f'Total Column Weight: {total_column_weight} lbs', ln=True)

    for floor in forces:
        total_force = np.sum(forces[floor])
        total_moment = np.sum(moments[floor])
        pdf.cell(200, 10, txt=f'{floor} - Total Force: {total_force} N, Total Moment: {total_moment} Nm', ln=True)

    linear_load = calculate_linear_load(perimeter, roof_uplift, roof_downpressure)
    wall_moment = calculate_wall_moments(wind_force, wall_height)
    wind_pressure = wind_loads['Wind Pressure']

    pdf.cell(200, 10, txt=f'Estimated Linear Load on Perimeter: {linear_load} lbs/ft', ln=True)
    pdf.cell(200, 10, txt=f'Wall Moment from Wind: {wall_moment} Nm', ln=True)
    pdf.cell(200, 10, txt=f'Wind Pressure on Roof: {wind_pressure} lbs/ft²', ln=True)

    pdf.cell(200, 10, txt=f'Roof Perimeter: {roof_perimeter} feet', ln=True)
    pdf.cell(200, 10, txt=f'XZ Area: {areas[2]} sq. feet', ln=True)
    pdf.cell(200, 10, txt=f'YZ Area: {areas[1]} sq. feet', ln=True)
    pdf.cell(200, 10, txt=f'XY Area: {areas[0]} sq. feet', ln=True)

    pdf.cell(200, 10, txt="Wind Load Calculation Results:", ln=True)
    pdf.cell(200, 10, txt=f"Wind Pressure: {wind_loads['Wind Pressure']} lbs/ft", ln=True)
    pdf.cell(200, 10, txt=f"Wall Moment: {wind_loads['Wall Moment']} ft-lbs", ln=True)

    pdf.cell(200, 10, txt="Dead Load Calculation Results:", ln=True)
    pdf.cell(200, 10, txt=f"Total Dead Load: {dead_load} lbs", ln=True)

    pdf.cell(200, 10, txt="Snow Load Calculation Results:", ln=True)
    pdf.cell(200, 10, txt=f"Total Snow Load: {total_snow_load} lbs", ln=True)

    pdf.cell(200, 10, txt="Ice Load Calculation Results:", ln=True)
    pdf.cell(200, 10, txt=f"Total Ice Load: {total_ice_load} lbs", ln=True)

    pdf.output(output_path)

def on_drop(event):
    ifc_file_path = event.data.strip('{}')  # Remove curly braces if present
    coordinates = parse_ifc_file(ifc_file_path)
    areas = calculate_area_from_coords(coordinates)
    
    output_path = os.path.splitext(ifc_file_path)[0] + "_coordinate_plots.pdf"
    floor_count = extract_floor_data(ifc_file_path)
    forces, moments = extract_forces_moments(ifc_file_path)
    perimeter = calculate_perimeter(coordinates)
    roof_perimeter = calculate_roof_perimeter(coordinates)
    # Call the live_load_widget function to get live load inputs
    live_loads = live_load_widget(floor_count)
    # Process live loads if needed (e.g., print them or integrate into further calculations)
    print("Live Loads: ", live_loads)
    plot_coordinates(coordinates, areas, output_path, ifc_file_path)
    forces, moments = extract_forces_moments(ifc_file_path)
    perimeter = calculate_perimeter(coordinates)
    roof_perimeter = calculate_roof_perimeter(coordinates)
    
    plot_coordinates(coordinates, areas, output_path, ifc_file_path)
    print(f"Output saved to: {output_path}")
    Aux_output_path = os.path.splitext(ifc_file_path)[0] + "_Aux.pdf"
    
    roof_uplift = float(roof_uplift_entry.get())
    roof_downpressure = float(roof_downpressure_entry.get())
    wind_force = float(wind_force_entry.get())
    wall_height = float(wall_height_entry.get())
    
    try:
        snow_load_per_unit_area = float(snow_load_entry.get())  # Get the snow load per unit area
        ice_load_per_unit_area = float(ice_load_entry.get())  # Get the ice load per unit area
        roof_uplift_pressure = float(roof_uplift_entry.get())
        roof_downpressure = float(roof_downpressure_entry.get())
        wind_force = float(wind_force_entry.get())
        wall_height = float(wall_height_entry.get())
        
        # Continue with your logic
        # For example, you could calculate the snow load and display it
        snow_load_total = snow_load_per_unit_area * wall_height  # Example calculation
        # messagebox.showinfo("Snow Load", f"Total Snow Load: {snow_load_total} lbs")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers")
    snow_load_per_unit_area = float(snow_load_entry.get())  # Get the snow load per unit area
    ice_load_per_unit_area = float(ice_load_entry.get())  # Get the ice load per unit area
    # Calculate snow load
    roof_area = areas[0]  # Assuming the XY area is the roof area
    total_snow_load = calculate_snow_load(roof_area, snow_load_per_unit_area)
    ice_load_total = calculate_ice_load(roof_area, ice_load_per_unit_area)
    
    # Extract element counts
    element_counts = extract_element_counts(ifc_file_path)
    
    # Calculate wind loads
    wind_loads = calculate_wind_loads(ifc_file_path)
    
    # Calculate dead load
    dead_load = calculate_dead_load(ifc_file_path)
    
    # Calculate beam and column weights
    total_beam_weight, total_column_weight = calculate_beam_column_weight(ifc_file_path)
    create_Aux_pdf(element_counts, Aux_output_path, ifc_file_path, floor_count, forces, moments, perimeter, roof_uplift, roof_downpressure, wind_force, wall_height, roof_perimeter, areas, wind_loads, dead_load, total_column_weight, total_beam_weight, total_snow_load, ice_load_total)
    
    section_types = extract_section_types(ifc_file_path)
    
    multi_story_msg = "The building is a single story."
    if floor_count > 1:
        multi_story_msg = f"The building has {floor_count} stories."

    messagebox.showinfo("Info", f"Plot saved to {output_path}\nAuxiliary data saved to {Aux_output_path}")


def main():
    root = TkinterDnD.Tk()
    root.title("IFC to PDF Converter")
    root.geometry("400x500")
    global ice_load_entry, snow_load_entry, remove_zero_point_var, Imperial_var, roof_uplift_entry, roof_downpressure_entry, wind_force_entry, wall_height_entry
    label = Label(root, text="Drag and drop an IFC file here", width=40, height=10)
    label.pack(pady=10)

    # Add a label and entry field for snow load per unit area
    Label(root, text="Snow Load (lbs/sq. ft.):").pack(anchor='w')
    snow_load_entry = Entry(root)
    snow_load_entry.pack(anchor='w')
    Label(root, text="Ice Load (lbs/sq. ft.):").pack(anchor='w')
    ice_load_entry = Entry(root)
    ice_load_entry.pack(anchor='w')
    
    remove_zero_point_var = BooleanVar(value=False)
    checkbox = Checkbutton(root, text="Remove (0,0,0) Point", variable=remove_zero_point_var)
    checkbox.pack(anchor='w')
    
    Label(root, text="Roof Uplift Pressure (psf)").pack(anchor='w')
    roof_uplift_entry = Entry(root)
    roof_uplift_entry.pack(anchor='w')

    Label(root, text="Roof Downpressure (psf)").pack(anchor='w')
    roof_downpressure_entry = Entry(root)
    roof_downpressure_entry.pack(anchor='w')

    Label(root, text="Wind Force (lbs)").pack(anchor='w')
    wind_force_entry = Entry(root)
    wind_force_entry.pack(anchor='w')

    Label(root, text="Wall Height (feet)").pack(anchor='w')
    wall_height_entry = Entry(root)
    wall_height_entry.pack(anchor='w')
    
    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', on_drop)

    root.mainloop()

if __name__ == '__main__':
    main()