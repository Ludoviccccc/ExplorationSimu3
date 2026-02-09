import sys
sys.path.append('../../')
import pickle
import os
import json
import matplotlib.pyplot as plt
import numpy as np

def bin_diversity(content):
    div = 5*np.ones(content.shape[1])
    coords = (content)//div
    c = np.unique(coords,axis=0)
    return c

def evaluate_hist_diversity(content_list):
    #hist diversity for imgep
    step = 1000
    diversity_list = []
    for f,content in enumerate(content_list):
        diversity = [0]+ [len(bin_diversity(content[:j])) for j in range(0,len(content),step) if j!=0]+ [len(bin_diversity(content))]
        diversity_list.append(diversity)
    return diversity_list
if __name__=='__main__':
    with open(sys.argv[1],"rb") as f:
        config = json.load(f)
    N = config['N']
    k_values = config['k_values']
    N_init = config['N_init']
    folder = 'results' 
    #os.system('mkdir images')
    #images = 'images'
    #excl = 'imgep raw data'

    #name = f'{folder}/rand_run_{N}'
    algo = ['imgep_run_1']+['operators_run_1']+['rand_run']
    N = 10000
    id_ = 0
    j_list = range(19)
    content_imgep_list = []
    for j in j_list:
        with open(os.path.join('results',f'{algo[id_]}_{N}_{j}.pkl'),'rb') as f:
            stats = pickle.load(f)
            content_imgep_list.append(stats['tabular_view'])
    print('len content list', len(content_imgep_list))
    print('len content', len(content_imgep_list[-1]))

    diversity_list = np.array(evaluate_hist_diversity(content_imgep_list))

    ll = np.arange(0,N+1,1000)
    print("ll",len(ll))
    for j in range(19):
        plt.plot(ll,diversity_list[j])
    plt.xlabel('iterations')
    plt.ylabel('diversity')
    plt.savefig("distinct_imgep.png")

    #diversities_imgep_mean = stats['imgep']['mean']
    #diversities_imgep_var = stats['imgep']['var']

    #diversities_rand_mean = stats['random']['mean']
    #diversities_rand_var = stats['random']['var']
    #t_crit_interval = stats['t_crit_interval']
    #m = stats['m']
    #print(diversities_imgep_mean.shape)
    #start = 0
    #for f in range(diversities_imgep_mean.shape[0]):
    #    y = diversities_imgep_mean[f][start:]
    #    x = np.arange(0,N+1,1000)[start:]
    #    ci = diversities_imgep_var[f][start:] *t_crit_interval[1]/np.sqrt(m)
    #    print('ci shape', ci.shape)
    #    plt.plot(x,y,'-o',label=[1,2,3][f])
    #    #plt.fill_between(x, (y-ci), (y+ci), color='b', alpha=.1)
    #plt.plot(np.arange(0,N+1,1000)[start:],diversities_rand_mean[start:],'-o',label=f'random')
    #plt.grid()
    #plt.title('Entire space Diversity IMGEP vs RANDOM', fontsize=19)
    #plt.ylabel('sum of squares of distances between all pairs', fontsize=12)
    #plt.xlabel('iterations', fontsize=19)
    #plt.xticks(range(0,10001,1000)[start:])
    #plt.legend(prop={'size': 19})
    #plt.show()
