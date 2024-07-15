from fpdf import FPDF
from imports import *

class ReportGenerator:
    def __init__(self, report_path):
        self.pdf = FPDF()
        self.report_path = report_path

    def add_title(self, title):
        self.pdf.add_page()
        self.pdf.set_font("Arial", "B", 16)
        self.pdf.cell(0, 10, title, 0, 1, "C")

    def add_section(self, title, content):
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.cell(0, 10, title, 0, 1, "L")
        self.pdf.set_font("Arial", "", 10)
        self.pdf.multi_cell(0, 10, content)

    def add_plot(self, plot_func, *args, **kwargs):
        plt.figure()
        plot_func(*args, **kwargs)
        plt.savefig("plot.png")
        self.pdf.image("plot.png", x=10, y=None, w=190)
        os.remove("plot.png")

    def save(self):
        self.pdf.output(self.report_path)
