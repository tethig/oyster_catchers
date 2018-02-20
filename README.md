# Discovery of mesa via this blog post
https://dadaromeo.github.io/posts/mesa-a-library-for-agent-based-modeling-in-python/
My conda notes [are here](https://github.com/tethig/turbo-spoon/blob/master/Installing%20Python.md).

# Introductory tutorial
Mesa's own intoductory tutorial [is linked here](http://mesa.readthedocs.io/en/latest/tutorials/intro_tutorial.html).

# Requirements
The above tutorial references [this list of requirements](https://github.com/projectmesa/mesa/blob/master/examples/boltzmann_wealth_model/requirements.txt).

# Create the mesa environment
To build the environment for mesa:
```
conda create -n mesa jupyter matplotlib numpy
conda activate mesa
pip install mesa
conda env export -n mesa > environment.yml
```
Note that pip also installed pandas and tqdm.

During that process I updated to a new conda
This can be added to .bash_profile:
```
echo ". /anaconda3/etc/profile.d/conda.sh" >> ~/.bash_profile
```
# Separate scripts
OK, super - I have created a set of python scripts that call each other. Run the server.py script to instantiate a simulation that you can view as it runs:

```
python server.py
```
A web page should open giving an interactive simulation session.