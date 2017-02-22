---
layout: post
title: Automating Feature Rescaling with Gaussianisation
categories: ml feature scaling kaggle scikit-learn
---

In this post, I'll discuss [feature scaling] and an idea I had about rescaling features so they are transformed into Gaussian distributions in additon to standardisation.
I'll be doing the Gaussianisation using the [Box-Cox transformation][Box-Cox paper].

But first, some background.


## The need to normalise features

Normalising continuous scaled features is widely considered to be a sensible data preprocessing step.
For features containing boolean values rescaling can be detrimental (because rescaling will destroy the boolean nature of the feature), but with continuous real-valued features rescaling the feature so it is normalised is rarely a bad idea and often very useful.

For some models and training algorithms, the features are assumed to have similar scalings.
For these, normalisation of the features is an essential to ensure the algorithm performs correctly.

- ***k*-means clustering**.
  Since the *k*-means algorithm uses the Euclidean (*L*2) distance from the cluster centre, normalisation is important to ensure it weights each feature equally.

- ***k*-nearest neighbours**.
  For *k*-nearest neighbours, we measure the Euclidean distance of the test sample from each training sample to see which it is most similar to.
  Hence features need to have similar scaling, otherwise a single feature will dominate the distance metric.

- **Gradient descent**.
  When training a model with gradient descent, the algorithm will typically converge faster if the features are scaled similarly.
  Otherwise, if one feature is scaled larger than another, the gradients will be larger for the parameters pertaining to the larger feature and lower for the smaller scaled feature.
  Such differences in the gradient can cause overshooting when updating the larger parameter and/or undershooting for the smaller parameter.
  Gradient descent is commonly used when training linear regression, logistic regression, support vector machine (SVM/SVC), and neural network models.

- **Regularising with *L*1 or *L*2 norm**.
  In order to reduce overfitting, we can use regularisation to try to minimise the *L*1 or *L*2 norm of the parameters whilst optimising the objective function.
  But this constraint only makes sense if we can expect the weights on each feature to be similar sizes when they have similar infuence on the output variable.
  Again, this is found when the features are scaled similarly to one-another.
  Such regularisation is used for Lasso and ElasticNet models, and is often used to for neural networks (also known as weight decay).

- **Principal Component Analysis** (PCA).
  Because PCA picks out the vectors which explain the most variance in the data, it is important that each feature have the same scaling.
  Otherwise the feature with the largest magnitude will trivially provide most of the overall variance.

Conceptually, the argument for rescaling features is clear.
The results of your model shouldn't change if you move from measuring money in dollars to cents.
And so, if the training algorithm is sensitive to such a simplistic rescaling of the feature such that an entirely different model will be produced if trained with a feature measured in cents or dollars, you should normalise beforehand.


## How to normalise features

There are two main [methods][sklearn preprocessing] which are [typically used][sebastianraschka] to normalise features (range scaling and Z-scoring), and a third (robust scaling) which is less common.

### Max-min or range scaling

With max-min scaling, we subtract the minimum value from every sample and divide by the difference between the maximum and minimum.

$$ x'_i = \frac{x_i - \min(x)}{\max(x) - \min(x)} $$

This method is highly influenced by outliers at either end of the distribution of samples.
Such outliers compress the range within which the majority of samples lie.

### Z-scoring (standardisation)

Here, we subtract the mean and divide by the variance.

$$ x'_i = \frac{x_i - \mu_x}{\sigma_x} $$

The feature will now have zero mean and a magnitude on the unit-scale, and if the feature was Gaussian distributed it will now conform to the standard normal distribution.
This method is also susceptible to outliers, since they will increase the measured standard deviation of the distribution.

### Median and quartile range rescaling ([robust scaling])

In this case, we subtract the median and divide by the interquartile range (IQR).

$$ x'_i = \frac{x_i - \operatorname{median}(x)}{\operatorname{IQR}(x)} $$

This method is more robust against outliers --- since the median and interquartile range are defined from percentiles of the data, the exact values at the extremities do not matter.


## The problem which remains

Whichever of these normalisation techniques is employed, the distribution for the data remains unchanged beyond translation and scaling.
So if the shape of the distribution was not suitable for the model we want to construct or the training algorithm we will use, it is still not suitable now.

If the features are all approximately uniform or Gaussian, simply rescaling the feature using one of the methods above will be sufficient for the data to work well with all the algorithms mentioned above.
But if one or more of the features is instead very asymmetric or heavy-tailed, this feature may still be under- or over-weighted across the majority of samples.

For instance, when a feature is known to be log-normally distributed one should take the logarithm of the feature, discarding the orignal and training on its logarithm instead.
This is already regarded as good practice, and helps performance because otherwise the values obtained from a log-normally distributed feature will vary greatly in order of magnitude across our training samples.

Let's consider what would happen to a **log-normally distributed** feature after normalising it with each of the techniques mentioned above.

- Under **max-min** scaling (where the minimum value is set to zero after normalisation), the majority of data points will be almost zero and only a few of the largest samples would be large enough look different to the rest and matter to the algorithm.
- Under **Z-scoring**, the mean and standard deviation are more heavily influenced by the minority of large values.
  Consequently, the majority of values have a decent sized negative value and only a few are positive.
- Under **median and IQR** rescaling, the smaller values constitute the majority of the datapoints, so the median and IQR are defined so these are appropriately rescaled.
  However, larger values from the log-normal distribution will fall outside the expected range and have more impact on their samples.

In addition, irrespective of which of these normalisation methods was applied, the heavy-tail means it is possible for much larger samples to show up in testing or implementation than were seen in the training data.
These unlikely data values could cause the model to make wildly inaccurate predicitons when they do turn up.

All these problems would be accentuated if the feature came from a power-law distribution with high degree, or from a super-exponential distribution, in which case there will be an even longer one-sided tail on the distribution.

Okay, so you could identify log-normally distributed features manually and train on their logarithm instead.
But what if you want to have an automated system without mandating such human intervention?
There might be so many features it is not so practical to inspect each of them and pick whether to use the log-transform.
Furthermore, some features might have an intermediate scaling best handled by something in-between linear and logarithmic transformation
Or a super-exponential distribution where taking the logarithm is not adequate.

Well, one option to resolve this is to automatically Gaussian-ise the features.


## The solution: Gaussianisation

To prevent asymetric and long-tailed distributions from hindering our performance, we can transform them so they are more Gaussian-like.

How do we do this? We can use a power transformation!

More specifically, the [Box-Cox power transformation][power transformation], which is given by

$$
x'_i =
\begin{cases}
\dfrac{(x_i + \lambda_2)^{\lambda_1} - 1}{\lambda_1} & \text{if } \lambda_1 \neq 0, \\[6pt]
\ln{(x_i + \lambda_2)} & \text{if } \lambda_1 = 0,
\end{cases}
$$

where \\( \lambda_1 \\) and \\( \lambda_2 \\) are free parameters which we fit in order to the distribution of \\( x \\) in order to make the output distribution as Gaussian-like as possible.

As mentioned before, translation and rescaling don't change the shape of a distribution, so the subtraction of 1 and division by \\( \lambda_1 \\) does not impact the Gaussianity of the output distribution.

However, since we have

$$
\lim_{\lambda_1 \to 0} \dfrac{(x + \lambda_2)^{\lambda_1} - 1}{\lambda_1} = \ln x
$$

this choice offers us continuity in the functions produced as we vary \\( \lambda_1 \\). 

It only makes sense to apply the Box-Cox transformation when the input feature is strictly positive, since we are taking roots if \\( \lambda_1 < 0\\), and our transformation would not be monotonic if \\( \lambda_1 > 0 \\) if we don't have \\( x \\) strictly positive.

To ensure \\( x \\) is positive, we can offset the data with \\( \lambda_2 = \max(0, -\min(x)) \\).

We then search over a range of potential \\( \lambda_1 \\) values and choose the one which either maximises the log-likelihood of the Box-Cox likelihood function or maximises the Pearson correlation-coefficient between the output and a normal distribution.
Or, instead of choosing a finite set of \\( \lambda_1 \\) values to test, we can use an optimiser ([bisection](https://en.wikipedia.org/wiki/Bisection_method), [linear interpolation](https://en.wikipedia.org/wiki/Secant_method), [Brent's method](https://en.wikipedia.org/wiki/Brent's_method)) to maximise our objective function.
If desired, we can optimise \\( \lambda_2 \\) as well.

After performing Gaussianisation with the Box-Cox transformation, as an additional step we can take a Z-score.
This will shift our new distribution to have zero mean and unitary variance, accomplishing rescaling after redistributing.


## Further implications

Applying power transformations in this manner to the raw features will certainly change the model which you construct.

As stated before, the results of your model shouldn't change if you move from measuring money in dollars to cents.
But after Gaussianising the same feature with the Box-Cox transformation, we've moved to measuring money in some non-linearly transformed space instead.
This transformed space is still for building a model an though.
In fact, it provides a representation similar to the percentile of monentary amount taken over all the samples we have for that feature.

Furthermore, taking a power transformation of an existing feature is one way for a data scientist to perform feature engineering and attempt to find a more accurate model of the data.
Here, we're doing the same thing but taking the human out of the routine and automating the choice of the power with which to transform the feature.

If we're fitting a linear model and have no reason to suspect that there is linear relationship between a financial feature measured in dollars and the class or regression target, why not take the Box-Cox transformation of the feature?
Without any other information, this is no less likely to be linearly related to the target variable.
The Box-Cox transformation is essentially giving us a measure of relative purchasing power instead of actual cash, which is not necessarily a bad thing.

Furthermore, if you're doing regression you can rescale the target variable using Box-Cox too (and undo the transformation after generating predictions so the overall model gives a salient output).

Should Gaussianisation be performed before PCA, this will change the co-linearity of the features and the eigenvectors produced.
But if the motivation for PCA is dimensionality reduction before fitting a predictive model to the data, this is not an issue.


## When to Gaussianise features

Honestly, I think most of the time Gaussianisation isn't necessary.
But it does add another pre-processing tool to your arsenal.

Applying a power transformation certainly won't help if your feature is multimodal.
If your features are sparse, or approximately uniformly or Gaussian distributed, there is no benefit to Gaussianising them.

But if your feature varies is far from Gaussian, Gaussianising may very well help you construct a more accurate model.

From our earlier list of algorithms motivating feature scaling, I suspect that *k*-means and *k*-nearest neighbours are most likely to benefit from Gaussianisation of non-sparse features.

Whilst it may help gradient descent to converge faster and weight the effect of regularisation more evenly, consideration must be given to the performance of the resulting model, which is more important than the convergence time.
I suspect that features post---Box-Cox transformation will carry no less predictive power than the raw features, particularly if the regression target is also Gaussianised (as stated above).
However, I've not yet done enough experimentation to know how true this is.

Stay tuned for some follow-up experiments!


[Box-Cox paper]: https://www.jstor.org/stable/2984418
[feature scaling]: https://en.wikipedia.org/wiki/Feature_scaling
[sklearn preprocessing]: http://scikit-learn.org/stable/modules/preprocessing.html
[sebastianraschka]: http://sebastianraschka.com/Articles/2014_about_feature_scaling.html
[robust scaling]: http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.RobustScaler.html#sklearn.preprocessing.RobustScaler
[power transformation]: https://en.wikipedia.org/wiki/Power_transform#Box.E2.80.93Cox_transformation
[isixsigma]: https://www.isixsigma.com/tools-templates/normality/making-data-normal-using-box-cox-power-transformation
[stats handbook]: http://www.itl.nist.gov/div898/handbook/eda/section3/boxcoxno.htm
[scipy boxcox]: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.boxcox.html
[probability plot]: https://en.wikipedia.org/wiki/Q%E2%80%93Q_plot
[dataset]: https://archive.ics.uci.edu/ml/datasets/Forest+Fires

