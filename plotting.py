import matplotlib.pyplot as plt
import seaborn as sns

class Plotter:
    @staticmethod
    def plot_aux_data(aux_data):
        sections, counts, weights = zip(*[(k, v['count'], v['total_weight']) for k, v in aux_data.items()])

        fig, ax1 = plt.subplots()
        sns.set(style="whitegrid")
        bar_width = 0.35
        bar1 = ax1.bar(sections, counts, bar_width, label='Number of Studs', color='b')
        ax1.set_xlabel('Section Type')
        ax1.set_ylabel('Number of Studs')
        ax1.set_title('Number of Studs and Total Weight by Section Type')
        ax2 = ax1.twinx()
        bar2 = ax2.bar(sections, weights, bar_width, label='Total Weight (kN)', color='r', alpha=0.6)
        ax2.set_ylabel('Total Weight (kN)')
        ax1.set_xticklabels(sections, rotation=45, ha='right')
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')
        plt.show()

    @staticmethod
    def plot_load_distribution(floor_names, floor_loads, floor_moments):
        fig, ax1 = plt.subplots()
        sns.set(style="whitegrid")
        bar_width = 0.35
        bar1 = ax1.bar(floor_names, floor_loads, bar_width, label='Loads (kN)', color='b')
        ax1.set_xlabel('Floors')
        ax1.set_ylabel('Loads (kN)')
        ax1.set_title('Load and Moment Distribution')
        ax2 = ax1.twinx()
        bar2 = ax2.bar(floor_names, floor_moments, bar_width, label='Moments (kNm)', color='r', alpha=0.6)
        ax2.set_ylabel('Moments (kNm)')
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')
        ax1.set_xticklabels(floor_names, rotation=45, ha='right')
        plt.show()
