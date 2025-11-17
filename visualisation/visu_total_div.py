import matplotlib.pyplot as plt
import numpy as np
def plot_total_diversity(content_rand,content_list,name='diversity_comparaison'):    
    max_ = np.max(content_rand['tabular_view'],axis=0)
    N = len(content_rand['tabular_view'])
    diff = lambda tab,j: np.sum(np.abs(tab[j+1:,:]-tab[j,:])**2,axis=1)
    distances = [[] for j in range(N)]
    diversities_rand = np.zeros((N//1000)+1)
    for j in range(N):
        distances[j] = diff(content_rand['tabular_view'],j)
    for j,n in enumerate(range(0,N+1,1000)):
        diversities_rand[j] = np.sum([np.sum(o[:n-i]) for i,o in  enumerate(distances[:n])])
    
    diversities = np.zeros((len(content_list),1+N//1000))
    start = 0
    for f,vec in enumerate(content_list):
        content_imgep,label = vec[0],vec[1]
        distances = [[] for j in range(len(content_imgep['tabular_view']))]
        for j in range(len(content_imgep['tabular_view'])):
            distances[j] = diff(content_imgep['tabular_view'],j)
        for j,n in enumerate(range(0,N+1,1000)):
            diversities[f,j] = np.sum([np.sum(o[:n-i]) for i,o in  enumerate(distances[:n])])

        plt.plot(np.arange(0,N+1,1000)[start:],diversities[f][start:],'-o',label=label+f'value = {round(diversities[f][-1]/1e11,1)}1e11')
    plt.plot(np.arange(0,N+1,1000)[start:],diversities_rand[start:],'-o',label=f'random value = {round(diversities_rand[-1]/1e11,1)}1e11',alpha=.3)
    plt.grid()
    plt.title('Entire space Diversity IMGEP vs RANDOM')
    plt.ylabel('sum of squares of distances between all pairs')
    plt.xlabel('iterations')
    plt.xticks(range(0,10001,1000)[start:])
    plt.legend()
    plt.savefig(name)
    plt.show()
