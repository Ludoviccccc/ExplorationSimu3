# Simulator description
A description of the simulator can be find in [Simu3](https://github.com/Ludoviccccc/Simu3)
![Alt text](illustrations/simulator_new.png)
# What to observe
We want to observe relevant data that provides material for analysis of sources of interference.

We make the hypothesis that the simulator is a white box. The following will be accessible:
* The exact queue contents of the ddr is avaible for every cycle
* Acces to *miss* and *hit* information for every cycle.
* Statuses of every cache line
* Statuses of every row and bank 
## Parameter space
to define

## Observables:
First I choose to consider events that allow to know if there is competition between the two cores in the ddr. In the sens that two instructions from the distincts cores are waiting for scheduling stage in the main memory.
```python
{'cycle': 7,
   'type': 'DDR_MEMORY_CONTENTION',
   'resource': 'DDR_MEMORY',
   'initiators': [0, 1],
   'details': {'banks': [3, 3],
    'rows': [0, 1],
    'operations': ['read', 'read'],
    'statuses': ['ROW MISS', 'waiting'],
    'bank_conflicts': True,
    'row_conflicts': True}}

{'cycle': 35,
   'type': 'DDR_MEMORY_CONTENTION',
   'resource': 'DDR_MEMORY',
   'initiators': [1, 0, 1],
   'details': {'banks': [0, 2, 0],
    'rows': [1, 0, 0],
    'operations': ['read', 'read', 'read'],
    'statuses': ['ROW HIT', 'waiting', 'waiting'],
    'bank_conflicts': True,
    'row_conflicts': True}}
```
Altough we might lose information we'll associate well defined vectors to these event, in order to work with metric spaces. This will allow to measure proximity between such events:
```
 {'ratio_cores': array([0.5]),
  'count_banks': array([0., 0., 0., 1.]),
  'count_rows': array([0.5, 0.5]),
  'conflicts_bank_row': array([1, 1])})

 {'ratio_cores': array([0.66666667]),
  'count_banks': array([0.66666667, 0.        , 0.33333333, 0.        ]),
  'count_rows': array([0.66666667, 0.33333333]),
  'conflicts_bank_row': array([1, 1])})
```




We'll also work with events such as :
```
{type: hit/miss 
delay: delay,
current location:row and bank 
current command type
previous location:row and bank 
previous command type}
```
# Temporary exploration results

![Alt text](illustrations/miss_ratios_k_1_s_1_4.png)
![Alt text](illustrations/time_k_1_s_1_3.png)
