import numpy as np

def fit2D_2ref(ref1,ref2,data,res):
    total = 100/res + 1
    factor = (np.linspace(0,100,res)).transpose()
    self.fRGB = float(np.array[factor,100-factor])/100
    self.fRGB = np.append(self.fRGB,np.zeros(total,dtype=np.float32),axis=1)
    sum_sqdata = np.sum(np.square(data),axis=0)
    [a,b,c] = data.size()
    R_ref = np.empty((a,b,total),dtype=np.float32)

    for i in range(self.n_rows):
        for j in range(self.n_cols):
	    for k in range(total):
                image_ref_com = self.fRGB[j,0]*ref1 + self.fRGB[j,1]*ref2
		sqr = np.square(data[i,j,:]-image_ref_com)
		R_ref[i,j,k] = np.sum(sqr,axis=0)/sum_sqdata[i,j]
            self.min_R[i,j] = np.amin(R_ref[i,j,:])
            self.index[i,j] = np.unravel_index((R_ref[i,j,:]).argmin(),k)
    


def fit2D_3ref(ref1,ref2,ref3,data,res):
    return

