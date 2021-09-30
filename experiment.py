# Copyright 2014 Modelling, Simulation and Design Lab (MSDL) at 
# McGill University and the University of Antwerp (http://msdl.cs.mcgill.ca/)
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Import code for model simulation:
from networkx.algorithms import regular
from pypdevs.infinity import INFINITY
from pypdevs.simulator import Simulator
import itertools
import os
import progressbar
import pandas as pd
import fileinput
import tempfile
import fnmatch
from matplotlib import pyplot as plt
# Import the model to be simulated
from model import Environment, Parameters
import numpy as np
import math

#    ======================================================================

# 1. Instantiate the (Coupled or Atomic) DEVS at the root of the 
#  hierarchical model. This effectively instantiates the whole model 
#  thanks to the recursion in the DEVS model constructors (__init__).
#

#    ======================================================================

# 2. Link the model to a DEVS Simulator: 
#  i.e., create an instance of the 'Simulator' class,
#  using the model as a parameter.

#    ======================================================================

# 3. Perform all necessary configurations, the most commonly used are:

# A. Termination time (or termination condition)
#    Using a termination condition will execute a provided function at
#    every simulation step, making it possible to check for certain states
#    being reached.
#    It should return True to stop simulation, or Falso to continue.
# def terminate_whenStateIsReached(clock, model):
#     return model.trafficLight.state.get() == "manual"
# sim.setTerminationCondition(terminate_whenStateIsReached)

#    A termination time is prefered over a termination condition,
#    as it is much simpler to use.
#    e.g. to simulate until simulation time 400.0 is reached

# B. Set the use of a tracer to show what happened during the simulation run
#    Both writing to stdout or file is possible:
#    pass None for stdout, or a filename for writing to that file
# sim.setVerbose(None)

# C. Use Classic DEVS instead of Parallel DEVS
#    If your model uses Classic DEVS, this configuration MUST be set as
#    otherwise errors are guaranteed to happen.
#    Without this option, events will be remapped and the select function
#    will never be called.

#    ======================================================================

import model
import networkx as nx
import seaborn as sns
from scipy import stats

from multiprocessing import Process

# from SIRSS_numeric import sir_num

SMALL_SIZE = 16
MEDIUM_SIZE = 20
BIGGER_SIZE = 24

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)

DURATION = 10
RETRIES = 10
output_columns = ['t','I','S','R','V','retry']

from vaccine_strategies import *

one_big_brother_dist = [4]*299 + [298] 
one_big_brother_mean = sum(one_big_brother_dist)/float(len(one_big_brother_dist))

def one_big_brother_gen(agent):
    return one_big_brother_dist[agent.id]

one_big_brother = {"generator":one_big_brother_gen, "mean":one_big_brother_mean, "name": "one_big_brother"}

xk1=np.arange(0,30,1)
pk1=np.zeros(30)
for i in range(30):
  pk1[i]=5**i*np.exp(-5)/math.factorial(i)

custm1 = stats.rv_discrete(name='custm', values=(xk1, pk1))

xk1=np.arange(0,51,1)
pk1=np.zeros(51)
for i in range(51):
  pk1[i]=0.73*(3)**i*np.exp(-3)/math.factorial(i)

q=0.27*np.array([1,0,0,0])
pk1[8]+=q[0]
pk1[21]+=q[1]
pk1[25]+=q[2]
pk1[50]+=q[3]

custm2 = stats.rv_discrete(name='custm', values=(xk1, pk1))


def bimodal_poisson_27_3():
    if np.random.random() <= 0.1:
        return np.random.poisson(27)
    else: 
        return np.random.poisson(2.56)


dfs = []
def run_single(retry=0,vaccine_props=default_vaccine_props,vaccine_strategy=default_strategy,degree_gen=bimodal):
    global dfs
    environ = Environment(degree_gen,vaccine_props,vaccine_strategy,name="SIR over CM")
    sim = Simulator(environ)
    initial_states = [(ag.state.name, ag.state.state, 0) for ag in environ.agents] 
    sim.setTerminationTime(DURATION)
    sim.setClassicDEVS()
    sim.setDSDEVS(True)
    topology_name = os.path.basename(Parameters.TOPOLOGY_FILE)
    # sim.setVerbose(None)
    sim.simulate()
    dataframe = pd.DataFrame(environ.log_agent.stats)
    dataframe.columns = ['t', 'S', 'I',  'R', 'V']
    dataframe['retry'] = retry
    dataframe['Quarantine Threshold'] = Parameters.QUARANTINE_THRESHOLD
    dataframe['Quarantine Acceptance'] = Parameters.QUARANTINE_ACCEPTATION
    tmpfile = tempfile.NamedTemporaryFile(mode='w', prefix='sir_model', delete=False)
    dataframe.to_csv(tmpfile, header=False, index=False)
    outfilename = "results/pa_model_dynamic_graph_%s.gml" % (topology_name)
    nx.write_gml(environ.G, outfilename)
    dfs.append(dataframe)

def run_multiple_retries(vaccine_strategy,dist_gen,vaccine_props):
    Parameters.TOPOLOGY_FILE = 'grafos_ejemplo/grafo_vacio'

    topology_name = os.path.basename(Parameters.TOPOLOGY_FILE)
    for i in range(RETRIES):
        run_single(retry=i,vaccine_strategy=vaccine_strategy,vaccine_props=vaccine_props,degree_gen=dist_gen)

# for i in [1, 0.10, 0.40]:
#     Parameters.QUARANTINE_THRESHOLD = 0.15
#     Parameters.QUARANTINE_ACCEPTATION = i

# strategies = [default_strategy,degree_based_strategy,double_degree_based_strategy,triple_degree_based_strategy]
strategies = [degree_based_strategy] 

# distributions = [poisson_5, bimodal, power_law, regular_5] 
distributions = [bimodal] 

# distributions = [bimodal] 

vaccine_factors = [default_vaccine_props] 
vaccine_factors_all = [{"name":"s=%.3f_limit=inf" % scale, "vaccine_scale": scale, "vaccine_limit": INFINITY } for scale in [0.001,0.005,0.010,0.050,0.100,0.200,0.300,0.400]]

vaccine_factors_100 = [{"name":"s=%.3f_limit=inf" % scale, "vaccine_scale": scale, "vaccine_limit": INFINITY } for scale in np.linspace(0.001,0.5,100)]

vaccine_factors_100_10 = [{"name":"s=%.3f_limit=0.10" % scale, "vaccine_scale": scale, "vaccine_limit": 0.10*300} for scale in np.linspace(0.001,0.5,100)]

vaccine_factors_100_25 = [{"name":"s=%.3f_limit=0.25" % scale, "vaccine_scale": scale, "vaccine_limit": 0.25*300} for scale in np.linspace(0.001,0.5,100)]

vaccine_factors_100_50 = [{"name":"s=%.3f_limit=0.50" % scale, "vaccine_scale": scale, "vaccine_limit": 0.50*300} for scale in np.linspace(0.001,0.5,100)]

vaccine_factors_100_75 = [{"name":"s=%.3f_limit=0.75" % scale, "vaccine_scale": scale, "vaccine_limit": 0.75*300} for scale in np.linspace(0.001,0.5,100)]


def run_strategy_experiments():

    for vaccine_strategy in strategies:
        for dist_gen in distributions:
            for vaccine_props in vaccine_factors_100_25:
                run_experiments(vaccine_strategy,dist_gen,vaccine_props)

def run_experiments(vaccine_strategy,dist_gen,vaccine_props):

    run_multiple_retries(vaccine_strategy,dist_gen,vaccine_props)

    data = pd.concat(dfs)
    data.to_csv('paraNumeric.csv')

    aux = data.groupby('retry').max().reset_index()
    aux = aux[(aux.R > 50)]
    data = data[data.retry.isin(aux.retry)]
    data_melteada = pd.melt(data, id_vars=['t', 'retry', 'Quarantine Threshold', 'Quarantine Acceptance'], value_vars=['I', 'S', 'R','V'])

    data_melteada['value'] = data_melteada['value'] / float(300)
    data_melteada = data_melteada.rename(columns={'variable': 'State', 't': 'Time', 'value': 'Proportion'})

    fig, ax =plt.subplots(figsize=(12, 14))
    colors=["#FF0B04","#4374B3","#228800"]
    sns.set_palette(sns.color_palette(colors))
    sns.lineplot(data=data_melteada, x='Time', y='Proportion', hue='State', style='Quarantine Acceptance',  ax=ax,color=['r','g','b','y'], ci=None)

    plt.setp(ax,yticks=np.arange(0, 1.01, 0.10))
    #plt.legend()
    fontdict = {'fontsize': 25, 'fontweight' : 100, 'verticalalignment': 'baseline', 'horizontalalignment': 'center'}
    plt.title("%s  %s" % (vaccine_strategy["name"],vaccine_props["name"]),fontdict)
    # plt.legend(bbox_to_anchor=( 0., 1.02,1.,.102),loc=3,prop={'size': 6},ncol=2, mode="expand",borderaxespad=0.,title='SIR with Quarantine') #, borderaxespad=0.)

    plt.tight_layout()
    plt.savefig('results/%s_%s_%s.png' %(dist_gen["name"],vaccine_strategy["name"],vaccine_props["name"]), bbox_inches='tight')

# run_strategy_experiments()

import sys
import os

if __name__ == '__main__':
    print("Simulating with parameters")
    vaccine_strategy = eval(sys.argv[1])
    print("strategy: %s" % str(vaccine_strategy["name"]))
    vaccine_factors = eval(sys.argv[3])
    dist = eval(sys.argv[2])
    print("distribution: %s" % str(dist["name"]))
    for vaccine_props in vaccine_factors:     
        print("props: %s" % str(vaccine_props))
        if os.path.exists('results/%s_%s_%s.png' %(dist["name"],vaccine_strategy["name"],vaccine_props["name"])):
            continue
        run_experiments(vaccine_strategy,dist,vaccine_props)
