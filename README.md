# Ben's Learning Curve for Agent-based Simulation with Mesa

## Pre-amble
I discovered the *mesa* library via [this blog post](https://dadaromeo.github.io/posts/mesa-a-library-for-agent-based-modeling-in-python/). My conda notes, which can be used to help with installation issues [are here](https://github.com/tethig/turbo-spoon/blob/master/(Ana)conda.md). Please note that the wolf-sheep folder is modified from the mesa examples folder.

## Introductory Tutorial
Mesa's own intoductory tutorial [is linked here](http://mesa.readthedocs.io/en/latest/tutorials/intro_tutorial.html).

## Requirements
The above tutorial references [this list of requirements](https://github.com/projectmesa/mesa/blob/master/examples/boltzmann_wealth_model/requirements.txt).

## Create the Mesa Environment
To build the environment for mesa:
```
conda create -n mesa jupyter matplotlib numpy
conda activate mesa
pip install mesa
conda env export -n mesa > environment.yml
```
Note that pip also installed pandas and tqdm.

## Separate Scripts
OK, super - I have created a set of python scripts that call each other. Run the server.py script to instantiate a simulation that you can view as it runs:

```
python server.py
```
A web page should open giving an interactive simulation session.

## Wolf-sheep Run with Mesa
The wolf-sheep scripts would make a better starting point for my simulation. Let's contrast with Netlogo:

Model | sheep-wolves-grass
------|-------------------
Initial sheep number | 100
Initial wolf number | 50
Grass regrowth time | 30
Sheep gain from food | 4
Sheep reproduce | 4%
Wolf gain from food | 20
Wolf reproduce | 5%
World | torus 51 X 51

I note similar dynamics when world size is increased in mesa model (from default 20 by 20). Previously I had observed unstable dynamics with mesa's default world size. Additional issues: the grass is black! I believe I previously observed revenant wolves (recovering from extinction)- but I cannot recapitulate that behaviour.

## Bug-fixing the Grass
I have fixed the grass colour issue in my fork of mesa repo. I have [raised a ticket](https://github.com/projectmesa/mesa/issues/474) and sought advice from mesa developers to ensure compliance with their rules.

Meanwhile I will run test. Extra libraries:
```
pip install flake8 nose
conda env export -n mesa > environment.yml
```
In my mesa fork, I figured out there's a requirements file for test dependencies!
```
pip install -r requirements.txt
(mesa) NHBLAP-MAC01:mesa bio3dickib$ nosetests --with-coverage --cover-package=mesa
102it [00:00, 2747.77it/s]
102it [00:00, 3209.97it/s]
102it [00:00, 3279.01it/s]
51it [00:00, 2892.31it/s]
................................................................................
Name                                                    Stmts   Miss  Cover
---------------------------------------------------------------------------
mesa.py                                                     9      0   100%
mesa/agent.py                                               7      0   100%
mesa/batchrunner.py                                        97      6    94%
mesa/datacollection.py                                     73      1    99%
mesa/model.py                                              18      4    78%
mesa/space.py                                             290     18    94%
mesa/time.py                                               52      1    98%
mesa/visualization/ModularVisualization.py                120     43    64%
mesa/visualization/UserParam.py                            50      4    92%
mesa/visualization.py                                       1      0   100%
mesa/visualization/modules/CanvasGridVisualization.py      25      0   100%
mesa/visualization/modules/ChartVisualization.py           25     18    28%
mesa/visualization/modules/HexGridVisualization.py         28     18    36%
mesa/visualization/modules/NetworkVisualization.py         16     10    38%
mesa/visualization/modules/TextVisualization.py             5      0   100%
mesa/visualization/modules.py                               6      0   100%
---------------------------------------------------------------------------
TOTAL                                                     822    123    85%
----------------------------------------------------------------------
Ran 83 tests in 1.346s

OK
(mesa) NHBLAP-MAC01:mesa bio3dickib$ flake8 . --ignore=F403,E501,E123,E128 --exclude=docs,build
./examples/wolf_sheep/wolf_sheep/server.py:34:9: E265 block comment should start with '# '
```
I don't understand nose test results yet. I have addressed the flake8 errors now.

## Icons
<a href="https://icons8.com">Icon pack by Icons8</a>

![Image](../master/resources/bird.png?raw=true)

[Link for Bird Image](https://icons8.com/icon/50494/bird)

![Image](../master/resources/limpet.png?raw=true)

[Link for Shellfish Image](https://icons8.com/icon/37550/shellfish)
