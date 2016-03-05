---
layout: post
title: Rank-Hot Encoder for Ordinal Features
categories: ml kaggle scikit-learn
---

Whenever I'm working with a dataset and it contains ordinal features, I never know what to do with them.


## Background

### Continuous data

If you're working with continuous valued fields with a ratio or interval scale, the relative value or difference in values has true meaning.

Let's say you're predicting the income of an individual given a set of descriptors about them.
Consider a variable like the number of hours they work each week.
Intuitively, if we hold everything constant but double their hours, we would expect their salary to approximately double (the effect is potentially non-linear due to non-linearities in the rate of income tax).

Since we can see an approximately linear relationship between the two, it might be a good idea to use a linear regression model.
But whichever model we use, doubling the number of work hours is a concept which makes sense, irrespective of how many hours were being worked initially.


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

Consequently, we typically use a one-hot encoding of categorical features.
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

Here, each field answers the query **Is the occupation *x*?**
It lets us build models with the correct assumptions about the data.
If we're training a linear regression model, we don't want it to assume that the dependent variable can vary linearly with the dictionary encoding of the occupation!
Instead, maybe there is an generic distribution of income versus the other variables (including hours worked), which is the same across all professions, and knowing the occupation gives us an additional scaling factor with which we can modulate the curve.


### Ordinal data

When we consider ordinal data, the typical example is a rating system, such as customer satisfaction.

| Satisfaction |
|--------------|
| Very bad     |
| Bad          |
| Neutral      |
| Good         |
| Very good    |

As I'm sure you'll agree, the values are ranked with *Very bad < Bad < Neutral < Good < Very good*.
But we don't have a continous scale for this variable and how satisfied the customer is does not change linearly as we progress through the scale.

Ordinal scales can be arbitrarily non-linear.
A slightly contrived example is shown below.
Age, which would have been continuous if it had been left unchanged, has been bracketed into bins of very different widths.
Consequently there clearly is not a constant rate of change in age as we move through these categories.

| Age Group |
|-----------|
|  0 -- 18  |
| 19 -- 21  |
| 22 -- 30  |
| 31 -- 60  |
| 61 -- 65  |
| 66+       |

As before, we can consider the results of an dictionary encoding and a one-hot encoding of such a field.
However, now we have to be careful to make sure the dictionary label mapping is ordered correctly so that we have a rank index which ascends monotonically with the ranking in the ordinal scale.

| Satisfaction | Rank Index | One-Hot Encoding  |
|--------------|------------|-------------------|
| Very bad     | 0          | `[1, 0, 0, 0, 0]` |
| Bad          | 1          | `[0, 1, 0, 0, 0]` |
| Neutral      | 2          | `[0, 0, 1, 0, 0]` |
| Good         | 3          | `[0, 0, 0, 1, 0]` |
| Very good    | 4          | `[0, 0, 0, 0, 1]` |

If we want to train a decision tree or random forest model, using the rank index would have no disadvantage.
This is because decision trees make their decisions by comparing the value of the feature with a threshold, and how much change their is between the thresholds is unimportant.
Their intrinsic assumption is of ordinality without multiplicitivity or additivity.

On the other hand, if we're training a linear model on this data we don't particularly want to give it the rank index directly because it doesn't scale linearly.
We're in a similar situation as we were with the categorical variables.

But it is also not ideal to train on the one-hot encoding, since this forgets the ranking structure present in the data.

My research on what to in order to handle ordinal variables said to either train on the rank index or its one-hot encoding.
Which one works best depends on the feature and its relationship with the output variable.
If there is no intuitive way to pick which is more appropriate, I've seen it recommended to simply try the model each way round (training on rank index and alternatively training on one-hot encoding) to see which performs best.

However, this didn't seem very satisfactory to me.
Surely there is a way to tell a linear model about the ordinality without making the false assumption that the field scales in a continuous manner?

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

Instead of answering the query **Is the satisfaction *x*?**, the fields of a rank-hot encoder tell us **Is the satisfaction level at least *x*?**
The new features inspect whether the rank meets or exceeds a thresholds, using the similar to the behaviour of a decision tree.

This set-up allows a linear model to explain the effect of a high rank as the additive composition of the effect of each rank in turn.
If such a model works well, this should out-perform either of the other encodings.

I suspect that one of the biggest advantages of the rank-hot encoder over the one-hot encoder is the regularising effect of reducing the sparsity of the features.
With a one-hot encoder, only a small fraction of the samples will match a single rank, so nearly all the samples inform us about the effect of the `0` value and a minority about the `1` value.
Whereas with the rank-hot encoder, the `0` and `1` values are more evenly distributed.
For the middle ranks, typically around half the samples will be below and half above the threshold.


## Future work

I intend to take the rank-hot encoder for a test drive and see when it out-performs rank index and one-hot encoding of ordinal variables.

When I do, I'll be back to this post with an update on how successful it was.

