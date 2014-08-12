kerbalcat
=========

Kerbal Space Program rocket launch simulation

##Current limitations:
- single stage
- 100% throttle
- straight up (only Z)

##Todo
- finish adding components
- finish stages

##Verification
###Verification case #1
```
Command Pod Mk1
FL-T800 Fuel Tank
LV-T45 Liquid Fuel Engine

Predicted:
Max altitude:  101666.716018m @ 211.6s
Max velocity:  1129.50143115m/s @ 69.0s

Actual:
Max altitude:  102928m @ ~212s
Max velocity:  ~1134.2m/s @ ~68.0s

Percent Difference:
Max altitude:  1.233%
Max velocity:  0.4151%
```

###Verification case #2
```
Command Pod Mk1
FL-T100 Fuel Tank
LV-909 Liquid Fuel Engine

Predicted:
Max altitude:  5859.83755715m @ 47.1s
Max velocity:  222.257058772m/s @ 31.14s

Actual:
Max altitude:  6086m @ ~47s
Max velocity:  ~227.2m/s @ ~31s

Percent Difference:
Max altitude:  3.7865%
Max velocity:  2.1995%%
```
