import numpy as np

def minn(x,n):
    n = np.min([n, np.size(x,0)])
    xt = x[0:n]
    xsn = np.msort(xt)
    I = np.argsort(xt)

    for i in range((n+1),np.size(x,0)+1):
        j=n

        while j > 0 and x[i-1] < xsn[j-1]:
            j = j - 1

        if j < n:

            xsn = [xsn[1:j], x[i-1], xsn[(j): (n - 1)]]
            I = [I[1:j], i-1, I[(j+1): (n - 1)]]
            xsn = np.array([e for e in xsn if e])
            I = np.array([e for e in I if e])

    return I

def nearestneighbour(X,P,r):
    NumberOfNeighbours = 1
    Radius = r


    idx = np.zeros([NumberOfNeighbours, np.size(P, 1)])

    # Loop through the set of points P, finding the neighbours
    Y = np.zeros([np.size(X,0),np.size(X,1)])
    for iPoint in range(np.size(P,1)):
        x = P[:, iPoint]
        for i in range(np.size(Y, 0)):
            Y[i,:] = X[i,:] - x[i]

        dSq = np.sum(np.abs(Y)**2, 0)
        iRad = np.squeeze((dSq < Radius**2).nonzero())
        iSorted = iRad[ minn(dSq[iRad],NumberOfNeighbours)]

        if iSorted.size == 0:
            print("No nearest neighbors in given radius")
            return
        idx[:,iPoint]=iSorted

    print(idx)
    return idx

def test():
    p = np.array([[2, 5, 3, 7, 2, 7, 3, 1],[8, 3, 7, 5, 2, 5, 4, 1]])
    x = np.array([[5, 9, 1, 6, 14, 6, 47, 2, 65, 25, 46, 1, 6, 1, 5836, 156, 36, 26, 2 ,3, 52, 6, 45 ,36],[1,654,25,51,62,5,12,96,15,2,8,4,69,54,5,56,8,1,6,1,46,4,486,48]])

    p = np.random.rand(2,120)
    x = np.random.rand(2,100)

    r = 10



    nearestneighbour(x,p,r)

    return 0


if __name__ == '__main__':
    test()
    print('Done')