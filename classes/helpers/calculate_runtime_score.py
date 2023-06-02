import numpy as np
from pathlib import Path

class ScoreCalculator:
    def __init__(self) -> None:
        with open(Path('./Sequences/Runtime_Scores.csv'), 'r', encoding='utf-8') as input:
            data=np.genfromtxt(input, delimiter=';',dtype='unicode')
        self.data = data

    def calculate(self):
        #headers=data[0,:]
        time_data = self.data[1:,1:]
        time_data = time_data.astype(dtype=float)
        tracker_names =self.data[:,0]

        sum_of_each_seq =time_data.sum(axis=0)
        n_track,n_seq = time_data.shape

        score_list = []
        for j in range(0,n_track):
            holder = []
            for i in range(0,n_seq):
                holder.append(1-(time_data[j,i]/sum_of_each_seq[i]))
            score_list.append((100/n_seq)*(np.asarray(holder,dtype=float).sum(axis=0)))
        print('Laufzeitscores:')
        for i in range(0,n_track):
            print(f'{tracker_names[i]}: {score_list[i]:.3f} %')


if __name__ == '__main__':
    obj = ScoreCalculator(Path(r'C:\Users\Sandro\Desktop\Mappe1.csv'))
    obj.calculate()