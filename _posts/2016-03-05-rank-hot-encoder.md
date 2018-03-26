---
layout: post
title: Rank-Hot Encoder for Ordinal Features
categories: ml kaggle scikit-learn
---

In the past, whenever I'm working with a dataset which contains ordinal features, I've never known what to do with them.
But now, I think I've come up with a good solution, which is the *rank-hot encoder*.


## Background

### Continuous data

If you're working with continuous valued fields with a ratio or interval scale, the relative value or difference in values has true meaning.

Let's say you're predicting the income of an individual given a set of descriptors about them.
Consider a variable like the number of hours they work each week.
Intuitively, if we hold everything constant but double their hours, we would expect their salary to approximately double (the effect is potentially non-linear due to non-linearities in the rate of income tax).

Since we can see an approximately linear relationship between the two, it might be a good idea to use a linear regression model.
But irrespective of which model we chose to use, doubling the number of work hours is a concept which makes sense, no matter how many hours were being worked initially.


### Categorical data

With categorical or nominal data, such as area of occupation, we have a discrete set of possible textual values.
The values have no sense of ordering to them.

| Occupation        |
|-------------------|
| Tech-support      |
| Sales             |
| Exec-managerial   |
| Machine-op-inspct |
| Adm-clerical      |
| ...               |

For the sake of passing arguments to our model, we can make a dictionary of the labels and encode them as integer indices into this dictionary.

| Occupation        | Dictionary Index    |
|-------------------|---------------------|
| Tech-support      | 0                   |
| Sales             | 1                   |
| Exec-managerial   | 2                   |
| Machine-op-inspct | 3                   |
| Adm-clerical      | 4                   |
| ...               |                     |

Here, it doesn't make sense to consider what happens if we double the value in the field --- `Exec-managerial` isn't "twice as occupation" as `Sales`.

Not only that, but there is no intrinsic ordering to the occupational roles.
Each occupation is a different property that the individual can have, it just so happens that they can only have one occupation at a time.

Consequently, we typically use a one-hot encoding of categorical features to input this data to the model.
In a one-hot encoding, we create new binary fields, one for each occupation, and the value in each tells us whether the individual has that occupation.
Since the occupations are mutually exclusive, exactly one of the new fields will be `1` (i.e. *hot*), and the rest `0`.

| Occupation        | Dictionary Index    | One-Hot Encoding       |
|-------------------|---------------------|------------------------|
| Tech-support      | 0                   | `[1, 0, 0, 0, 0, ...]` |
| Sales             | 1                   | `[0, 1, 0, 0, 0, ...]` |
| Exec-managerial   | 2                   | `[0, 0, 1, 0, 0, ...]` |
| Machine-op-inspct | 3                   | `[0, 0, 0, 1, 0, ...]` |
| Adm-clerical      | 4                   | `[0, 0, 0, 0, 1, ...]` |
| ...               |                     |                        |

Here, each field answers the query "**Is the occupation *x*?**".
It lets us build models with the correct assumptions about the data.
If we're training a linear regression model, we don't want it to assume that the dependent variable can vary linearly with the dictionary index encoding of the occupation!
By combining this feature with other features (such as number of hours worked) of the individuals in our dataset, we could build a linear model of the data where each occupation gives us a different scaling factor applied onto a generic occupation-free model.


### Ordinal data

A typical example of an ordinal data feature is a rating system, such as customer satisfaction.

| Satisfaction |
|--------------|
| Very bad     |
| Bad          |
| Neutral      |
| Good         |
| Very good    |

As I'm sure you'll agree, the values are ranked with *Very bad < Bad < Neutral < Good < Very good*.
But we don't have a continous scale for this variable, and customer satisfaction does not change in a linearly fashion as we progress through the scale.

Furthermore, ordinal scales can be arbitrarily non-linear.
The non-linearity of the customer satisfaction scale may not be immediately apparent, so allow me to elaborate with a slightly contrived example.
Age, which would have been continuous if it had been left unchanged, has been bracketed into bins of very different widths.

| Age Group |
|-----------|
|  0 -- 16  |
| 17 -- 18  |
| 19 -- 21  |
| 22 -- 60  |
| 61 -- 65  |
| 66+       |

Knowing which bracket the individual's age falls into will still be useful to useful to us when estimating their income, but the feature is clearly no longer continuously scaled.
As we progress through the categories in order, there is no constant rate of change in age.

As we discussed for the categorical data type, we can consider the results of an dictionary encoding and a one-hot encoding of such an ordinal feature.
However, now we have to be careful to make sure the dictionary label mapping is ordered correctly so that we have a rank index which ascends monotonically with the ranking in the ordinal scale.

| Satisfaction | Rank Index | One-Hot Encoding  |
|--------------|------------|-------------------|
| Very bad     | 0          | `[1, 0, 0, 0, 0]` |
| Bad          | 1          | `[0, 1, 0, 0, 0]` |
| Neutral      | 2          | `[0, 0, 1, 0, 0]` |
| Good         | 3          | `[0, 0, 0, 1, 0]` |
| Very good    | 4          | `[0, 0, 0, 0, 1]` |

Again we can either train on the rank index, or the one-hot encoding of the ordinal variable.
Each option offers different advantages and problems.

If we want to train a decision tree or random forest model, we can use the rank index with no downside.
This is because decision trees and forests of trees assume that the data they work with has the property of ordinality, but do not need to assume it possesses multiplicativity or additivity.
Decision trees make predictions using a series of decisions, each of which involves comparing the value of a single feature with a threshold (the threshold is optimised with training).
Whether the difference between the value and the threshold is large or small does not matter to the decision tree.
Consequently, it does not matter that the rank index for the ordinal feature does not scale linearly.

But, as with categorical features, we don't particularly want to train a linear model on the rank index directly.
This is because the model assumes our features scale linearly, with both multiplicativity and additivity as possible operations, but the rank index of an ordinal feature doesn't scale linearly.
However it is also not ideal to train a linear model on the one-hot encoding, since this removes the ranking structure present in the data.
We need a way to convey the structure of the data to the model without it making false assumptions.

I investigated standard practices on how to handle ordinal variables, and the advice I found instructed to train simply chose to train the model using either the rank index and or using the one-hot encoding, with the decision left to the data scientist.
In practice, which method works best depends on the feature and its relationship with the output variable --- if the relationship is approximately linear or highly non-linear.
Lacking a principled method to pick between the two representations, it is sometimes recommended to train two models, one with a rank index and the other with a one-hot encoding, and pick whichever performs best.

However, this didn't seem like a very satisfactory solution to me.
Surely there is a way to tell a linear model about the ordinality without making the false assumption that the field scales in a continuous manner?
Then we could have the best of both representations.

Enter, the *rank-hot encoder*.


## Rank-Hot Encoder

The rank-hot encoder is similar to a one-hot encoder, except every feature up to and including the current rank is hot.

| Satisfaction | Rank Index | One-Hot Encoding  | Rank-Hot Encoding |
|--------------|------------|-------------------|-------------------|
| Very bad     | 0          | `[1, 0, 0, 0, 0]` | `[0, 0, 0, 0]`    |
| Bad          | 1          | `[0, 1, 0, 0, 0]` | `[1, 0, 0, 0]`    |
| Neutral      | 2          | `[0, 0, 1, 0, 0]` | `[1, 1, 0, 0]`    |
| Good         | 3          | `[0, 0, 0, 1, 0]` | `[1, 1, 1, 0]`    |
| Very good    | 4          | `[0, 0, 0, 0, 1]` | `[1, 1, 1, 1]`    |

Instead of answering the query "**Is the satisfaction *x*?**", the entires in a rank-hot encoder tell us "**Is the satisfaction level at least *x*?**".
This representation of the data allows a linear model to explain the effect of a high-rank as the additive composition of the effect of each rank in turn.

It's a bit like an onion.
We start with a model for "very bad" satisfaction.
Then, when the satisfaction is higher than "very bad", we add an effect from this to the model for "very bad".
If the satisfaction is higher than "bad", we add another effect which accounts for this.
And so on, until we have an effect which accounts for the difference between "good" and "very good" satisfaction.

Training a model on such a representation of the data has the potential to out-perform either of the other encodings.

Possibly one of the biggest advantages of the rank-hot encoder over the one-hot encoder is the regularising effect created when the sparsity of the features is reduced.
With a one-hot encoder, only a small fraction of the samples will match a single rank, so nearly all the samples inform us about the effect of the `0` value and a minority about the `1` value.
Whereas with the rank-hot encoder, the `0` and `1` values are more evenly distributed.
For the middle ranks, typically around half the samples will be below and half above the threshold.


## Future work

I intend to take the rank-hot encoder for a test drive and see whether and in what scenarios it out-performs rank index and one-hot encoding of ordinal variables.

When I do, I'll be back to this post with an update on how successful it was.

