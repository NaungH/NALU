import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from line_graph import line_graph
from calibration import calibration
from main_data import Aphrodite, Observed, Trmm

x = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
y = [1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007]

root = tk.Tk()  # Build GUI basic interface
root.title('Satellite Data Graphing')
root.iconbitmap('graph/710satelliteantenna_100238.ico')
root.geometry("300x150")


class CalApp(tk.Frame):  # Build GUI input
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.n1 = tk.DoubleVar()
        self.n2 = tk.DoubleVar()
        self.n3 = tk.IntVar()

        self.lat_label = tk.Label(master, text="Latitude")  # Build GUI latitude label
        self.lat_label.grid(row=1, column=0, stick=tk.W, padx=20)
        self.lon_label = tk.Label(master, text="Longitude")  # Build GUI longitude label
        self.lon_label.grid(row=2, column=0, stick=tk.W, padx=20)
        self.year_label = tk.Label(master, text="Year")  # Build GUI year label
        self.year_label.grid(row=3, column=0, stick=tk.W, padx=20)

        self.lat_box = tk.Entry(master, textvariable=self.n1)  # Build GUI latitude entry for user input
        self.lat_box.grid(row=1, column=1, pady=5)
        self.lon_box = tk.Entry(master, textvariable=self.n2)  # Build GUI longitude entry for user input
        self.lon_box.grid(row=2, column=1, pady=5)
        self.year_box = ttk.Combobox(master, textvariable=self.n3)  # Build GUI year combobox for user selection
        self.year_box.grid(row=3, column=1, padx=5, pady=5)
        self.year_box['values'] = y

        # Build GUI button to show graph
        self.confirm_button = tk.Button(master, text="save to csv", command=lambda: {self.save_to_csv()
                                                                                     }).grid(row=4, column=0,
                                                                                             padx=10, pady=10)
        self.show_graph_button = tk.Button(master, text="Show Graph", command=lambda: [self.get_all(),
                                                                                       self.check_a(),
                                                                                       self.check_t(),
                                                                                       self.show_line_graph(),
                                                                                       self.show_cal()
                                                                                       ]).grid(row=4, column=1,
                                                                                               padx=10, pady=10)

    def get_all(self):  # get all data needed from main_data.py using the input location and year
        lat = self.n1.get()
        lon = self.n2.get()
        year = self.n3.get()

        a_data = Aphrodite()
        t_data = Trmm()
        o_data = Observed()

        a_o = a_data.get_data(lat, lon)
        a_o.columns = y
        a = a_o[year]

        t_o = t_data.get_data(lat, lon)
        t_o.columns = y
        t = t_o[year]

        o_o = o_data.get_data()
        o_o.columns = y
        o = o_o[year]
        return a, t, o

    def save_to_csv(self, **options):  # save to csv function
        lat = self.n1.get()
        lon = self.n2.get()

        a_data = Aphrodite()
        t_data = Trmm()
        o_data = Observed()

        t_data.get_data(lat, lon).to_csv('TRMM.csv', index=False, header=y, sep=',')
        a_data.get_data(lat, lon).to_csv('APHRODITE.csv', index=False, header=y, sep=',')
        o_data.get_data().to_csv('Observed.csv', index=False, header=y, sep=',')
        tk.messagebox.showinfo(title=None, message='save successful!', **options)

    def check_a(self, **options):  # check if we have the observed data from input latitude
        lat = self.n1.get()

        if lat == 16.85:
            tk.messagebox.showinfo(title=None, message='We have the latitude data!', **options)
        else:
            tk.messagebox.showwarning(title=None, message='only latitude = 16.85 has observed data!'
                                                          ' (no calibration possible)', **options)

    def check_t(self, **options):  # check if we have the observed data from input longitude
        lon = self.n2.get()

        if lon == 96.18:
            tk.messagebox.showinfo(title=None, message='We have the longitude data!', **options)
        else:
            tk.messagebox.showwarning(title=None, message='only longitude = 96.12 has observed data!'
                                                          ' (no calibration possible)', **options)

    def show_line_graph(self):  # show line graph
        line_graph(x, self.get_all()[0], self.get_all()[1], self.get_all()[2], "Line Graph")

    def show_cal(self, **options):  # show calibrated graph
        lat = self.n1.get()
        lon = self.n2.get()

        if lat == 16.85 and lon == 96.18:
            calibration(self.get_all()[0], self.get_all()[1], self.get_all()[2])
        else:
            tk.messagebox.showerror(title=None, message='No observed data!', **options)
            exit()


run = CalApp(root)
root.mainloop()
