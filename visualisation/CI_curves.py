import matplotlib.pyplot as plt
import pickle
import sys
sys.path.append('../')

def visu_div_iterations(data,title=None):
    k_values = [1,2,3]
    plt.figure()
    for algo in ['imgep', 'operators','rand']:
        for k in k_values:
            if algo=='rand':
                if k>1:
                    break
            x = data[algo][k]['iterations']
            mean_ = data[algo][k]['mean']
            inf = data[algo][k]['inf']
            sup = data[algo][k]['sup']
            if algo=='rand':
                plt.plot(x,mean_,'-o',label=f'mean value {algo}')
                plt.fill_between(x, inf, sup,  alpha=0.5)
            else:
                plt.plot(x,mean_,'-o',label=f'mean value {algo}, k={k}')
                plt.fill_between(x, inf, sup,  alpha=0.5)
            plt.legend()
    if title:
        plt.title(title+' mean diversity, 95 % asymptotic CI interval, 500 runs')
    plt.xlabel('iterations')
    plt.ylabel('diversity: nb of bins filled')
    plt.grid()
if __name__=='__main__':
    with open('ci_diversity.pkl','rb') as f:
        data = pickle.load(f)
    visu_div_iterations(data,title='entire space')
    plt.savefig('entire_space_div.pdf')
    plt.show()

    with open('ci_diversity_time.pkl','rb') as f:
        data = pickle.load(f)
    print(data['imgep'][1].keys())
    visu_div_iterations(data,title='Time subspace')
    plt.savefig('time_space_div.pdf')
    plt.show()

    with open('ci_diversity_remain.pkl','rb') as f:
        data = pickle.load(f)
    visu_div_iterations(data,title='Miss and hit subspace')
    plt.savefig('miss_hit_space_div.pdf')
    plt.show()
