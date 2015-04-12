# DBNN.NASA
We tackled the Neuromorphic Studies of Asteroid Imagery problem by constructing a demo of a tool that automatically fetches information about recently spotted asteroids, and uses a neural network to classify the composition of the asteroid.

We used the open source [DL4J API](http://deeplearning4j,org) to train our neural network to predict the composition of asteroids. This tool has the advantage of pluggable backend libraries, which means that the programs we wrote this weekend to run on a laptop can be converted to run on a GPU, a standard scientific HPC cluster, or a set of Amazon EC2 cloud computing resources, all by changing just one or two lines of code. It is licensed under Apache2. 

We used Python, [PySide](http://pyside.github.io/docs/pyside/) and [Matplotlib](http://matplotlib.org/) to make our visualizations of the network and asteroid data, to fetch content from online databases, and to link these together into a single application.

We used two primary sources for data - light curves from NASA’s [WISE mission](http://www.nasa.gov/mission_pages/WISE/main/), a infra-red space telescope which has imaged most of the solar system, and the new asteroid reports from the Minor Planet Center. Data for training the network was drawn from the [LINEAR](http://neo.jpl.nasa.gov/programs/linear.html) group’s classification of a group of 6000 asteroids merged with light curves from the WISE database. We then classify new asteroids from the [Minor Planet Center’s](http://minorplanetcenter.net/) reports by pulling corresponding light curves from the WISE mission and running them against our classifier.

Future work will focus on incorporating more predictive features into the neural network, ideally including raw pixel data from the images. Right now the performance of the network is not as good as it could be. If raw images could be used, then the network could undergo unsupervised training on a much larger dataset, which should dramatically improve performance. We also plan to provide an interface to allow users to upload their own images along with coordinate information, to automate classification of data gathered by citizen scientists.

![DBNN Screenshot](https://github.com/j3doucet/DBNN.NASA/blob/master/screenshot.png)
