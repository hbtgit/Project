# import tkinter as tk
# from tkinterdnd2 import TkinterDnD

# from ifc_processing import IFCProcessor
# from load_calculations import LoadCalculator
# from plotting import Plotter
# from reporting import ReportGenerator
# from gui_components import Application

# def main():
#     root = TkinterDnD.Tk()
#     ifc_processor = IFCProcessor("")
#     load_calculator = LoadCalculator()
#     plotter = Plotter()
#     report_generator = ReportGenerator("path_to_report.pdf")
#     app = Application(master=root, ifc_processor=ifc_processor, load_calculator=load_calculator, plotter=plotter, report_generator=report_generator)
#     app.mainloop()

# if __name__ == "__main__":
#     main()
    
    
    
    
# from imports import * 
# import tkinter as tk
# from tkinter import filedialog
# from ifc_processing import process_ifc

# class MainGUI(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title("IFC Processing")
#         self.geometry("800x600")

#         # Set up the drag and drop functionality
#         self.drop_target_register(tk.DND_FILES)
#         self.dnd_bind('<<Drop>>', self.on_drop)

#     def on_drop(self, event):
#         file_paths = event.data.split()
#         for file_path in file_paths:
#             process_ifc(file_path)

# if __name__ == "__main__":
#     app = MainGUI()
#     app.mainloop()

import tkinter as tk
from tkinterdnd2 import TkinterDnD

from ifc_processing import IFCProcessor
from load_calculations import LoadCalculator
from plotting import Plotter
from reporting import ReportGenerator
from gui_components import Application

def main():
    root = TkinterDnD.Tk()
    ifc_processor = IFCProcessor(None)  # Initialize with None or a valid default path
    load_calculator = LoadCalculator()
    plotter = Plotter()
    report_generator = ReportGenerator("path_to_report.pdf")
    app = Application(master=root, ifc_processor=ifc_processor, load_calculator=load_calculator, plotter=plotter, report_generator=report_generator)
    app.mainloop()

if __name__ == "__main__":
    main()
