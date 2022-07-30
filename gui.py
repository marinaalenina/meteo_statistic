from tkinter import *
from datetime import *
from tkinter import ttk
from tkinter.ttk import Combobox as combobox
from tkinter import messagebox
import json
import matplotlib.pyplot as plt


class GUI():
    window = Tk()
    mainmenu = Menu(window, font=14)

    spin_sdt = 0
    spin_fdt = 0
    data = dict()
    devices = []
    parameters = []
    chosen_parameters = list()
    average = {"Без осреднения": 0, "Осреднение за час": 1, "Осреднение за каждые 3 часа": 3, "Осреднение за сутки": 24, "Max, min параметры за сутки": -1}
    colors = {"Черный": "k", "Красный": "r", "Синий": "b", "Зеленый": "g"}
    type_graph = {"Линейный": '-', "Столбчатый": '|', "Точечный": '.'}

    def __init__(self):
        self.window.title("Practic")
        self.window.geometry('1000x1000')
        self.mainmenu.add_cascade(label='Помощь', command=self.clicked)
        self.window.config(menu=self.mainmenu)

        self.btn_json = Button(self.window, text="Загрузить файл JSON", command=self.load_json, font=14)
        self.btn_json.grid(column=0, row=2, ipadx=10, ipady=6, padx=10, pady=10)

        self.btn_clear_mem = Button(self.window, text="Очистить память", command=self.clear_mem, font=14)
        self.btn_clear_mem.grid(column=1, row=2, ipadx=10, ipady=6, padx=10, pady=10)

        self.btn_add = Button(self.window, text="Добавить парамерт для отображения", command=self.insert_to_table, font=14)
        self.btn_add.grid(columnspan=3, row=5, ipadx=170, ipady=6, padx=10, pady=10)

        self.btn_graph = Button(self.window, text="Построение графиков", command=self.create_plot, font=14)
        self.btn_graph.grid(columnspan=3, row=11, ipadx=200, ipady=6, padx=10, pady=10)

        self.btn_clear_list = Button(self.window, text="Очистка списка отображения", command=self.clear_list, font=14)
        self.btn_clear_list.grid(columnspan=3, row=12, ipadx=180, ipady=6, padx=10, pady=10)

        self.lbl_device = Label(self.window, text="Файл, прибор", font=14)
        self.lbl_device.grid(column=0, row=3, ipadx=10, ipady=6, padx=10, pady=10)

        self.lbl_param = Label(self.window, text="Параметр", font=14)
        self.lbl_param.grid(column=1, row=3, ipadx=10, ipady=6, padx=10, pady=10)

        self.lbl_color = Label(self.window, text="Цвет", font=14)
        self.lbl_color.grid(column=2, row=3, ipadx=10, ipady=6, padx=10, pady=10)

        self.lbl_start = Label(self.window, text="Начало", font=14)
        self.lbl_start.grid(column=0, row=0, ipadx=10, ipady=6, padx=10, pady=10)

        self.lbl_finish = Label(self.window, text="Окончание", font=14)
        self.lbl_finish.grid(column=1, row=0, ipadx=10, ipady=6, padx=10, pady=10)

        self.lbl_graph = Label(self.window, text="Тип графика", font=14)
        self.lbl_graph.grid(column=0, row=9, ipadx=10, ipady=6, padx=10, pady=10)

        self.lbl_average = Label(self.window, text="Осреднение", font=14)
        self.lbl_average.grid(column=1, row=9, ipadx=10, ipady=6, padx=10, pady=10)

        self.lbl_ef_temp = Label(self.window, text="График ЭТ и нагрузки", font=14)
        self.lbl_ef_temp.grid(column=2, row=9, ipadx=10, ipady=6, padx=10, pady=10)

        self.box_device = combobox(self.window, state="readonly")
        self.box_device['values'] = ("Выбор_прибора")
        self.box_device.bind("<<ComboboxSelected>>", self.get_parameters)
        self.box_device.current(0)
        self.box_device.grid(column=0, row=4, ipadx=10, ipady=6, padx=10, pady=10)

        self.box_param = combobox(self.window, state="readonly")
        self.box_param['values'] = ("Выбор_параметра")
        self.box_param.current(0)
        self.box_param.grid(column=1, row=4, ipadx=10, ipady=6, padx=10, pady=10)

        self.box_color = combobox(self.window, state="readonly")
        self.box_color['values'] = ([i[0] for i in self.colors.items()])
        self.box_color.current(0)
        self.box_color.grid(column=2, row=4, ipadx=10, ipady=6, padx=10, pady=10)

        self.box_graph = combobox(self.window, state="readonly")
        self.box_graph['values'] = ([i[0] for i in self.type_graph.items()])
        self.box_graph.current(0)
        self.box_graph.grid(column=0, row=10, ipadx=10, ipady=6, padx=10, pady=10)

        self.box_average = combobox(self.window, state="readonly")
        self.box_average['values'] = ([i[0] for i in self.average.items()])
        self.box_average.current(0)
        self.box_average.grid(column=1, row=10, ipadx=30, ipady=6, padx=10, pady=10)

        self.box_ef_temp = BooleanVar()
        Checkbutton(self.window, variable=self.box_ef_temp , text='График ЭТ и нагрузки').grid(column=2, row=10, ipadx=30, ipady=6, padx=10, pady=10)

        self.table = ttk.Treeview(self.window)
        self.table.grid(column=0, columnspan=3, row=6, rowspan=3)
        self.table['columns'] = ('Прибор', 'Параметр', 'Цвет', 'График ЭТ и нагрузки', 'Тип графика', 'Осреднение')
        self.table.column("#0", width=0, stretch=NO)
        self.table.column("Прибор", anchor=CENTER, width=150)
        self.table.column("Параметр", anchor=CENTER, width=150)
        self.table.column("Цвет", anchor=CENTER, width=130)
        self.table.column("График ЭТ и нагрузки", anchor=CENTER, width=130)
        self.table.column("Тип графика", anchor=CENTER, width=130)
        self.table.column("Осреднение", anchor=CENTER, width=130)

        self.table.heading("#0", text="", anchor=CENTER)
        self.table.heading("Прибор", text="Прибор", anchor=CENTER)
        self.table.heading("Параметр", text="Параметр", anchor=CENTER)
        self.table.heading("Цвет", text="Цвет", anchor=CENTER)
        self.table.heading("График ЭТ и нагрузки", text="График ЭТ и нагрузки", anchor=CENTER)
        self.table.heading("Тип графика", text="Тип графика", anchor=CENTER)
        self.table.heading("Осреднение", text="Осреднение", anchor=CENTER)

        dt = datetime(2020, 12, 8, 0, 0, 0)
        values = []
        while dt <= datetime(2021, 1, 5, 0, 0, 0):
            values.append(dt.strftime("%Y/%m/%d %H:%M"))
            dt += timedelta(minutes=15)

        self.spin_sdt = Spinbox(values=values)
        self.spin_sdt.grid(column=0, row=1, ipadx=10, ipady=6, padx=10, pady=10)

        self.spin_fdt = Spinbox(values=values)
        self.spin_fdt.grid(column=1, row=1, ipadx=10, ipady=6, padx=10, pady=10)

        self.window.mainloop()

    def clicked(self):
        with open('help.txt', 'r', encoding='utf-8') as help_file:
            f = help_file.read()
            messagebox.showinfo("Помощь", f)
            
    def load_json(self):
        start_datetime = datetime.strptime(self.spin_sdt.get(), "%Y/%m/%d %H:%M").date()
        end_datetime = datetime.strptime(self.spin_fdt.get(), "%Y/%m/%d %H:%M").date()
        while start_datetime <= end_datetime:
            with open('json_file/test_{}.json'.format(start_datetime), 'r', encoding='utf-8') as file:
                self.data.update(json.load(file))
            start_datetime += timedelta(days=1)
        self.get_devices()

    def get_devices(self):
        self.devices = set([self.data[i]['uName'] + ' ' + self.data[i]['serial'] for i in self.data])
        self.box_device['values'] = list(self.devices)

    def get_parameters(self, other):
        device = self.box_device.get()
        self.parameters.clear()
        for i in self.data:
            if self.data[i]['uName'] + ' ' + self.data[i]['serial'] == device:
                for j in self.data[i]['data']:
                    try:
                        float(self.data[i]['data'][j])
                        self.parameters.append(j)
                    except BaseException:
                        pass
                break
        self.box_param['values'] = self.parameters

    def insert_to_table(self):
        self.table.insert("", "end", values=(self.box_device.get(), self.box_param.get(), self.box_color.get(), self.box_ef_temp.get(), self.box_graph.get(), self.box_average.get()))
        self.chosen_parameters.append((self.box_device.get(), self.box_param.get(), self.box_color.get(), self.box_graph.get(), self.box_average.get(), self.box_ef_temp.get()))

    def clear_list(self):
        self.table.delete(self.table.get_children()[-1])
        self.chosen_parameters.clear()

    def clear_mem(self):
        self.data.clear()
        self.chosen_parameters.clear()
        self.table.delete(*self.table.get_children())
        self.box_device['values'] = ("Выбор_прибора")
        self.box_device.current(0)
        self.box_param['values'] = ("Выбор_параметра")
        self.box_param.current(0)
        self.box_color.current(0)
        self.box_average.current(0)
        self.box_graph.current(0)

    def create_plot(self):
        plt.figure(figsize=(12, 7))
        for i in self.chosen_parameters:
            device, parameter, color, type_graph, average, ef_temp = i
            graph = {"axes": [], 'color': self.colors[color]}
            for key, value in self.data.items():
                if value['uName'] + ' ' + value['serial'] == device and parameter in value['data']:
                    if ef_temp:
                        graph["axes"].append((datetime.strptime(value['Date'], "%Y-%m-%d %H:%M:%S"), self.effective_temp(value['data'])))
                    else:
                        graph["axes"].append((datetime.strptime(value['Date'], "%Y-%m-%d %H:%M:%S"), float(value['data'][parameter])))
            sorted(graph["axes"], key=lambda tup: tup[0])
            average_sum_y = []
            average_x = []
            all_y = []
            min_y = []
            if self.average[average] > 0:
                curr_dt = graph["axes"][0][0]
                for x, y in graph["axes"]:
                    if x < curr_dt:
                        average_sum_y[-1] = (average_sum_y[-1] + y) / 2
                    else:
                        average_sum_y.append(y)
                        average_x.append(curr_dt)
                        curr_dt += timedelta(hours=self.average[average])
            elif self.average[average] == -1:
                curr_dt = graph["axes"][0][0] + timedelta(days=1)
                for x, y in graph["axes"]:
                    if x < curr_dt:
                        all_y.append(y)
                    else:
                        average_sum_y.append(max(all_y))
                        min_y.append(min(all_y))
                        all_y.clear()
                        average_x.append(curr_dt)
                        curr_dt += timedelta(days=1)
                self.determine_type_graph(average_x, min_y, "b", type_graph, parameter)
            else:
                average_sum_y = [i[1] for i in graph["axes"]]
                average_x = [i[0] for i in graph["axes"]]
            self.determine_type_graph(average_x, average_sum_y, graph["color"], type_graph, parameter)
            if self.box_ef_temp.get():
                plt.fill_between(average_x, average_sum_y, where=([i > 30 for i in average_sum_y]), color='r', alpha=1)
                plt.fill_between(average_x, average_sum_y, where=([30 >= i > 24 for i in average_sum_y]), color='y', alpha=1)
                plt.fill_between(average_x, average_sum_y, where=([24 >= i > 0 for i in average_sum_y]), color='g', alpha=1)
                plt.fill_between(average_x, average_sum_y, where=([0 >= i > -12 for i in average_sum_y]), color='y', alpha=1)
                plt.fill_between(average_x, average_sum_y, where=([-12 >= i > -24 for i in average_sum_y]), color='c', alpha=1)
                plt.fill_between(average_x, average_sum_y, where=([-24 >= i > -30 for i in average_sum_y]), color='b', alpha=1)
        plt.legend(bbox_to_anchor=(1, 0.6), fontsize='medium', frameon=True)
        plt.show()

    def effective_temp(self, parameters):
        temp, humi = 0, 0
        for key, value in parameters.items():
            if '_temp' in key:
                temp = float(value)
            if '_humidity' in key:
                humi = float(value)
        return temp - 0.4 * (temp - 10) * (1 - humi/100)

    def determine_type_graph(self, average_x, average_sum_y, color, type_graph, parameter):
        plt.xlabel('Date')
        plt.ylabel(parameter)
        if self.box_ef_temp.get():
            lbl = "Effective temp"
        else:
            lbl = parameter
        if self.type_graph[type_graph] == "-":
            plt.plot(average_x, average_sum_y, '.-{}'.format(color), alpha=0.7, lw=2, mew=2, mec='k', ms=0.1, label=lbl)
        elif self.type_graph[type_graph] == "|":
            plt.bar(average_x, average_sum_y, width=0.01, color=color, alpha=0.7, label=lbl, edgecolor="w", linewidth=0.1)
        else:
            plt.scatter(average_x, average_sum_y, c=color, s=5, label=lbl)
