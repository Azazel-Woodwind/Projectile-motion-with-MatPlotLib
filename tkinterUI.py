import tkinter as tk
import projmotion as proj

class App(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        self.targets = []

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

        title.grid(columnspan = 2)
        velL.grid(row = 1, column = 0)
        velE.grid(row = 1, column = 1)
        tgtCountL.grid(row = 2, column = 0)
        tgtCountE.grid(row = 2, column = 1)
        done.grid(columnspan = 2)

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
        done = tk.Button(self, text = "Next", command = lambda: self.next(self.hDistE.get(), self.vDistE.get()))

        self.title.grid(columnspan = 2)
        hDistL.grid(row = 1, column = 0)
        self.hDistE.grid(row = 1, column = 1)
        vDistL.grid(row = 2, column = 0)
        self.vDistE.grid(row = 2, column = 1)
        done.grid(columnspan = 2)

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

        tk.Label(self, text = "The Results are in...").grid

        

if __name__ == "__main__":
    app = App()
    app.mainloop()
