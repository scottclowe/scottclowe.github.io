---
layout: post
title: Stratified Validation Splits for Regression Problems
categories: ml kaggle scikit-learn regression
---


In this post, I'll describe a technique for doing stratified partitions of datasets when your goal is regression instead of classification.


## Setting the scene

Let's say you're training a model on a dataset and you need to split it into **train** and **test** partitions.

You're doing this so your training algorithm will learn a model based on some of the samples (the training set) and then evaluate how good it is on other samples (the [test set]) which were unseen during training.
It's important that you test on unseen samples so that you know your algorithm generalises well --- otherwise it could cheat by writing down the answers while your training it, which is effectively what happens if it [overfits][overfitting].

Additionally, you can split your data down further into three sets: train, **validation**, and test.
Now you can train lots of different models on the training set and then work out which is best by seeing how the perform on the validation set.
After picking out the best model, you can see how well it generalises by inspecting its performance on the test set.

Why not cut out this step and just compare the models on the test set and report this as the final performance?
Well when you test your model you don't find out the true, underlying performance of it but the performance on a certain number of samples.
And the finite sampling leads to variability in the result.
There's a chance that your model performance appears high during testing because it happens to do well on these samples even though it doesn't generalise so well overall.
As you increase the number of models which are trained, the chance that one of them has a high performance purely at random increases.
Although none of the models were trained on the validation set, by using the validation set to choose our model we can overfit to the validation set.
Consequently, we should evaluate on the test set alone only at the end of selecting our model and training it.

You can also do \\( k \\)-fold [cross-validation], where the training set is partitioned into \\( k \\) equally sized sets.
We then train \\( k \\) models on (\\( k \\)-1) of the partitions and evaluate its perfomance on the remaining partition.
The overall perfomance from these \\( k \\) repetitions can then be used to compare our models and pick the best one.
Having \\( k \\) folds instead of 1 increases makes the model validation score more reliable, since it is based on more data.

But each time you partition the data, how do you pick out which samples should be in each subset?

The simplest method is **random** partitioning.
Let's say you want the training, validating and testing partitions to have an 80/10/10% split.
With random splits, samples are randomly ordered and then allocated to one of these partitions.

A smarter method method is **stratified** partitioning.
This method is typically applied for single-label classification problems, where each sample belongs to one of *C* classes and we want to a model which applies the correct label to each sample.
For stratified partitioning, the distribution of samples across the classes are held constant for each partition.
So if 30% of all samples have label 0, 60% label 1, and 10% label 2, each partition will have this proportion of samples within its members.

Studies have shown that stratified cross-validation gives a more reliable (lower bias and variance) estimate of model performance ([Kohavi, 1995]), and it is common practice to use 10-fold stratified cross-validation to evaluate the perfomance of models on classification tasks.
Using stratification during model selection produces better results because the validation set(s) more accurately represent the task we need to solve.
If one class is hard to predict, we won't have more of them (artificially hindering the performance metric) or less (assisting performance) if we use stratification.

But what if you're not doing classification? What if you're doing **regression** instead?

In a regression task, we are trying to predict a scalar value (annual income, say) instead of a class label ("chair", say).
Usually for regression problems, random partitioning is used.
Since we don't have class labels, we can't do stratification in the same way as we do for a classification task.

Or can we?

Here, I'll present a new option to consider.


## Sorted stratification

Let \\( N \\) denote the number of samples, \\( y \\) the target variable for the samples, and \\( k \\) the number of equally sized partitions we wish to create.

With sorted stratification, we first sort the samples based on their target variable, \\( y \\).
Then we step through each consecutive \\( k \\) samples in this order and randomly allocate exactly one of them to one of the partitions.
We continue this \\( \operatorname{floor}(N / k) \\) times, and the remaining \\( \operatorname{mod}(N, k) \\) samples are randomly allocated to one of the \\( k \\) partitions.

This algorithm ensures the distribution over \\( y \\) is the same in each of the \\( k \\) partitions as it is for the \\( N \\) samples overall.

As an improvement, we can choose the \\( \operatorname{mod}(N, k) \\) "left-over" samples to remove from \\( N \\) before running this partitioning algorithm.
We can either select these at random, or at regular intervals of \\( N \cdot \operatorname{mod}(N, k) / (\operatorname{mod}(N, k) + 1) \\), dividing up the distribution evenly.

The number of possible partitions is \\( (k!)^{\operatorname{mod}(N, k)} \\), which is still very large.

*Sorted stratification* works well for \\( k \\)-fold cross-validation, where we need to create \\( k \\) equally sized partitions of the data.
But it is a little more difficult to generalise to unequal partitions.

A 90/10% split can be achieved easily by choosing \\( k = 10 \\) and grouping 9 of the partitions together.
Whereas an 89/11% split would require us to use \\( k = 100 \\) since the greatest common factor in 89 and 11 is 1.
As the precision of the split rises, the value of \\( k \\) needed to generate that split also rises.

Since the reproduction of the distribution shape decreases as \\( k / N \\) increases, there is a trade-off in the quality of the distribution replication and the precision of the split.
Instead, for arbitrary partition sizes we can use fractional stratification.


## Fractional stratification

Suppose we want to create \\( P \\) partitions, \\( \pi_i \\) for \\( i = 1, \ldots, P \\), each of which should contain some proportion \\( s_i > 0\\) of the samples, where \\( \sum_i s_i = 1 \\).

For fractional stratification, we first choose the precision at which we want to reproduce the distribution of \\( y \\).
Let \\( q \\) denote the chosen precision.

We sort the samples based on \\( y \\) and allocate each consecutive block of \\( N / q \\) samples into temporary partitions, \\( \Omega_j \\) for \\( j = 1, \ldots, q \\).

Now we consider the temporary partitions in turn.
Let \\( Q_j \\) denote the number of samples in the temporary partition \\( \Omega_j \\).
For each of the \\( P \\) output partitions, \\( \pi_i \\), we assign \\( \operatorname{floor}(s_i \, Q_j) \\) samples at random from without replacement.
After this, we have some \\( R_j = Q_j - \sum_i( \operatorname{floor}(s_i \, Q_j) ) \\) unallocated samples.

After repeating this for each partition, we can collate the \\( R = \sum_j R_j\\) remaining samples.
We can recursively apply this algorithm to the remaining \\( R \\) samples, adding more samples to the same partitions \\( \pi_i \\).
The extraction fraction must be updated to \\( s^{(1)}_i = ( s_i \, N - |\pi_i| ) / R \\) to ensure the total number of samples is correct.
The precision must also be reduced, to \\( q^{(1)} = \operatorname{floor}(q / 2) \\) say, to ensure the algorithm terminates.

If we ever allocate all \\( R^{(l)} \\) samples to partitions, the algorithm terminates.
Otherwise, after \\( L = \operatorname{floor}(\log_2(q)) \\) recursions we reach the minimum precision of \\( q^{(L)} = 1 \\).
At this point, we randomly allocate each of the remaining \\( R^{(L)} \\) samples to the partitions \\( \pi_i \\) with probabilities \\( s_i^{(L)} \\) respectively.


## Discussion

The advantage of using either sorted or fractional stratification over random partitioning is that the distribution of target values is assured to be approximately the same across all the partitions.
This is useful to make sure validation and test performance gives depicts the expected performance of the model with less bias and variance.

Typical performance metrics for regression are *mean squared error* and *mean absolute error*.
With either metric, the error contributed from an individual sample typically rises as its target value rises, because a fixed percentage error will give a larger absolute difference for larger target values.
Consequenly, poor distribution consistency will increase the variance in the result --- under or over representation of the targets with larger magnitudes will respectively result in an decrease or increase in the measuered loss.

Such an effect is more prominent for distributions which are heavy-tailed.
With these, the total loss is more likely to be dominated by a minority of the samples.

If your distribution is heavy-tailed, another solution to this problem is to transform the distribution of targets with [Gaussianisation][gaussianisation blog post].
You can perform the Gaussianisation step with a Box-Cox transformation ([as described here][gaussianisation blog post]) to your \\( y \\) values before training and evalutating the model.
Afterwards, when you're making predictions on samples in the wild using your model, make sure you remember to apply the inverse transformation to the outputs.

However, Gaussianisation isn't always suitable for your problem.
When or not you need to evaluate the loss of a regression problem with a heavy-tailed distribution, stratified partitioning using sorted or fracitional stratification will always work.


[test set]: https://en.wikipedia.org/wiki/Test_set
[overfitting]: https://en.wikipedia.org/wiki/Overfitting
[cross-validation]: https://en.wikipedia.org/wiki/Cross-validation_(statistics)
[Kohavi, 1995]: http://web.cs.iastate.edu/~jtian/cs573/Papers/Kohavi-IJCAI-95.pdf
[Forman and Scholz, 2010]: http://www.kdd.org/exploration_files/v12-1-p49-forman-sigkdd.pdf
[gaussianisation blog post]: /2016-03-12-boxcox-feature-gaussianisation

