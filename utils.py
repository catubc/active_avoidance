import numpy as np
import matplotlib.pyplot as plt
import h5py


class AA():
    
    #
    def __init__(self, fname):

        self.fname = fname


    #
    def load_csv(self):

        with h5py.File(self.fname, "r") as f:
            self.dset_names = list(f.keys())
            self.locations = f["tracks"][:].T
            self.node_names = [n.decode() for n in f["node_names"][:]]


        # print("===HDF5 datasets===")
        # print(self.dset_names)
        # print()

        # print("===locations data shape===")
        # print(self.locations.shape)
        # print()

        # print("===nodes===")
        # for i, name in enumerate(self.node_names):
        #     print(f"{i}: {name}")
    
    #
    def plot_track(self):

        #
        self.locations.shape

        #
        plt.figure(figsize=(12,10))
        for k in [1]:
            loc = self.locations[:,k,:,0]
            
            # bp has dimensions: (90000,2)
            plt.plot(loc[:,0],
                    1200-loc[:,1],
                    )
                    
        x = np.linspace(0, 1200, 100)
        y1 = 0.5773502691896384 * x + 310.9599293337763
        y2 = 1948.7191084394267 * x + -1236078.708004072  # as close to x = 634 as possible 
        y3 = -0.5766662617226573 * x + 1043.3574098868085

        plt.plot(x, y1, 'black') 
        plt.plot(x, y2, 'black') 
        plt.plot(x, y3, 'black') 

        plt.gray()        
        plt.xlim(250, 1050) # 1280 /4 * 2.5 = 800
        plt.ylim(350, 990) #1024 /4 * 2.5 = 640

        plt.show()

    #
    def compute_sector_occupancy(self):
        sector1 = 0 
        sector2 = 0 
        sector3 = 0 
        sector4 = 0 
        sector5 = 0 
        sector6 = 0

        for i in range (0, self.locations.shape[0]):
            x_m = self.locations[i, 1, 0, 0]
            y_m = 1200-self.locations[i, 1, 1, 0]

            y1 = 0.5773502691896384 * x_m + 310.9599293337763
            y2 = 1948.7191084394267 * x_m + -1236078.708004072  # as close to x = 634 as possible 
            y3 = -0.5766662617226573 * x_m + 1043.3574098868085


            if x_m >= 634:
                if y1 <= y_m:
                    sector3 += 1
                elif y3 <= y_m:
                    sector4 += 1 
                else:
                    sector5 += 1
            
            elif x_m < 634:
                if y1 >= y_m:
                    sector6 += 1
                elif y3 >= y_m:
                    sector1 += 1
                else:
                    sector2 += 1
                    
            #print (sector1, sector2, sector3, sector4, sector5, sector6)
            #print (x_m, y_m)
            
        # print("Sector 1 = ", sector1)
        # print("Sector 2 =", sector2)
        # print("Sector 3 =", sector3)
        # print("Sector 4 =", sector4)
        # print("Sector 5 =", sector5)
        # print("Sector 6 =", sector6)

        # Labels for the bars
        labels = ['1', '2', '3', ' 4', ' 5', ' 6']

        # Values for the bars
        data = [sector1, sector2, sector3, sector4, sector5, sector6]

        if self.plotting:
            plt.figure()
            # Create a bar chart
            plt.bar(labels, data)

            # Add labels and title
            plt.xlabel('Sectors')
            plt.ylabel('Detection Count')
            plt.suptitle("Mouse Detection per Sector (Entire Video)")
            plt.title("d1, Trial 1")


            plt.savefig('mouse1_d1_bar_chart.png')
            plt.show()

        return data
