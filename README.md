# What to observe
We want to observe revelant data that provides material for analysis of sources of interference.

We make the folloing hypothesis:
* The exact queue contents of the ddr is avaible for every cycle
* Acces to *miss* and *hit* information for every cycle.


Observables:
```python
 {'cycle': 20,
  'type': 'DDR_MEMORY_CONTENTION',
  'resource': 'DDR_MEMORY',
  'initiators': [0, 1],
  'details': {'banks': [0, 0],
   'rows': [0, 0],
   'operations': ['read', 'read'],
   'statuses': ['ROW HIT', 'waiting'],
   'bank_conflicts': True,
   'row_conflicts': False}},
 {'cycle': 24,
  'type': 'DDR_MEMORY_CONTENTION',
  'resource': 'DDR_MEMORY',
  'initiators': [0, 1, 1],
  'details': {'banks': [2, 0, 2],
   'rows': [0, 0, 0],
   'operations': ['read', 'read', 'read'],
   'statuses': ['ROW HIT', 'waiting', 'waiting'],
   'bank_conflicts': True,
   'row_conflicts': False}}
```



On pourra resumer un evenement de contention dans la ddr comme:

{type: hit/miss 
delay: delay,
current location:row and bank 
current command type
previous location:row and bank 
previous command type}



