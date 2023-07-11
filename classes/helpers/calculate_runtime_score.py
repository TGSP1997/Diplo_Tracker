"""
Helper to calculate and create Diagramms from a Runtime_Scores.csv
Diagramm 1 for the Score for all Sequences
DIagramm 2 for a mean time value of each tracker
"""


from typing import Dict
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


class ScoreCalculator:
    """
    Class to automaticly create 2 DIagramms out of the Runtime_Scores.csv
    """
    def __init__(self) -> None:
        self.csv_path  = Path('./Sequences/Runtime_Scores.csv')
        with open(self.csv_path, 'r', encoding = 'utf-8') as input_file:
            data = np.genfromtxt(input_file, delimiter = ';', dtype = 'unicode')
        self.data  = data

    def calculate(self) -> None:
        """
        Calculates Score and mean runtime
        """
        # multidim array without
        # strings(first row and collumn) but values are string
        time_data = self.data[1:, 1:]
        time_data = time_data.astype(dtype = float)
        tracker_names = self.data[1:, 0] #get first column
        sum_of_each_seq = time_data.sum(axis = 0)
        n_track,n_seq = time_data.shape #number of trackers and sequences available
        score_list  = []
        score_dict_1  = {} #Score
        score_dict_2  = {} #mean runtime
        for j in range(0, n_track):
            holder  = []
            for i in range(0, n_seq):
                holder.append(1-(time_data[j, i]/sum_of_each_seq[i]))
            score_list.append((100/n_seq)*(np.asarray(holder, dtype = float).sum(axis = 0)))
        print('Laufzeitscores:')
        for i in range(0, n_track):
            print(f'{tracker_names[i]}: {score_list[i]:.3f} %')
            score_dict_1.update({tracker_names[i]: score_list[i]})
        self._draw_diagramm(score_dict_1, option = 1)

        for k in range(0, n_track):
            score_dict_2.update({tracker_names[k]: time_data[k].mean()})
        self._draw_diagramm(score_dict_2, option = 2)

    def _draw_diagramm(self, score_dict: Dict[str, float], option: int) -> None:
        """
        Create a diagramm of given dict with two options
        Args:
            score_dict (Dict[str,float]): Contains tracker names and corresponding value
            option (int): 1 for overall Score; 2 for mean runtime score
        """
        x_axis = []
        y_axis = []
        for key, value in score_dict.items():
            x_axis.append(key.encode().decode('unicode_escape'))
            y_axis.append(value)
        sorted_values = sorted(y_axis, reverse = True)
        _, ax_sub = plt.subplots()
        y_pos = np.arange(len(x_axis))
        plt.xticks(y_pos, x_axis)
        if option == 1:
            colormat = np.where( #asarray solely for type checking
                np.asarray(y_axis) > sorted_values[1],
                'orange',
                'darkgray'
            )
            ax_sub.set_ylim(top =110) # type: ignore[call-arg]
            plt.ylabel('Score')

        if option ==2:
            colormat =np.where(
                np.asarray(y_axis)<sorted_values[-2],
                'orange',
                'darkgray'
            )
            plt.ylabel('Mittelwert in s')
            ax_sub.set_ylim(top =sorted_values[0]+2) # type: ignore[call-arg]

        bar_y  = plt.bar( # type: ignore[attr-defined]
            y_pos,
            y_axis,
            align = 'center',
            color = colormat,
            width = 0.5
        )
        plt.bar_label(bar_y, fmt = '%.2f') # type: ignore[attr-defined]
        plt.title('Runtime Comparison')
        plt.tick_params(axis = 'x', which = 'both', bottom = False) # type: ignore[attr-defined]
        if option == 1:
            plt.savefig(
                fname = self.csv_path.parent.joinpath('Runtime_Comparison_1.pdf').as_posix(),
                bbox_inches = 'tight'
            )
            plt.savefig(
                fname = self.csv_path.parent.joinpath('Runtime_Comparison_1.png').as_posix(),
                bbox_inches = 'tight'
            )
        if option ==2:
            plt.savefig(
                fname = self.csv_path.parent.joinpath('Runtime_Comparison_2.pdf').as_posix(),
                bbox_inches = 'tight'
            )
            plt.savefig(
                fname = self.csv_path.parent.joinpath('Runtime_Comparison_2.png').as_posix(),
                bbox_inches = 'tight'
            )


if __name__  == '__main__':
    obj  = ScoreCalculator()
    obj.calculate()
