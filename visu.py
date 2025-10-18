import numpy as np
import os
import matplotlib.pyplot as plt
def diversity(data:[np.ndarray,np.ndarray],bins:[np.ndarray, np.ndarray]):
    H,_,_ = np.histogram2d(data[0],data[1],bins)
    divers = np.sum(H>0)
    return divers
def plot_ddr_miss_ratio_diversity(content_random, content_imgep = None, name = None, title = None,label_algo = 'imgep',num_bank=4,num_row = 2,show=False):
    fig, axs = plt.subplots(num_row*num_bank,4, figsize = (28*num_row//2,20), layout='constrained')
    fontsize = 22
    fontsize_label = 32
    fontsize3 = 22
    for j in range(num_bank):
        for row in range(num_row):
            bins = np.arange(-1.0,1.0,0.05)
            axs[num_bank*row+j,0].hist(content_imgep['mutual']['miss_ratios_detailled'][:,row,j] - content_imgep['core0']['miss_ratios_detailled'][:,row,j],bins=bins,alpha = .5, label=label_algo)
            #axs[num_bank*row+j,0].set_yscale('log')
            axs[num_bank*row+j,0].hist(content_random['mutual']['miss_ratios_detailled'][:,row,j] - content_random['core0']['miss_ratios_detailled'][:,row,j],  bins=bins,alpha = .5, label='random')
        
            axs[num_bank*row+j,0].set_xlabel('miss ratio diff',fontsize=fontsize_label)
            axs[num_bank*row+j,0].set_title(f'[b{j+1},rw{row}][(S_0,S_1)]-(S_0,)]', fontsize=fontsize)
            if row==0 and j==0:
                axs[num_bank*row+j,0].legend(fontsize=fontsize)
            else:
                axs[num_bank*row+j,0].legend()
            #axs[num_bank*row+j,0].set_yscale('log')

            axs[num_bank*row+j,1].hist(content_imgep['mutual']['miss_ratios_detailled'][:,row,j] - content_imgep['core1']['miss_ratios_detailled'][:,row,j],bins=bins,alpha = .5, label=label_algo)
            axs[num_bank*row+j,1].hist(content_random['mutual']['miss_ratios_detailled'][:,row,j] - content_random['core1']['miss_ratios_detailled'][:,row,j],  bins=bins,alpha = .5, label='random')
            axs[num_bank*row+j,1].set_xlabel('miss ratio diff', fontsize = fontsize_label)
            axs[num_bank*row+j,1].set_title(f'r[b{j+1},rw{row}][(S_0,S_1)-(,S_1)]', fontsize=fontsize)
            axs[num_bank*row+j,1].legend()
            #axs[num_bank*row+j,1].set_yscale('log')

            diversity_ratio_random = diversity([content_random['mutual']['miss_ratios_detailled'][:,row,j],  content_random['core0']['miss_ratios_detailled'][:,row,j]], [bins, bins])
            diversity_ratio_imgep = diversity([content_imgep['mutual']['miss_ratios_detailled'][:,row,j],  content_imgep['core0']['miss_ratios_detailled'][:,row,j]], [bins, bins])
            axs[num_bank*row+j,2].scatter(content_imgep['core0']['miss_ratios_detailled'][:,row,j],  content_imgep['mutual']['miss_ratios_detailled'][:,row,j],label=label_algo, alpha = .5)
            axs[num_bank*row+j,2].scatter(content_random['core0']['miss_ratios_detailled'][:,row,j],  content_random['mutual']['miss_ratios_detailled'][:,row,j],  label='random', alpha = .5)
            axs[num_bank*row+j,2].set_xlabel('miss ratio alone (S_0,)',fontsize=fontsize_label)
            axs[num_bank*row+j,2].set_ylabel('(S_0,S_1)', fontsize=fontsize_label)
            axs[num_bank*row+j,2].axline(xy1=(0, 0), slope=1, color='r', lw=2)
            axs[num_bank*row+j,2].set_title(f'bank {j+1}, row {row}, imgep:{diversity_ratio_imgep}, rand:{diversity_ratio_random}', fontsize=fontsize3)
            axs[num_bank*row+j,2].legend()
            axs[num_bank*row+j,2].set_xticks(np.linspace(0,1,11))
            axs[num_bank*row+j,2].set_yticks(np.linspace(0,1,11))
            axs[num_bank*row+j,2].grid()

            diversity_ratio_random = diversity([content_random['mutual']['miss_ratios_detailled'][:,row,j],  content_random['core1']['miss_ratios_detailled'][:,row,j]], [bins, bins])
            diversity_ratio_imgep = diversity([content_imgep['mutual']['miss_ratios_detailled'][:,row,j],  content_imgep['core1']['miss_ratios_detailled'][:,row,j]], [bins, bins])
            axs[num_bank*row+j,3].scatter(content_imgep['core1']['miss_ratios_detailled'][:,row,j],  content_imgep['mutual']['miss_ratios_detailled'][:,row,j],label=label_algo, alpha = .5)
            axs[num_bank*row+j,3].scatter(content_random['core1']['miss_ratios_detailled'][:,row,j],  content_random['mutual']['miss_ratios_detailled'][:,row,j],  label='random', alpha = .5)
            axs[num_bank*row+j,3].set_xlabel('miss ratio alone (S_1,)',fontsize=fontsize_label)
            axs[num_bank*row+j,3].set_ylabel('(S_0,S_1)', fontsize=fontsize_label)
            axs[num_bank*row+j,3].axline(xy1=(0, 0), slope=1, color='r', lw=2)
            axs[num_bank*row+j,3].set_title(f'bank {j+1}, row {row}, imgep:{diversity_ratio_imgep}, rand:{diversity_ratio_random}', fontsize=fontsize3)
            axs[num_bank*row+j,3].legend()
            axs[num_bank*row+j,3].set_xticks(np.linspace(0,1,11))
            axs[num_bank*row+j,3].set_yticks(np.linspace(0,1,11))
            axs[num_bank*row+j,3].grid()

    if title:
        fig.suptitle(title,fontsize = fontsize_label)
    if name:
        k = 0
        while os.path.isfile(f'{name}_{k}.png'):
            k+=1
        plt.savefig(f'{name}_{k}.png')
    if show:
        plt.show()
    plt.close()


def plot_time_diversity(content_random, content_imgep = None, name = None, title = None,label_algo = 'imgep',num_bank=4,num_row = 2,show=False):
    fig = plt.figure(figsize = (12,12))#, layout='constrained')

    bins = np.arange(0,max(np.max(content_imgep['core0']['time_core0']),np.max(content_imgep['mutual']['time_core0'])),5)
    diversity_time_rand = diversity([content_random['core0']['time_core0'],content_random['mutual']['time_core0']], [bins, bins])
    diversity_time_imgep = diversity([content_imgep['core0']['time_core0'],content_imgep['mutual']['time_core0']], [bins, bins])

    ax1 = plt.subplot(321)
    ax1.scatter(content_imgep['core0']['time_core0'],content_imgep['mutual']['time_core0'], label='imgep', alpha = .5)
    ax1.scatter(content_random['core0']['time_core0'],content_random['mutual']['time_core0'], label='random', alpha = .5)
    ax1.axline(xy1=(0, 0), slope=1, color='r', lw=2)
    ax1.set_xlabel('time_core0_alone')
    ax1.set_ylabel('time_core0_together')
    ax1.legend()
    ax1.set_xticks(bins,minor=True)
    ax1.set_yticks(bins,minor=True)
    ax1.grid(which='minor')
    ax1.set_title(f'imgep:{diversity_time_imgep}, rand:{diversity_time_rand}')

    bins = np.arange(0,max(np.max(content_imgep['core1']['time_core1']),np.max(content_imgep['mutual']['time_core1'])),5)
    diversity_time_rand = diversity([content_random['core1']['time_core1'],content_random['mutual']['time_core1']], [bins, bins])
    diversity_time_imgep = diversity([content_imgep['core1']['time_core1'],content_imgep['mutual']['time_core1']], [bins, bins])



    ax2 = plt.subplot(322)
    ax2.scatter(content_imgep['core1']['time_core1'],content_imgep['mutual']['time_core1'], alpha = .5, label='imgep')
    ax2.scatter(content_random['core1']['time_core1'],content_random['mutual']['time_core1'], alpha = .5, label='random')
    ax2.axline(xy1=(0, 0), slope=1, color='r', lw=2)
    ax2.set_xlabel('time_core1_alone')
    ax2.set_ylabel('time_core1_together')
    ax2.legend()
    ax2.set_xticks(bins,minor=True)
    ax2.set_yticks(bins,minor=True)
    ax2.grid(which='minor')
    ax2.set_title(f'imgep:{diversity_time_imgep}, rand:{diversity_time_rand}')


    bins_hist= np.arange(-100,100,5)
    bins = np.arange(0,100,5)
    ax3 = plt.subplot(323)
    ax3.hist(content_imgep['mutual']['time_core0'] - content_imgep['core0']['time_core0'], bins=bins_hist,alpha=.5, label='imgep')
    ax3.hist(content_random['mutual']['time_core0'] - content_random['core0']['time_core0'], bins=bins_hist,alpha=.5, label='random')
    ax3.set_xlabel('time[together] - time[alone]')
    ax3.legend()


    ax4 = plt.subplot(324)
    ax4.hist(content_imgep['mutual']['time_core1'] - content_imgep['core1']['time_core1'], bins=bins_hist,alpha=.5, label='imgep')
    ax4.hist(content_random['mutual']['time_core1'] - content_random['core1']['time_core1'], bins=bins_hist,alpha=.5, label='random')
    ax4.set_xlabel('time[together] - time[alone]')
    ax4.legend()




    ax5 = plt.subplot(313)
    bins = np.arange(0,max(np.max(content_imgep['mutual']['time_core0']),np.max(content_imgep['mutual']['time_core1'])),5)
    diversity_time_rand = diversity([content_random['mutual']['time_core0'],content_random['mutual']['time_core1']], [bins, bins])
    diversity_time_imgep = diversity([content_imgep['mutual']['time_core0'],content_imgep['mutual']['time_core1']], [bins, bins])
    ax5.scatter(content_imgep['mutual']['time_core0'],content_imgep['mutual']['time_core1'], label='imgep', alpha = .5)
    ax5.scatter(content_random['mutual']['time_core0'],content_random['mutual']['time_core1'], label='random', alpha = .5)
    ax5.set_xlabel('time_core0_together')
    ax5.set_ylabel('time_core1_together')
    ax5.legend()
    ax5.set_xticks(bins,minor=True)
    ax5.set_yticks(bins,minor=True)
    ax5.grid(which='minor')
    ax5.set_title(f'imgep:{diversity_time_imgep}, rand:{diversity_time_rand}')
    if title:
        fig.suptitle(title,fontsize = 15,y = .95)
    if name:
        k = 0
        while os.path.isfile(f'{name}_{k}.png'):
            k+=1
        plt.savefig(f'{name}_{k}.png',bbox_inches = 'tight',pad_inches = 0)
    if show:
        plt.show()
    plt.close()


def comparaison_ratios_iterations(contents:list[tuple], name = None,k = None):
    plt.figure()
    fig, axs = plt.subplots(8,1, figsize = (25,20), layout='constrained')

    bins = np.arange(-1.0,1.0,0.05)
    for j in range(4):
        for row in range(2):
            for label, content in contents:
                ll = len(content['core0']['miss_ratios_detailled'])
                diversity_ratio = [diversity([content['core0']['miss_ratios_detailled'][:k,row,j],  content['mutual']['miss_ratios_detailled'][:k,row,j]], [bins, bins]) for k in range(0,ll+1,100)]
                axs[j+row*4].plot(range(0,ll+1,100),diversity_ratio, label=label)
                axs[j+row*4].set_xlabel('iteration',fontsize=18)
                axs[j+row*4].set_ylabel('diversity',fontsize=18)
                axs[j+row*4].legend()
                axs[j+row*4].set_title(f'Mutual Vs Isolation bank {j},row {row}', fontsize=20)
    if name:
        plt.savefig(name)
    plt.close()


def diversity_time_iteration(content_random,content_imgep,title=None, folder="images"):
    count_bins = lambda content: np.arange(0,max(np.max(content['mutual']['time_core0']),np.max(content['mutual']['time_core1'])),5)
    ll = len(content_random['core0']['miss_ratios_detailled'])
    bins = count_bins(content_random)
    plt.figure()
    diversity_time_random = [diversity([content_random['mutual']['time_core0'][:k],content_random['mutual']['time_core1'][:k]], [bins, bins]) for k in range(0,ll,100)]
    plt.plot(range(0,ll,100),diversity_time_random, label='random')
    diversity_time_imgep = [diversity([content_imgep['mutual']["time_core0"][:k],content_imgep['mutual']["time_core1"][:k]],[bins, bins]) for k in range(0,ll,100)]
    plt.plot(range(0,ll,100),diversity_time_imgep, label=f"imgep k = 1")
    plt.xlabel("iteration")
    plt.ylabel("diversity")
    if title:
        plt.title(title)
    else:
        plt.title("time")
    plt.legend()
    if title:
        plt.savefig(f"{folder}/{title}")
    plt.close()
