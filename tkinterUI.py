import tkinter as tk
from matplotlib import pyplot as plt
import projmotion as proj
from math import inf


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.targets = []
        self.smallest = inf
        self.optTgt = None

        container = tk.Frame(self, bg = "white")
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        for F in (Menu, Targets, Results):
            pageName = F.__name__
            frame = F(container, self, bg = "light blue", padx = 5, pady = 5)
            self.frames[pageName] = frame

        self.oldFrame = self.frames["Menu"]
        self.showFrame("Menu")

    def showFrame(self, pageName):
        self.oldFrame.grid_forget()
        self.frames[pageName].grid(row = 0, column = 0)
        self.oldFrame = self.frames[pageName]


class Menu(tk.Frame):

    def __init__(self, parent, controller, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.controller = controller

        title = tk.Label(self, text = "Projectile Motion Simulator")
        velL = tk.Label(self, text = "Projectile speed:")
        velE = tk.Entry(self)
        tgtCountL = tk.Label(self, text = "Amount of targets:")
        tgtCountE = tk.Entry(self)
        done = tk.Button(self, text = "Done", command = lambda: self.nextPage(velE.get(), tgtCountE.get()))

        title.grid(columnspan = 2, pady = 5)
        velL.grid(row = 1, column = 0, pady = 5)
        velE.grid(row = 1, column = 1, pady = 5)
        tgtCountL.grid(row = 2, column = 0, pady = 5)
        tgtCountE.grid(row = 2, column = 1, pady = 5)
        done.grid(columnspan = 2, pady = 5)

    def nextPage(self, vel, tgtCount):
        self.controller.vel = int(vel)
        self.controller.tgtCount = int(tgtCount)
        self.controller.showFrame("Targets")


class Targets(tk.Frame):

    def __init__(self, parent, controller, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.controller = controller
        self.count = 1

        self.title = tk.Label(self, text = "Target " + str(self.count))
        hDistL = tk.Label(self, text = "Horizontal displacement:")
        self.hDistE = tk.Entry(self)
        vDistL = tk.Label(self, text = "Vertical displacement:")
        self.vDistE = tk.Entry(self)
        done = tk.Button(self, text = "Next",
                         command = lambda: self.next(int(self.hDistE.get()), int(self.vDistE.get())))

        self.title.grid(columnspan = 2, pady = 5)
        hDistL.grid(row = 1, column = 0, pady = 5)
        self.hDistE.grid(row = 1, column = 1, pady = 5)
        vDistL.grid(row = 2, column = 0, pady = 5)
        self.vDistE.grid(row = 2, column = 1, pady = 5)
        done.grid(columnspan = 2, pady = 5)

    def next(self, hDist, vDist):
        self.controller.targets.append([hDist, vDist])
        self.hDistE.delete(0, "end")
        self.vDistE.delete(0, "end")
        if self.count < self.controller.tgtCount:
            self.count += 1
            self.title.configure(text = "Target " + str(self.count))
        else:
            self.count = 1
            self.controller.showFrame("Results")


class Results(tk.Frame):

    def __init__(self, parent, controller, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.controller = controller

        self.showRes = tk.Button(self, text = "Click me to find out results", command = self.calc)
        self.showRes.grid()

    def calc(self):
        self.showRes.grid_forget()
        tk.Label(self, text = "Please wait as I calculate \n"
                              "Optimum angle and time\nFor each target\n(N/A means target impossible to hit)").grid(
            columnspan = 2)
        for (count, target) in enumerate(self.controller.targets):
            count += 1
            tk.Label(self, text = "TARGET {}\n({}, {}):".format(str(count), target[0], target[1]),
                     font = ("Arial Bold", 12)).grid(
                row = (count * 3) - 2, column = 0, pady = 5, columnspan = 2)
            tk.Label(self, text = "Optimum Angle\n(to the horizontal):").grid(row = (count * 3) - 1,
                                                                              column = 0, pady = 5)
            optAng = tk.Label(self, text = "Calculating...")
            tk.Label(self, text = "Time Taken:").grid(row = (count * 3), column = 0, pady = 5)
            timeTaken = tk.Label(self, text = "Calculating...")

            optAng.grid(row = (count * 3) - 1, column = 1, pady = 5)
            timeTaken.grid(row = (count * 3), column = 1, pady = 5)

            self.controller.update()

            data = proj.main(self.controller.vel, target[0], target[1])
            if data == -1:
                optAng.config(text = "N/A")
                timeTaken.config(text = "N/A")
            else:
                optAng.config(text = str(data[0]) + " degrees")
                timeTaken.config(text = str(data[1]) + " seconds")
                if data[1] < self.controller.smallest:
                    self.controller.smallest = data[1]
                    self.controller.optTgt = count
                plt.plot([0, target[0]], [0, 0], "k-")
                plt.plot(data[2], data[3], label = "Target " + str(count))

        if self.controller.optTgt is None:
            tk.Label(self, text = "No Targets will hit").grid(columnspan = 2, pady = 5)
        else:
            tk.Label(self, text = "Target " + str(self.controller.optTgt) + " is your best bet").grid(columnspan = 2,
                                                                                                      pady = 5)
            tk.Button(self, text = "Click to see a graph of your projectile/s", command = self.showGraph).grid(
                columnspan = 2, pady = 5)

    def showGraph(self):
        plt.legend()
        plt.show()


if __name__ == "__main__":
    app = App()
    app.mainloop()
