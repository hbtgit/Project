import tkinter as tk
from tkinterdnd2 import TkinterDnD
from imports import *
from ifc_processing import IFCProcessor
from load_calculations import LoadCalculator
from plotting import Plotter
from reporting import ReportGenerator
from gui_components import Application

def main():
    root = TkinterDnD.Tk()
    ifc_processor = IFCProcessor("")
    load_calculator = LoadCalculator()
    plotter = Plotter()
    report_generator = ReportGenerator("path_to_report.pdf")
    app = Application(master=root, ifc_processor=ifc_processor, load_calculator=load_calculator, plotter=plotter, report_generator=report_generator)
    app.mainloop()

if __name__ == "__main__":
    main()
