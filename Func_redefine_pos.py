import matplotlib.pyplot as plt

def multiclass_visulization_PCA(X, y):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1) 
    ax.set_xlabel('Principal Component 1', fontsize = 15)
    ax.set_ylabel('Principal Component 2', fontsize = 15)
    ax.set_title('2 component PCA', fontsize = 20)
    labels = [1, 2, 3, 4, 5]
    colors = ['r', 'g', 'b', 'c', 'm']  # 'bgrcmyk'
    for label, color in zip(labels,colors):
        ax.scatter(X[y == label][:, 0], X[y == label][:, 1]
                   , c = color
                   , s = 25)
    ax.legend(labels)
    ax.grid()
    plt.show()

def multiclass_visulization_LDA(X, y, names):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1) 
    ax.set_xlabel('Principal Component 1', fontsize = 15)
    ax.set_ylabel('Principal Component 2', fontsize = 15)
    ax.set_title('2 component LDA', fontsize = 20)
    labels = [1, 2, 3, 4, 5]
    colors = ['r', 'g', 'b', 'c', 'm']  # 'bgrcmyk'
    for label, color in zip(labels,colors):
        ax.scatter(X[y == label][:, 0], X[y == label][:, 1]
                   , c = color
                   , s = 10)
        
    ax.legend(labels)
    ax.grid()
    plt.show()


def multiclass_visulization_Kmeans(X, y):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1) 
    ax.set_xlabel('Dimentsion 1', fontsize = 15)
    ax.set_ylabel('Dimension 2', fontsize = 15)
    ax.set_title('K means', fontsize = 20)
    labels = range(8)
    #colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']  # 'bgrcmyk'
    colors = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8']  # 'bgrcmyk'
    for label, color in zip(labels,colors):
        ax.scatter(X[y == label][:, 0], X[y == label][:, 1]
                   , c = color
                   , s = 25)
    ax.legend(labels)
    ax.grid()
    plt.show()


