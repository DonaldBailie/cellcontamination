import pandas as pd
import matplotlib.pyplot as plt
import numpy
from matplotlib.pyplot import figure


class PlotContam:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.contam_df = pd.read_excel(self.file_name, sheet_name=self.sheet_name, header=self.header_line)

    def exclude(self, contam_s, cell_line):
        i = 0
        other_value = 0
        other_len = 0
        while i != len(contam_s.index):
            if contam_s.index[i] != cell_line:
                other_value = contam_s[i] + other_value
                contam_s = contam_s.drop(contam_s.index[i])
                i = i - 1
                other_len = other_len + 1
            i = i + 1
        contam_s = contam_s.set_value('Other {0} Contaminators'.format(other_len), other_value)
        return contam_s

    def length_check(self, contam_s, length):
        for i in numpy.arange(0, len(contam_s.index)):
            if len(contam_s.index[i]) > length:
                contam_s = contam_s.rename(index={contam_s.index[i]: contam_s.index[i][0:length]+'...'})
        return contam_s

    def contam_format(self, label, cell_line=None):
        contam_s = self.contam_df[label].value_counts()
        if cell_line is not None:
            contam_s = self.exclude(contam_s, cell_line)
        else:
            contam_s = self.length_check(contam_s, self.label_length)
        return contam_s

    def plot(self, plot_type, contam_s, title, xlabel=None, ylabel=None, high_end=None, cell_line=None):
        figure(figsize=(20, 10))
        if plot_type == 'pie':
            if high_end != 'all' or cell_line is None:
                contam_s[0:high_end].plot.pie(autopct='%1.1f%%', startangle=90)
            else:
                contam_s[:].plot.pie(autopct='%1.1f%%', startangle=90)
        elif plot_type == 'bar':
            if high_end != 'all' or cell_line is None:
                contam_s[0:high_end].plot.barh(color='royalblue')
            else:
                contam_s[:].plot.barh(color='royalblue')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.savefig('{0}.png'.format(title), figsize=(20, 10))
        plt.show()

    def pie(self, label, title, xlabel=None, ylabel=None, high_end=None, cell_line=None):
        contam_s = self.contam_format(label, cell_line)
        self.plot('pie', contam_s, title, xlabel, ylabel, high_end, cell_line)

    def bar(self, label, title, xlabel=None, ylabel=None, high_end=None, cell_line=None):
        contam_s = self.contam_format(label, cell_line)
        self.plot('bar', contam_s, title, xlabel, ylabel, high_end, cell_line)


cellcontam = PlotContam(file_name='crosscont.xlsx', sheet_name='Version 9 Table 1', header_line=27, label_length=20)
cellcontam.bar('Contaminating Cell Line',
               'Top 20 Contaminators',
               'Number Of Cell Lines Contaminated',
               'Cell Line',
               high_end=20)
cellcontam.pie('Contaminating Cell Line',
               'Percentage of Contaminations Caused By HeLa',
               cell_line='HeLa')
cellcontam.bar('Contaminating Cell Line',
               'Number of Contaminations Caused By HeLa',
               'Number of Cell Lines Contaminated',
               'Cell Line',
               cell_line='HeLa')
cellcontam.bar('Claimed Cell Type',
               'Top 20 Claimed Cell Types',
               'Number Of Times Claimed',
               'Claimed Cell Type',
               high_end=20)
cellcontam.bar('Actual Cell Type',
               'Top 20 Actual cell types',
               'Number Of Times Found',
               'Actual Cell Type',
               high_end=20)
