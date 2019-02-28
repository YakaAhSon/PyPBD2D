a = -1
b = 3
c = -3
def kernel(x):
    return a*x**6 + b*x**4 + c*x**2 + 1

def kernel_d(x):
    return 6*a*x**5 + 4*b*x**3 + 2*c*x

def kernel_d_by_x(x):
    return 6*a*x**4 + 4*b*x**2 + 2*c

def main():
    from matplotlib import pyplot as plt
    x = [(i-100)*0.012 for i in range(200)]
    y = [kernel(i) for i in x]
    y1 = [1-i for i in x]
    y2 = [0 for i in x]
    plt.plot(x,y)
    plt.plot(x,y1)
    plt.plot(x,y2)
    plt.show()

if __name__=="__main__":
    main()