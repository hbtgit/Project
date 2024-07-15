from ifc_processing import IFCProcessor
from load_calculations import LoadCalculator
from plotting import Plotter
from reporting import ReportGenerator
from imports import *

def main(ifc_path, report_path):
    ifc_processor = IFCProcessor(ifc_path)
    load_calculator = LoadCalculator()
    plotter = Plotter()
    report_generator = ReportGenerator(report_path)

    # Extract data from IFC file
    element_counts = ifc_processor.extract_element_counts()
    total_weight = ifc_processor.extract_ifc_data()
    section_types = ifc_processor.extract_section_types()
    total_stud_count, aux_data = ifc_processor.extract_aux_data()
    total_floors = ifc_processor.extract_floor_data()
    forces, moments = ifc_processor.extract_forces_moments()
    coordinates = ifc_processor.parse_ifc_file()

    # Perform load calculations
    total_beam_weight, total_column_weight = load_calculator.calculate_beam_column_weight(ifc_processor)
    area_xy, area_yz, area_xz = load_calculator.calculate_area_from_coords(coordinates)
    footing_perimeter = load_calculator.calculate_footing_perimeter(coordinates)
    roof_perimeter = load_calculator.calculate_roof_perimeter(coordinates)
    wall_moments = load_calculator.calculate_wall_moments(100.0, 10.0)
    load_area = load_calculator.calculate_load_area(coordinates, 50.0, 20.0)

    # Generate plots
    plotter.plot_aux_data(aux_data)
    plotter.plot_load_distribution(list(forces.keys()), list(forces.values()), list(moments.values()))

    # Generate PDF report
    report_generator.add_title("IFC Report")
    report_generator.add_section("Element Counts", str(element_counts))
    report_generator.add_section("Total Weight", str(total_weight))
    report_generator.add_section("Section Types", str(section_types))
    report_generator.add_section("Auxiliary Data", str(aux_data))
    report_generator.add_section("Total Stud Count", str(total_stud_count))
    report_generator.add_section("Total Floors", str(total_floors))
    report_generator.add_section("Forces", str(forces))
    report_generator.add_section("Moments", str(moments))
    report_generator.add_section("Coordinates", str(coordinates))
    report_generator.add_section("Total Beam Weight", str(total_beam_weight))
    report_generator.add_section("Total Column Weight", str(total_column_weight))
    report_generator.add_section("Area (XY, YZ, XZ)", f"{area_xy}, {area_yz}, {area_xz}")
    report_generator.add_section("Footing Perimeter", str(footing_perimeter))
    report_generator.add_section("Roof Perimeter", str(roof_perimeter))
    report_generator.add_section("Wall Moments", str(wall_moments))
    report_generator.add_section("Load Area", str(load_area))

    report_generator.save()

if __name__ == "__main__":
    # Replace with actual paths
    main("path_to_ifc_file.ifc", "path_to_report.pdf")
