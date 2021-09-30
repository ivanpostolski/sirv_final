from pypdevs.infinity import INFINITY
import numpy as np
import math
from scipy import stats

# Vaccination Strategies

def default_strategy_fun(agent,env,props):
    if agent.deg == 0:
        return INFINITY
    else:
        return np.random.exponential(float(1)/(float(props.PHI)*env.vaccine_scale))

default_strategy = {"name": "default_strategy", "fun": default_strategy_fun}


def double_default_strategy_fun(agent,env,props):
    if agent.deg == 0:
        return INFINITY
    else:
        return np.random.exponential(np.random.exponential(float(1)/(float(props.PHI)*env.vaccine_scale)))

double_default_strategy = {"name": "double_default_strategy", "fun": double_default_strategy_fun}


def triple_default_strategy_fun(agent,env,props):
    if agent.deg == 0:
        return INFINITY
    else:
        return np.random.exponential(np.random.exponential(np.random.exponential(float(1)/(float(props.PHI)*env.vaccine_scale))))

triple_default_strategy = {"name": "triple_default_strategy", "fun": triple_default_strategy_fun}

def degree_based_strategy_fun(agent,env,props):
    if agent.deg == 0:
        return INFINITY
    else: 
        return np.random.exponential(float(1)/((float(agent.deg)*env.vaccine_scale)))

degree_based_strategy = {"name": "degree_based_strategy", "fun": degree_based_strategy_fun}


def double_degree_based_strategy_fun(agent,env,props):
    if agent.deg == 0:
        return INFINITY
    else: 
        return np.random.exponential(np.random.exponential(float(1)/((float(agent.deg)*env.vaccine_scale))))

double_degree_based_strategy = {"name": "double_degree_based_strategy", "fun": double_degree_based_strategy_fun}


def triple_degree_based_strategy_fun(agent,env,props):
    if agent.deg == 0:
        return INFINITY
    else: 
        return np.random.exponential(np.random.exponential(np.random.exponential(float(1)/((float(agent.deg)*env.vaccine_scale)))))

triple_degree_based_strategy = {"name": "triple_degree_based_strategy", "fun": triple_degree_based_strategy_fun}

# Degree distributions

def poisson_5_gen(agent):
    return np.random.poisson(5)


poisson_5 = {"generator":poisson_5_gen, "mean":5.0, "name": "poisson_5"}

def bimodal_poisson_3_L13_gen(agent):
    if np.random.random() <= 0.8:
        return np.random.poisson(3)
    else:
        return 13

bimodal = {"generator":bimodal_poisson_3_L13_gen, "mean": 5.0 ,"name": "bimodal"}

xk1=np.arange(0,30,1)
pk1=np.zeros(30)
for i in range(30):
  pk1[i]=5**i*np.exp(-5)/math.factorial(i)

custm1 = stats.rv_discrete(name='custm', values=(xk1, pk1))

def power_law_gen(agent):
    return custm1.rvs(size=1)[0]


power_law = {"generator":power_law_gen, "mean": 5.0 ,"name": "power_law"}

regular_5 = {"generator":lambda x: 5, "mean": 5.0 ,"name": "regular_5"} 


default_vaccine_props = {"name":"s=0.05_limit=inf", "vaccine_scale": 0.05, "vaccine_limit": INFINITY } 