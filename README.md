# 

# Presentation
The shift from single-core to multi-core architectures is essential in safety-critical embedded systems in multiple domains such as aerospace and automotive, driven by both the need to enhance processor performance for increasingly demanding applications and adaptation to recent technology. However, this transition introduces new complexities, particularly hardware contention issues known as inter-core interferences.

The objective of this project is to apply automated exploration algorithms to the novel use case  of identification of inter-core interference sources in multi-core architectures. Indeed, undesirable phenomena such as temporal interference can occur due to concurrent access to shared resources (e.g. memory buses, caches etc …). Due to the hardware complexities, the conditions under which interference occurs, as well as their effects, can vary greatly and often seem random, making them very difficult to model and to predict. In other words, such architectures are complex systems. Thus we believe that our automated discovery algorithms can be very useful to characterize their behavior.

The purpose of the study is to developp a framework to automatically identify sources of interference on multi-core platforms:

* Identify all micro architectural mechanisms that can lead to the occurrence of an interference.
* Identify the conditions under which the corresponding interferences occur.

In order to provide a proof of concept for applying automated discovery framework on the problem of interference identification, one choose to explore a simplified simulated model of mutli-core architectures.

This will require finding sequences of code that generate a maximal diversity of interference mechanisms. The
following curiosity-driven exploration method will be applied to identify hardware interference patterns. It relies
on the construction of an autonomous AI agent that can learn to represent, generate, select, and solve its own
problems to efficiently explore the vast outcome space of artificial or natural complex systems. These methods
aim to address the knowledge gap between our ability to manipulate low-level inputs of complex systems and our
ability to discover controllable properties. Moreover, these methods help deal with a limited experimental budget

## What is an interference ?
An interference is a phenomenon such that, for identical initial conditions, the execution time of an application S1
running in isolation (S1 , _) on a platform differs from the execution time of S1 running with an application S2 on
the platform. (S1 , S2 ).
## Automated Discovery process
An exploration consists of several steps: 1) choosing the experimental parameters, 2) launching an experiment in the
system with the input parameters, 3) measuring the outcomes into numerical vectors describing some of the observed
properties, and 4) collecting the results in a database.

The Intrinsically Motivated Goal Exploration Process algorithm architecture is a diversity-driven strategy that aims to
maximally cover an observation space or a behaviour space by selecting parameters leading to the highest diversity in
that space. From the IMGEP architecture perspective, an element of a behaviour space is seen as a goal to reach. The
algorithm architecture 1 relies on the definition of exploration 2.1. The autotelic agent firstly samples the goals to solve
and then uses a strategy to solve them. Two internal models are used for these respective aspects, a goal generator G
and a goal strategy achievement model $\Pi$. During the exploration, the agent fills a database $\mathcal{H}$ used to update its internal models, and thus the data acquired is reused to extract potential solutions to solve other goals.

IMGEP addresses solutions to explore, with a limited budget, complex systems suffering from butterfly effects, attrac-
tor effects, or stochasticity.

**Justify choice of population based imgep**
# Simulator description
In order to provide a proof of concept for applying automated discovery framework on the problem of interference identification, one choose to explore a simplified simulated model of mutli-core architectures.

![Alt text|306x345](illustrations/simulator_new.png)

We work with a minimal 
A full description of the simulator can be found in [Simu3](https://github.com/Ludoviccccc/Simu3)
## DDR model
The memory consists of several banks, each of which has a row buffer (a form of cache). Each bank is managed by a timed state machine which includes the one described in [1] (see figure above)
The state of the banks of the DDR determines the completion dates of operations. The requests are issued by the DDR controller
## DDR Controller model

The DDR model and that of the memory controller are coupled.
At each cycle,the controller determines which requests are completed i.e. the current date is greater than the scheduled completion date. In this case, and for a request of type 'read', the controller informs core that the access is completed. This signal is used by the core to unlock the execution of a new instruction. No signal is provided in the case of a write request.

The controller processes requests located in its input queue. For each request, it determines if it can be processed by the DDR according to its state (managed by the state machine of the DDR) ensuring the constraints of minimum delays (cf [1]). Then it determines the "best" request to process based on a ranking established to prioritize requests resulting in a "row hit", write requests over read requests and the arrival order (FIFO). Finally, it transmits the "best" request to the DDR. The DDR Controller model takes up the "main lines" of the general mechanisms described in [1].

## Core model
The simulation of cores handles exclusively memory accesses instructions.  In other words, the instruction set is reduced to read and write (load and store) operations in memory since, ultimately, only memory accesses are simulated.

For each core, a simple loop models the "fetch and execute" cycle.

At each iteration of the loop (thus, each CPU cycle), the core can

    wait for the end of a read operation
    execute a "read" (load);
    execute a "write" (store).
    execute an instruction that does not perform memory accesses, which, in the case of the simulator, amounts to doing nothing.


This model is obviously very simplified compared to the actual operation of a physical target device.


  Waiting for the completion of a read memory access to continue the code execution does not correspond to reality because the processor has various mechanisms precisely allowing to hide these latencies. This wait is only necessary to preserve the true enter access dependencies (e.g., a @a LD sequence, WR @a must be preserved at run time to maintain program semantics).

## Cache model

Each cache level within the simulator is configurable with parameters such as total size, cache line size and associativity. 
One choose the behavior type to be 'write_back', that is to say, writing in lower-level memory occurs when the cache line is evicted. During the write operation, the line is simply marked "dirty" and when the line is evicted, it is written into the lower-level memory.It is also possible to implement a "write-through" behavior in which writing into the lower-level memory takes place immediately.
The management of the eviction of cache lines is carried out by a PLRU (PLRU class) whose role is to determine the line to be replaced based on the current state of the cache. Ideally, one would like to implement a behavior of the LRU (Least Recently Used) type, which would consist in eliminating the line used less recently in order to make the most of the locality principle. However, this strategy is expensive to implement and we often prefer to use a simpler mechanism called Pseudo-LRU which relies on a binary tree.
This algorithm includes:
  * a function allowing to maintain the data structure (binary tree) which will allow to choose the next row to be evicted according to memory accesses ("update_on-access")
  * a function allowing to choose the next cache line to remove ("get_victim") from the information contained in the binary tree.
  * The last level cache (L2 in current code) is shared by both memory hierarchies, core 0 and core 1.

Note taht there is no cache coherency management mechanism.

# Some tests for the behavior of the simulator

* this following notebook gathers some tests [test_simulator.ipynb](test_simulator.ipynb)
* 1 core, 2 read cycles,same index, same tag, same bank, different rows, no dependency
* 1st RD => cache miss => DDR reads transaction 
* 2nd RD => cache miss => DDR reads transaction 
```python
GlobalVar.clear_history()
# Create instruction sequences
inst0 = { 0: ('read', 0), 60: ('read', 20) }
inst1 = {  }
exp=Experiment()
exp.load_instr(inst0, inst1)
results = exp.simulate(200,display_stats=True)
import pandas as pd
print('DDR miss ratio:')
pd.DataFrame(results['miss_ratios_detailled'],columns=[f'bank {j}' for j in range(4)],index = [f'row {j}' for j in range(2)])
```
produces:
```
core0 {'level': 'L1', 'hits': 0, 'misses': 2, 'miss_rate': 1.0}
core1 {'level': 'L1', 'hits': 0, 'misses': 0, 'miss_rate': 0}
shared cache L2 {'level': 'L2', 'hits': 0, 'misses': 2, 'miss_rate': 1.0}
ddr hits [[0. 0. 0. 0.]
 [0. 0. 0. 0.]]
ddr miss [[1. 0. 0. 0.]
 [1. 0. 0. 0.]]
DDR miss ratio:
	bank 0 	bank 1 	bank 2 	bank 3
row 0 	1.0 	-0.0 	-0.0 	-0.0
row 1 	1.0 	-0.0 	-0.0 	-0.0
```

* 1 core, 2 read cycles, same cache line, no dependency
* 1st RD => cache miss => DDR reads transaction 
* 2nd RD => cache hit => no DDR transaction
```python
# Create instruction sequences
GlobalVar.clear_history()
inst0 = { 0: ('read', 0), 60: ('read', 0) }
inst1 = {}

exp=Experiment()
exp.load_instr(inst0, inst1)
results = exp.simulate(200, display_stats=True)
print('DDR miss ratio:')
pd.DataFrame(results['miss_ratios_detailled'],columns=[f'bank {j}' for j in range(4)],index = [f'row {j}' for j in range(2)])
```
output
```
--- Simulation Stats ---
core0 {'level': 'L1', 'hits': 0, 'misses': 2, 'miss_rate': 1.0}
core1 {'level': 'L1', 'hits': 0, 'misses': 0, 'miss_rate': 0}
shared cache L2 {'level': 'L2', 'hits': 0, 'misses': 2, 'miss_rate': 1.0}
ddr hits [[1. 0. 0. 0.]
 [0. 0. 0. 0.]]
ddr miss [[1. 0. 0. 0.]
 [0. 0. 0. 0.]]
DDR miss ratio:
	bank 0 	bank 1 	bank 2 	bank 3
row 0 	0.5 	-0.0 	-0.0 	-0.0
row 1 	-0.0 	-0.0 	-0.0 	-0.0
```
# Apply Intrinsically motivated Goal exploration process
![Alt text](illustrations/imgep_scheme.png)
## Parameter space
Because we find it revelant to study interference patterns occuring with independant programs, we divide in two parts the set of 101 adresses from 0 to 100 for core 0 and 1. 
* Core 1: addresses from 0 to 49
* Core 2: addresses from 50 to 100
  
In order to make trackable analysis, we choose the length of the applications to be from 1 to 10, and the 
Sequences will look like this:
```python
{4: ('write', 3),
 6: ('write', 14),
 8: ('write', 15),
 9: ('read', 7),
 16: ('write', 0),
 48: ('read', 17),
 51: ('read', 2),
 56: ('write', 2),
 60: ('write', 10)}
```
## What to observe

We want to observe relevant data that provides material for analysis of sources of interference.


For the material device at least the following information is avaible and thus also for the simulator:
| id | Performance counter      | Category | Description                     |
|----|--------------------------|----------|---------------------------------|
|    | Processor cycles         | General  | Nb of executed cycles           |
|    | Instruction completed    | General  | Nb of completed instructions    |
|    | decode stalled           | General  | Nb of cycles in a waiting status|
|    | L1/L2 cache misses       | L1/L2    | Nb of cache misses L1/L2           |
|    | L1/L2 cache store misses | L1/L2    | Nb of cache misses L1/L2 for stores|
|    | L1 cache load misses     | L1/L2    | Nb of cache misses L1/L2 for loads |
|    | L1 demand access         | L1/L2    | Nb of requests for L1/L2           |
|    | L1 store allocates       | L1/L2    | Nb of line allocations in L1/L2 |


For our simulator, at least the following is also avaiable :
| id | Performance counter      | Category | Description                     |
|----|--------------------------|----------|---------------------------------|
|    | DDR   cache misses       | DDR      | Nb of cache misses DDR          |
|    | DDR   cache store misses | DDR      | Nb of cache misses DDR for stores|
|    | DDR   cache load misses  | DDR      | Nb of cache misses DDR for loads|
|    | DDR   demand access      | DDR      | Nb of requests for DDR          |
|    | DDR   store allocates    | DDR      | Nb of line allocations in DDR   |

Since the simulator is a white box, one can also have acces to:
* The exact queue contents of the ddr is avaible for every cycle
* Statuses of every cache line
* Statuses of every row and bank 
## Goal Space
Our objective is to collect data points to form a cloud that spreads as much as possible in $\mathcal{G}$.

* In order to spot the occurence of interference, one can spot the changes of some well chosen data for execution in isolation vs non-isolation. Thus we will target the following values when applications are executed on isolation on cores 0 and 1 and in mutually i.e on both cores simultaneously.

| id | Category | Description                     |
|----|----------|---------------------------------|
|    | General  | Nb of executed cycles           |
|    | DDR      | miss ratios for DDR for every (bank,line)|
|    | L2       | miss ratios for cache L2|
|    | L2       | Nb of cache misses L2         |

Let:
* $\mathcal{T} = (t_{0,⋅}​(c_0​),t_{⋅,1}​(c_1​),t{0_,1}​(c_0​),t_{0,1}​(c_1​)) \subset \mathbb{R}^{4}$
* $\mathcal{D} = \{ratio[0,⋅],ratio[⋅,1],ratio[0,1],\forall \mbox{row},\mbox{banks}\}\subset\mathbb{R}^{\mbox{nb rows}\times\mbox{nb banks}\times 3}$
* $\mathcal{L} = \{\mbox{L2 cache miss ratio}\}\cup \{\mbox{Nb of cache misses L2}\}\subset\mathbb{R}^{2\times 3}$

We explore the product space: $\mathcal{G} = \mathcal{T}\times\mathcal{M}\times\{\mathcal{L}\}\subset\mathbb{R}^{4+\mbox{nb rows}\times\mbox{nb banks}\times 3+2}$

* We gather iteratively all the results in a matrix $A\in\mathbb{R}^{N,F}. F \approx 160, N $ is the growing number of individuals.
 The observable set can be partition as follow : $\mathcal{O} = \mathcal{T}\cup\mathcal{R}, \mathcal{T}\cap\mathcal{R}=\emptyset.  \mathcal{T}$ are time features and $\mathcal{R}$ are miss ratios informations. $\mathcal{T}$ and $\mathcal{R}$ are not exclusive set, in the sense that we can observe pairs of values $(t,m)\in\mathcal{T}\times\mathcal{R}$.


## Goal generation
For any event we track, we synthetize a vector. Thus, we generate vectors and not events as goals
* We show that targeting multidimensional goals help to increase the diversity along on the bordure, as opposed with an exclusive exploration along the axis.
* We choose 'large' vectors up to size $v\in\mathbb{R}^{F}$. Whenever we choose to sample a goal as a vector of size $v\in\mathbb{R}^{F}$, that is one third of the time,

* One third of the time, we also sample goals $g$ such that $\forall i: g_i\in\mathcal{T} $, and one other third such that $\forall i: g_i\in\mathcal{R} $.
* Periodically set the sampling boundaries based on the history $\mathcal{H}$, allowing to sample new goals *e.g*:
	* $\mbox{min}_{\mathcal{T}} g:= (\mbox{min } g_1,\cdots,\mbox{min } g_6)$
 	* $\mbox{max}_{\mathcal{T}} g:= (\mbox{max } g_1,\cdots,\mbox{max } g_6)$
 * Periodically sample goal uniformly in a slightly larger set, using two factors *e.g* $f_1 = 0.8,f_2 = 1.2$, $g\sim\mathcal{U}([f_1\mbox{min } g_1,f_2\mbox{max } g_2])\otimes\cdots\otimes\mathcal{U}([f_1\mbox{min } g_6,f_2\mbox{max }g_6])$
 * During exploration we also find out that setting bounds for the time values allows more diversity, as it helps to not enlarge the data cloud in a specific direction.
See [goal_generation.py](https://github.com/Ludoviccccc/ExplorationSimu3/blob/master/exploration/imgep/goal_generator.py)


## Mixing sequence operator
In order to conserve interference patterns, we use a mixing sequence operator that randomly selects segments of the disctinct programs to produce another one. This idea comes from the fact that interference comes from specific successions of instructions tath we can call segments. If we mix randomly two applications regardless of their order, we can expect to break the interference pattern and then to not get closer from our target. See [mixxx.py](https://github.com/Ludoviccccc/ExplorationSimu3/blob/master/exploration/imgep/mixxx.py)

## Mutation Operator
With a given number of actions as argument. The program either `add`,`delete` or `modify` an instruction. The modification can either be changing the `type`,`address` or both. See [mutation.py](https://github.com/Ludoviccccc/ExplorationSimu3/blob/master/exploration/imgep/mutation.py)
## Goal achievement strategy policy $\Pi$
![Alt text](illustrations/achievement_strategy.png)
* The method [OptimizatoinPolicy.py](https://github.com/Ludoviccccc/ExplorationSimu3/exploration/imgep/OptimizationPolicy.py) generates a pair of instruction sequences by selecting the closest observations stored in the database $\mathcal{H}$, mixing them and lightly mutate the resulting pair.
* We synthetize a weighted distance to avoid exploring specific regions of the total space. The weights will be periodically updated according to the feature magnitudes :
${||z||}^{2} = \sum_{j}{\frac{{z_{j}}^{2}}{{\mbox{max}}(A_{i,j},\forall i})}$

*  we then normalize features with their maximum magnitude. For instance if j is the executing time on the core 0, then I will replace $g_{i,j}$ with  $g_{j}/max(\{A_{i,j}, \forall 1\leq i \leq N\})$.

# Temporary exploration results
Run of 10000 iterations, 1000 for initialization.
* To assess the diversity of the resulting dataset, we design a diversity measure $\mathcal{D}$ on the entire space $\mathcal{O}\subset\mathbb{R}^{D}$ , and other measures $\mathcal{D}_{j}$ to evaluate the diversity along specific axis $j$. We choose $\mathcal{D}$ to be the cumulated squared distance between all the wise points. Measures $\mathcal{D}_j$ will be the sum of all non -empty bins in a defined histogram $H_j$.
* We compare k-NN goal strategy achievement IMGEP with a random exploration. Results [pictures ] show that using k-NN allows a more efficient exploration along the bordure of the domain $mathcal{O}$. Meanwhile the resulting diversity of the total space is not significantly larger.

* In order to target the right combination of parameter we perform a grid search on a product space of values of k and number of segments to split the programs. Parameters leading to the highest diversty will be selectionned.
* Parametric study with : k, number of segment for mixing operator/mixing method, exclusive exploration along axis vs non-exclusive exploration along axis
* Add diversity value: some of all squared distances

# Interpretation, diagnostics: 
* Analysis of acceleration phenomenon
* Visualisation of cache miss, ddr miss, and execution time + other space.
* Analyse the impact of exploring interference event observables.



Observation : imgep exhibe des couples de programmes dont les temps d’exécution sont bien plus importants qu’en random
pb : quels mécanismes causent les temps élevés :


H0 : imgep découvre des paires de programmes dont les adresses utilisées font overlapping + random découvre que très rarement de cas d’overlapping 

méthode 0 : pour tester: proposer méthode pour mesurer le overlap entre deux programmes, qui prend en compte que on connaît le mapping.
Prédiction : la mesure sera corrélée au temps d’exécution
on peut pas trouver en random + intéressant à trouver sur la source matérielle + est-ce qu’on voudrait éviter d’exploiter ce phénomène

 
Méthode 1 : méthode qui permet de 

![Alt text](illustrations/diversity_bar_core0.png)
![Alt text](illustrations/diversity_bar_core1.png)
![Alt text](illustrations/time_k_2_s_1_11.png)
![Alt text](illustrations/comparaison_iteration_ddr_miss_ratio.png)
## Acceleration phenomena
