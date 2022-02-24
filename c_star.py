import numpy as np
import matplotlib.pyplot as plt


def plot_x_star(y_max, dy):
    # plot the solution to
    # y = x + 0.15 x^5

    Y = np.arange(0,y_max, dy)
    x_star = np.zeros(Y.shape)
    for i, y in enumerate(Y):
        if i == 0:
            x_star[i] = compute_x_star(y, 0, dy)
        else:
            x_star[i] = compute_x_star(y, x_star[i-1], dy)

    return Y, x_star


def compute_x_star(y, x_0, dx):
    # compute the solution to
    # y = x + 0.15 x^5
    # where x_0 is a known lower bound on x_star.

    x = x_0 + dx

    while x + 0.15 * x ** 5 < y:
        x = x + dx

    return x - dx


if __name__ == '__main__':
    y_max = 200
    dy = 0.001

    # compute the counts-to-flow lookup table 
    #######################################################################
    Y, x_star = plot_x_star(y_max, dy)

    # load the counts-to-flow from disk 
    #######################################################################
    # Y, x_star = np.load('counts2flow_LUT.npy')

    error = 0
    for i in range(Y.shape[0]):
        error = error + np.abs(x_star[i] + 0.15*x_star[i]**5 - Y[i])
    print('Total estimation error: {}'.format(error))

    # plot counts to flow 
    #######################################################################
    plt.plot(Y, x_star, label = 'x_star')
    plt.xlabel('counts (y)')
    plt.ylabel('flow (x_star)')
    plt.legend()
    # plt.savefig('x_star_L.png')
    plt.close()

    # plot counts to travel time
    #######################################################################
    # plt.plot(Y, 1 + 0.15*x_star**4, label = 'counts2time')
    # plt.xlabel('counts (y)')
    # plt.ylabel('travel time')
    # plt.legend()
    # plt.savefig('counts2time.png')

    # save the counts to flow lookup table 
    #######################################################################
    np.save('counts2flow_LUT_ymax'+str(y_max)+'.npy', (Y,x_star))
    


