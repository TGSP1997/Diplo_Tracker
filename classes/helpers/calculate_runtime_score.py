import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict

class ScoreCalculator:
    def __init__(self) -> None:
        self.csv_path = Path('./Sequences/Runtime_Scores.csv')
        with open(self.csv_path, 'r', encoding='utf-8') as input_file:
            data=np.genfromtxt(input_file, delimiter=';',dtype='unicode')
        self.data = data



    def calculate(self):
        #headers=data[0,:]
        time_data = self.data[1:,1:]
        time_data = time_data.astype(dtype=float)
        tracker_names =self.data[1:,0]
        sum_of_each_seq =time_data.sum(axis=0)
        n_track,n_seq = time_data.shape
        score_list = []
        score_dict = {}
        for j in range(0,n_track):
            holder = []
            for i in range(0,n_seq):
                holder.append(1-(time_data[j,i]/sum_of_each_seq[i]))
            score_list.append((100/n_seq)*(np.asarray(holder,dtype=float).sum(axis=0)))
        print('Laufzeitscores:')
        for i in range(0,n_track):
            print(f'{tracker_names[i]}: {score_list[i]:.3f} %')
            score_dict.update({tracker_names[i]:score_list[i]})
        self.draw_diagramm(score_dict)

    def draw_diagramm(self, score_dict: Dict[str,float]):
        x_axis = []
        y_axis=[]
        for key, value in score_dict.items():
            x_axis.append(key.encode().decode('unicode_escape'))
            y_axis.append(value)
        sorted_values = sorted(y_axis, reverse=True)

        _, ax = plt.subplots()
        y_pos = np.arange(len(x_axis))
        colormat=np.where(y_axis>sorted_values[1], 'orange','darkgray')
        bar = plt.bar(y_pos,y_axis,align='center', color=colormat, width=0.5)
        plt.bar_label(bar, fmt='%.2f')
        plt.xticks(y_pos,x_axis)
        plt.ylabel('Score in %')
        ax.set_ylim(top=110)
        plt.title('Runtime Comparison')
        plt.tick_params(axis='x', which='both', bottom=False)
        plt.savefig(fname = self.csv_path.parent.joinpath('Runtime_Comparison.pdf').as_posix(),bbox_inches='tight')
        plt.savefig(fname = self.csv_path.parent.joinpath('Runtime_Comparison.png').as_posix(),bbox_inches='tight')
        #plt.show()

if __name__ == '__main__':
    obj = ScoreCalculator()
    obj.calculate()