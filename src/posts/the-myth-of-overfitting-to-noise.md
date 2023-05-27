---
title: 'The Myth of "Overfitting to noise"'
date: 2022-11-15 04:25:09
tag: [Data Science]
cover: https://github.com/ethen8181/machine-learning/blob/master/regularization/images/bias_variance.png?raw=true
---
## TL;DR

This post serves as a study note on the topic of "overfitting" in machine learning. It would also help to clarify some common misunderstandings on this topic. Although "overfitting to noise" is common, it's not the root cause of the lack of generalization in overly complex models.

<!-- more -->

## Review: a classic example

In most introductory materials of machine learning, the issue of "overfitting" is illustrated  using something similar to the graph below. Here the data was generated from a smooth function, with some random noises added to it. A polynomial regression model was used to fit the data. When the order of the polynomial was set too high(30 in the figure), the model tried to fit the noise and failed to generalize. Although the error was low on the training data, it can't predict well for new points generated from this curve. Bad.

<img src="https://s2.loli.net/2022/11/16/LQUHKPgRYeXw7Cr.png" alt="overfit_noise.png" style="zoom:67%;" />

Noisy data is everywhere, especially in regression tasks, due to measurement error. For classification tasks, it's possible due to mislabeling and ambiguous samples(Think about an image with both a cat and a dog in it. Its label can be both "cat" and "dog"!).

According to the classic materials, this is why regularization and cross validation are needed.

## This is not the whole story

Ok, so suppose we now have a clean training dataset. We can have each sample carefully checked and we are sure that the labels are correct(Think about benchmark datasets like MNIST). Then we don't need to worry about regularization because there is no noise, right? Actually no. If we train a complex neural network model on it, for many epochs, it is likely to still fail on testing data.

Back to a synthetic regression example. The data was still generated from a smooth function, with no added noise. The graph below shows the fit for a high order polynomial(order is 40) model. Still pretty bad.

<img src="https://s2.loli.net/2022/11/16/zXk2sCcQf4blaKE.png" alt="overfit_wo_noise.png" style="zoom:67%;" />

## Why? A simple explanation

Suppose the model has $m$ parameters and the training data size is $n$. $\mathcal{F}_m$ is the hypothesis space, which means the set of all possible models. In the above example, $\mathcal{F}$ contains all polynomials of the given order($m-1$, to be exact). Denote the parameters for the best solution in the hypothesis space $\theta^\star=\mathrm{argmin}_\theta R(\theta)$, where $R()$ is the risk function(expectation of the loss function). The generalization error on a testing sample can be formulated as follows:
$$
f_{\hat{\theta}}-f^*=(f_{\hat{\theta}}-f_{\theta^*})+(f_{\theta^*}-f^*)
$$
where $f_{\hat\theta}$ is the trained model, $f^\star$ is the ground truth, and $f_{\theta^\star}$ is the best model in $\mathcal{F}_m$.

We call the first part "approximation error". This part is not related to the training set. It only depends on the hypothesis space. Generally, if the hypothesis space is larger, this term gets smaller. For example, if we include higher order polynomials in the hypothesis space, we can get closer to the ground truth using the best possible model.

We call the second part "estimation error". We have this term because we can't get the best possible model in the hypothesis space using finite training samples, even when the data is completely clean. In the example above, there are many potential high order polynomials that can fit (almost) perfectly to the data. Among all these solutions, some are better for generalization, and some are worse. For a large hypothesis space(complex models), there can be many bad solutions, so it's almost sure that the "estimation error" will be large. Here we have "overfitting" again, and regularization can help reduce it.

## It can get complicated

In this [link](https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote12.html), the expected test error under squared loss are separated into bias, variance and noise. The "approximation error" above is bias, and the "estimation error" includes both variance and noise. It's clear from the decomposition that the root cause of overfitting is the variance term.

For modern model structures such as neural networks, it can get more complicated. In this [paper](https://arxiv.org/pdf/2003.01054.pdf), the test error are decomposed to "bias", "noise variance", "initialization variance", and "sampling variance". Roughly speaking, the "variance" part in the above decomposition was again separated according to their causes: "initialization" and "sampling".

Also, from the above research, the generalization error curve may not be the classic U-shaped curve. As the parameter size increases, the test error may decrease again. It's called "Double descent". There might even be "triple descent"s([link](https://proceedings.neurips.cc/paper/2020/hash/1fd09c5f59a8ff35d499c0ee25a1d47e-Abstract.html)).

## Conclusion

Now we have looked briefly into the issue of "overfitting". The classic explanation of "overfitting to noise" is over-simplified. The root cause of "overfitting" can be seen as the lack of ability to choose the best model using finite training data.

This post is heavily based on lecture notes from one of my undergraduate courses.
