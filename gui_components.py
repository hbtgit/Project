# import tkinter as tk
# from tkinter import simpledialog, messagebox, Label, Checkbutton, BooleanVar, Entry
# from tkinterdnd2 import TkinterDnD, DND_FILES
# from imports import *

# class Application(tk.Frame):
#     def __init__(self, master, ifc_processor, load_calculator, plotter, report_generator):
#         super().__init__(master)
#         self.master = master
#         self.ifc_processor = ifc_processor
#         self.load_calculator = load_calculator
#         self.plotter = plotter
#         self.self.report_generator = report_generator
#         self.init_gui()
    
#     def init_gui(self):
#         self.master.title('IFC Processing Tool')
#         self.master.geometry('500x300')
#         self.create_widgets()

#     def create_widgets(self):
#         self.label = Label(self.master, text="Drag and drop an IFC file here.")
#         self.label.pack(padx=10, pady=10)

#         self.button_frame = tk.Frame(self.master)
#         self.button_frame.pack(padx=10, pady=10)

#         self.process_button = tk.Button(self.button_frame, text="Process IFC", command=self.process_ifc)
#         self.process_button.pack(side="left", padx=5, pady=5)

#         self.generate_report_button = tk.Button(self.button_frame, text="Generate Report", command=self.generate_report)
#         self.generate_report_button.pack(side="left", padx=5, pady=5)

#         self.file_label = Label(self.master, text="", wraplength=400)
#         self.file_label.pack(padx=10, pady=10)

#         self.master.drop_target_register(DND_FILES)
#         self.master.dnd_bind('<<Drop>>', self.on_drop)

#     def on_drop(self, event):
#         file_path = event.data
#         self.file_label.config(text=f"File selected: {file_path}")
#         self.ifc_processor.ifc_path = file_path

#     def process_ifc(self):
#         element_counts = self.ifc_processor.extract_element_counts()
#         total_weight = self.ifc_processor.extract_ifc_data()
#         section_types = self.ifc_processor.extract_section_types()
#         total_stud_count, aux_data = self.ifc_processor.extract_aux_data()
#         total_floors = self.ifc_processor.extract_floor_data()
#         forces, moments = self.ifc_processor.extract_forces_moments()
#         coordinates = self.ifc_processor.parse_ifc_file()

#         # Perform load calculations
#         total_beam_weight, total_column_weight = self.load_calculator.calculate_beam_column_weight(self.ifc_processor)
#         area_xy, area_yz, area_xz = self.load_calculator.calculate_area_from_coords(coordinates)
#         footing_perimeter = self.load_calculator.calculate_footing_perimeter(coordinates)
#         roof_perimeter = self.load_calculator.calculate_roof_perimeter(coordinates)
#         wall_moments = self.load_calculator.calculate_wall_moments(100.0, 10.0)
#         load_area = self.load_calculator.calculate_load_area(coordinates, 50.0, 20.0)

#         self.plotter.plot_aux_data(aux_data)
#         self.plotter.plot_load_distribution(list(forces.keys()), list(forces.values()), list(moments.values()))

#     def generate_report(self):
#         element_counts = self.ifc_processor.extract_element_counts()
#         total_weight = self.ifc_processor.extract_ifc_data()
#         section_types = self.ifc_processor.extract_section_types()
#         total_stud_count, aux_data = self.ifc_processor.extract_aux_data()
#         total_floors = self.ifc_processor.extract_floor_data()
#         forces, moments = self.ifc_processor.extract_forces_moments()
#         coordinates = self.ifc_processor.parse_ifc_file()

#         # Perform load calculations
#         total_beam_weight, total_column_weight = self.load_calculator.calculate_beam_column_weight(self.ifc_processor)
#         area_xy, area_yz, area_xz = self.load_calculator.calculate_area_from_coords(coordinates)
#         footing_perimeter = self.load_calculator.calculate_footing_perimeter(coordinates)
#         roof_perimeter = self.load_calculator.calculate_roof_perimeter(coordinates)
#         wall_moments = self.load_calculator.calculate_wall_moments(100.0, 10.0)
#         load_area = self.load_calculator.calculate_load_area(coordinates, 50.0, 20.0)

#         self.report_generator.add_title("IFC Report")
#         self.report_generator.add_section("Element Counts", str(element_counts))
#         self.report_generator.add_section("Total Weight", str(total_weight))
#         self.report_generator.add_section("Section Types", str(section_types))
#         self.report_generator.add_section("Auxiliary Data", str(aux_data))
#         self.report_generator.add_section("Total Stud Count", str(total_stud_count))
#         self.report_generator.add_section("Total Floors", str(total_floors))
#         self.report_generator.add_section("Forces", str(forces))
#         self.report_generator.add_section("Moments", str(moments))
#         self.report_generator.add_section("Coordinates", str(coordinates))
#         self.report_generator.add_section("Total Beam Weight", str(total_beam_weight))
#         self.report_generator.add_section("Total Column Weight", str(total_column_weight))
#         self.report_generator.add_section("Area (XY, YZ, XZ)", f"{area_xy}, {area_yz}, {area_xz}")
#         self.report_generator.add_section("Footing Perimeter", str(footing_perimeter))
#         self.report_generator.add_section("Roof Perimeter", str(roof_perimeter))
#         self.report_generator.add_section("Wall Moments", str(wall_moments))
#         self.report_generator.add_section("Load Area", str(load_area))

#         self.report_generator.save()
#         messagebox.showinfo("Report Generated", "The report has been generated successfully.")


# import tkinter as tk
# from tkinter import simpledialog, messagebox, Label, Checkbutton, BooleanVar, Entry
# from tkinterdnd2 import TkinterDnD, DND_FILES
# import os

# class Application(tk.Frame):
#     def __init__(self, master, ifc_processor, load_calculator, plotter, report_generator):
#         super().__init__(master)
#         self.master = master
#         self.ifc_processor = ifc_processor
#         self.load_calculator = load_calculator
#         self.plotter = plotter
#         self.report_generator = report_generator
#         self.init_gui()
    
#     def init_gui(self):
#         self.master.title('IFC Processing Tool')
#         self.master.geometry('500x300')
#         self.create_widgets()

#     def create_widgets(self):
#         self.label = Label(self.master, text="Drag and drop an IFC file here.")
#         self.label.pack(padx=10, pady=10)

#         self.button_frame = tk.Frame(self.master)
#         self.button_frame.pack(padx=10, pady=10)

#         self.process_button = tk.Button(self.button_frame, text="Process IFC", command=self.process_ifc)
#         self.process_button.pack(side="left", padx=5, pady=5)

#         self.generate_report_button = tk.Button(self.button_frame, text="Generate Report", command=self.generate_report)
#         self.generate_report_button.pack(side="left", padx=5, pady=5)

#         self.file_label = Label(self.master, text="", wraplength=400)
#         self.file_label.pack(padx=10, pady=10)

#         self.master.drop_target_register(DND_FILES)
#         self.master.dnd_bind('<<Drop>>', self.on_drop)

#     def on_drop(self, event):
#         file_path = event.data
#         if os.path.isfile(file_path):
#             self.file_label.config(text=f"File selected: {file_path}")
#             self.ifc_processor.ifc_path = file_path
#         else:
#             messagebox.showerror("Invalid File", "The dropped file path is not valid. Please drop a valid IFC file.")
#             self.file_label.config(text="")

#     def process_ifc(self):
#         if not self.ifc_processor.ifc_path:
#             messagebox.showerror("No File", "No IFC file selected. Please drop a valid IFC file.")
#             return
        
#         try:
#             element_counts = self.ifc_processor.extract_element_counts()
#             total_weight = self.ifc_processor.extract_ifc_data()
#             section_types = self.ifc_processor.extract_section_types()
#             total_stud_count, aux_data = self.ifc_processor.extract_aux_data()
#             total_floors = self.ifc_processor.extract_floor_data()
#             forces, moments = self.ifc_processor.extract_forces_moments()
#             coordinates = self.ifc_processor.parse_ifc_file()

#             # Perform load calculations
#             total_beam_weight, total_column_weight = self.load_calculator.calculate_beam_column_weight(self.ifc_processor)
#             area_xy, area_yz, area_xz = self.load_calculator.calculate_area_from_coords(coordinates)
#             footing_perimeter = self.load_calculator.calculate_footing_perimeter(coordinates)
#             roof_perimeter = self.load_calculator.calculate_roof_perimeter(coordinates)
#             wall_moments = self.load_calculator.calculate_wall_moments(100.0, 10.0)
#             load_area = self.load_calculator.calculate_load_area(coordinates, 50.0, 20.0)

#             self.plotter.plot_aux_data(aux_data)
#             self.plotter.plot_load_distribution(list(forces.keys()), list(forces.values()), list(moments.values()))

#         except Exception as e:
#             messagebox.showerror("Processing Error", f"An error occurred during IFC processing: {str(e)}")

#     def generate_report(self):
#         if not self.ifc_processor.ifc_path:
#             messagebox.showerror("No File", "No IFC file selected. Please drop a valid IFC file.")
#             return

#         try:
#             element_counts = self.ifc_processor.extract_element_counts()
#             total_weight = self.ifc_processor.extract_ifc_data()
#             section_types = self.ifc_processor.extract_section_types()
#             total_stud_count, aux_data = self.ifc_processor.extract_aux_data()
#             total_floors = self.ifc_processor.extract_floor_data()
#             forces, moments = self.ifc_processor.extract_forces_moments()
#             coordinates = self.ifc_processor.parse_ifc_file()

#             # Perform load calculations
#             total_beam_weight, total_column_weight = self.load_calculator.calculate_beam_column_weight(self.ifc_processor)
#             area_xy, area_yz, area_xz = self.load_calculator.calculate_area_from_coords(coordinates)
#             footing_perimeter = self.load_calculator.calculate_footing_perimeter(coordinates)
#             roof_perimeter = self.load_calculator.calculate_roof_perimeter(coordinates)
#             wall_moments = self.load_calculator.calculate_wall_moments(100.0, 10.0)
#             load_area = self.load_calculator.calculate_load_area(coordinates, 50.0, 20.0)

#             self.report_generator.add_title("IFC Report")
#             self.report_generator.add_section("Element Counts", str(element_counts))
#             self.report_generator.add_section("Total Weight", str(total_weight))
#             self.report_generator.add_section("Section Types", str(section_types))
#             self.report_generator.add_section("Auxiliary Data", str(aux_data))
#             self.report_generator.add_section("Total Stud Count", str(total_stud_count))
#             self.report_generator.add_section("Total Floors", str(total_floors))
#             self.report_generator.add_section("Forces", str(forces))
#             self.report_generator.add_section("Moments", str(moments))
#             self.report_generator.add_section("Coordinates", str(coordinates))
#             self.report_generator.add_section("Total Beam Weight", str(total_beam_weight))
#             self.report_generator.add_section("Total Column Weight", str(total_column_weight))
#             self.report_generator.add_section("Area (XY, YZ, XZ)", f"{area_xy}, {area_yz}, {area_xz}")
#             self.report_generator.add_section("Footing Perimeter", str(footing_perimeter))
#             self.report_generator.add_section("Roof Perimeter", str(roof_perimeter))
#             self.report_generator.add_section("Wall Moments", str(wall_moments))
#             self.report_generator.add_section("Load Area", str(load_area))

#             self.report_generator.save()
#             messagebox.showinfo("Report Generated", "The report has been generated successfully.")

#         except Exception as e:
#             messagebox.showerror("Report Generation Error", f"An error occurred during report generation: {str(e)}")



import tkinter as tk
from tkinter import simpledialog, messagebox, Label, Checkbutton, BooleanVar, Entry
from tkinterdnd2 import TkinterDnD, DND_FILES
import os
from imports import *

class Application(tk.Frame):
    def __init__(self, master, ifc_processor, load_calculator, plotter, report_generator):
        super().__init__(master)
        self.master = master
        self.ifc_processor = ifc_processor
        self.load_calculator = load_calculator
        self.plotter = plotter
        self.report_generator = report_generator
        self.init_gui()
    
    def init_gui(self):
        self.master.title('IFC Processing Tool')
        self.master.geometry('500x300')
        self.create_widgets()

    def create_widgets(self):
        self.label = Label(self.master, text="Drag and drop an IFC file here.")
        self.label.pack(padx=10, pady=10)

        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(padx=10, pady=10)

        self.process_button = tk.Button(self.button_frame, text="Process IFC", command=self.process_ifc)
        self.process_button.pack(side="left", padx=5, pady=5)

        self.generate_report_button = tk.Button(self.button_frame, text="Generate Report", command=self.generate_report)
        self.generate_report_button.pack(side="left", padx=5, pady=5)

        self.file_label = Label(self.master, text="", wraplength=400)
        self.file_label.pack(padx=10, pady=10)

        self.master.drop_target_register(DND_FILES)
        self.master.dnd_bind('<<Drop>>', self.on_drop)

    def on_drop(self, event):
        file_path = event.data
        if os.path.isfile(file_path):
            self.file_label.config(text=f"File selected: {file_path}")
            self.ifc_processor.ifc_path = file_path
            try:
                self.ifc_processor.ifc_file = ifcopenshell.open(file_path)
            except Exception as e:
                messagebox.showerror("Invalid File", f"Failed to open IFC file: {str(e)}")
                self.file_label.config(text="")
        else:
            messagebox.showerror("Invalid File", "The dropped file path is not valid. Please drop a valid IFC file.")
            self.file_label.config(text="")

    def process_ifc(self):
        if not self.ifc_processor.ifc_file:
            messagebox.showerror("No File", "No IFC file selected. Please drop a valid IFC file.")
            return
        
        try:
            element_counts = self.ifc_processor.extract_element_counts()
            total_weight = self.ifc_processor.extract_ifc_data()
            section_types = self.ifc_processor.extract_section_types()
            total_stud_count, aux_data = self.ifc_processor.extract_aux_data()
            total_floors = self.ifc_processor.extract_floor_data()
            forces, moments = self.ifc_processor.extract_forces_moments()
            coordinates = self.ifc_processor.parse_ifc_file()

            # Perform load calculations
            total_beam_weight, total_column_weight = self.load_calculator.calculate_beam_column_weight(self.ifc_processor)
            area_xy, area_yz, area_xz = self.load_calculator.calculate_area_from_coords(coordinates)
            footing_perimeter = self.load_calculator.calculate_footing_perimeter(coordinates)
            roof_perimeter = self.load_calculator.calculate_roof_perimeter(coordinates)
            wall_moments = self.load_calculator.calculate_wall_moments(100.0, 10.0)
            load_area = self.load_calculator.calculate_load_area(coordinates, 50.0, 20.0)

            self.plotter.plot_aux_data(aux_data)
            self.plotter.plot_load_distribution(list(forces.keys()), list(forces.values()), list(moments.values()))

        except Exception as e:
            messagebox.showerror("Processing Error", f"An error occurred during IFC processing: {str(e)}")

    def generate_report(self):
        if not self.ifc_processor.ifc_file:
            messagebox.showerror("No File", "No IFC file selected. Please drop a valid IFC file.")
            return

        try:
            element_counts = self.ifc_processor.extract_element_counts()
            total_weight = self.ifc_processor.extract_ifc_data()
            section_types = self.ifc_processor.extract_section_types()
            total_stud_count, aux_data = self.ifc_processor.extract_aux_data()
            total_floors = self.ifc_processor.extract_floor_data()
            forces, moments = self.ifc_processor.extract_forces_moments()
            coordinates = self.ifc_processor.parse_ifc_file()

            # Perform load calculations
            total_beam_weight, total_column_weight = self.load_calculator.calculate_beam_column_weight(self.ifc_processor)
            area_xy, area_yz, area_xz = self.load_calculator.calculate_area_from_coords(coordinates)
            footing_perimeter = self.load_calculator.calculate_footing_perimeter(coordinates)
            roof_perimeter = self.load_calculator.calculate_roof_perimeter(coordinates)
            wall_moments = self.load_calculator.calculate_wall_moments(100.0, 10.0)
            load_area = self.load_calculator.calculate_load_area(coordinates, 50.0, 20.0)

            self.report_generator.add_title("IFC Report")
            self.report_generator.add_section("Element Counts", str(element_counts))
            self.report_generator.add_section("Total Weight", str(total_weight))
            self.report_generator.add_section("Section Types", str(section_types))
            self.report_generator.add_section("Auxiliary Data", str(aux_data))
            self.report_generator.add_section("Total Stud Count", str(total_stud_count))
            self.report_generator.add_section("Total Floors", str(total_floors))
            self.report_generator.add_section("Forces", str(forces))
            self.report_generator.add_section("Moments", str(moments))
            self.report_generator.add_section("Coordinates", str(coordinates))
            self.report_generator.add_section("Total Beam Weight", str(total_beam_weight))
            self.report_generator.add_section("Total Column Weight", str(total_column_weight))
            self.report_generator.add_section("Area (XY, YZ, XZ)", f"{area_xy}, {area_yz}, {area_xz}")
            self.report_generator.add_section("Footing Perimeter", str(footing_perimeter))
            self.report_generator.add_section("Roof Perimeter", str(roof_perimeter))
            self.report_generator.add_section("Wall Moments", str(wall_moments))
            self.report_generator.add_section("Load Area", str(load_area))

            self.report_generator.save()
            messagebox.showinfo("Report Generated", "The report has been generated successfully.")

        except Exception as e:
            messagebox.showerror("Report Generation Error", f"An error occurred during report generation: {str(e)}")
