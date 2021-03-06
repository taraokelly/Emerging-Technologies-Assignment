# Emerging-Technologies-Assignment

*An application to recognize handwritten digits written in Python using Flask and Tensorflow. Forth Year, Emerging Technologies, Software Development.*

## Table of Contents

+ [Introduction](#introduction)
+ [Project Specification](#project-specification)
+ [Technologies](#technologies)
+ [Implemention](#implemention)
+ [User Guide](#user-guide)
+ [References](#references)

## Introduction

As apparent by its presence in the latest Gartner Hype Cycle for Emerging Technologies (currently 2017), **Machine Learning**, and its ongoing research, is receiving a lot of attention right now. The name machine learning, in my opinion, is quite self-explanitory. Machine learning focuses on enabling machines to learn from data. Subsequently, facilitating the machine to make decisions and predictions based on that data. 
The following project has been assigned by lecturer [Ian McLoughlin](https://ianmcloughlin.github.io/) to assist the learning of the module [Emerging Technologies](https://emerging-technologies.github.io). It is a basic implementation of supervised machine learning, trained using the [MNIST](http://yann.lecun.com/exdb/mnist/) data sets of images and corresponding labels. For the sake of simplicity, the UI will be actualized in the form of a simple single web page.

## Project Specification

The following are your instructions to complete the project for the module [Emerging Technologies](https://emerging-technologies.github.io) for 2017.
This project is worth [40% of your marks for the module](https://emerging-technologies.github.io/#assessment-information).
Please see the [course homepage for the deadline](https://emerging-technologies.github.io/#submit-ca).

### Overview
In this project you will create a web application in Python to recognise digits in images.
Users will be able to visit the web application through their browser, submit (or draw) an image containing a single digit, and the web application will respond with the digit contained in the image.
You should use [tensorflow](https://www.tensorflow.org/) and [flask](http://flask.pocoo.org/) to do this.
Note that accuracy of approximately 99% is considered excellent in recognising digits, so it is okay if your algorithm gets it wrong sometimes.

### Instructions
1. Create a git repository with a README.md and an appropriate gitignore file. The README should explain who you are, why you created the application, how you created it, how to download and run it, and summarise any references you have used.
2. In the repository, create a web application that serves a HTML page as the root resource. The page should contain an input where the user can upload (or draw) an image containing a digit, and an area to display the image and the digit.
3. Add a route to your application that accepts requests containing a user input image and responds with the digit.
4. Connect the HTML page to the route using AJAX.

### Submission
To submit your project, you must make your git repository available using a git hosting service like [GitHub](https://github.com/) or [GitLab](https://gitlab.com).
Use the [submission link on the course webpage](https://emerging-technologies.github.io/#submit-ca) to submit the URL for your hosted repository.
You can submit at any time before the deadline, the earlier the better, as the last commit you make to the repository before the deadline will be corrected irrespective of when you submitted your link.
If your repository is private you must add the lecturer as a collaborator.

### Grading 
Your project will be graded using the following rubric.

| Category      | Description                            | Poor | Fair | Average | Excellent | Distinct |
|---------------|----------------------------------------|------|------|---------|-----------|----------|
| Research      | Investigation of problem and solutions | | | | | |
| Development   | Architecture and code                  | | | | | |
| Consistency   | Planning and pragmatism                | | | | | |
| Documentation | Descriptions and explanations          | | | | | |

## Technologies

### Python

Python is a simple yet powerful programming language. It offers programmers the rare ability to focus mainly on the solution, and less on adhering to a strict syntax. This lightweight web application and it's handling of machine learning is attributed to Python's extensive libraries. I used [Python](https://www.python.org/) 3 and the flask framework for the server-side scripting. I used the @app.route decorator to map the URL to functions in my flask application.

### Tensorflow

[TensorFlow](https://www.tensorflow.org/) is a powerful library for doing large-scale numerical computation. It does so using data flow graphs. One of the tasks at which it excels is implementing and training deep neural networks. 

## Implemention

At first I considered using keras, a library that can use tensorflow as a backend, as module resources supply a easy to follow example that builds, trains and validates a model. However, Tensorflow provides ample documentation and tutorials - one which boasted over 99% accuracy! First I created, trained, and tested a regressional model following the [MNIST for ML Beginners](https://www.tensorflow.org/get_started/mnist/beginners) tutorial. Subsequently, I restored the model and used this to make predictions. This model adapted from the tutorial was not that proficent so I then did the same examination and implementation of the [Deep MNIST for Experts](https://www.tensorflow.org/get_started/mnist/pros) tutorial. The tutorial demonstates a multilayer convolutional model. This rough work can be found in the [rough_work](https://github.com/taraokelly/Emerging-Technologies-Assignment/tree/master/rough_work) directory in the form of jupyter notebooks. To run these, follow the user guide and run the following command in the cmd:

```
jupyter notebook
```

Using this multilayer convolutional model I integrated the implementaion into the Flask application, also giving the application the functionality to build a new model if one does not already exist.

## User Guide

Download and install Anaconda [here](https://anaconda.org/anaconda/python) to download Python 3, and all the nessecary libraries.

Clone this repository.

```
https://github.com/taraokelly/Emerging-Technologies-Assignment.git
```

__To run__:

```
py webapp.py
```


## References

[TensorFlow](https://www.tensorflow.org/)

[MNIST](http://yann.lecun.com/exdb/mnist/)

[Gartner Hype Cycle](https://www.gartner.com/smarterwithgartner/top-trends-in-the-gartner-hype-cycle-for-emerging-technologies-2017/)

[Python](https://www.python.org/)

[Emerging Technology Module Resources](https://emerging-technologies.github.io/)

-----

__*Tara O'Kelly - G00322214@gmit.ie*__