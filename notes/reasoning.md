# Notes (Reasoning followed during these months)

## Dataset theme

Dataset focused on SW metrics and buggy outcome

Key metrics:

- Lines of code
- Cyclomatic complexity, quantitative metric of the number of linearly independent paths through a program source code
- Lenght, Volume, Difficulty (Halstead complexity metrics)
- Fan In, Fan Out -> Module dependencies in input and output
- Num operators, num operands -> Info related to symbols used in code
- Branch count -> conditional logic and related branches
- Defect -> 1 stands for buggy, 0 for sane

## Steps

0. **Imports**: Import from libraries and env variables
1. **Data loading**: Load data with Polars
2. **Data exploration**: Basic exploration of the dataset, along with target column analysis, distribution of the features, imbalance ratio (ca 2, so slightly imbalanced). First assumptions on characteristics of defective code
3. **Data Visualization**: Plotting of correlation and other metrics, VIF (Variation Inflation Factor)
4. **Prediction on original dataset**: Set up of basic binary classification models and performance metrics evaluation
5. **Feature engineering**: using domain knowledge, calculate deriving metrics in order to improve overall performance of the models
6. **Model comparison**: compare metrics and find out which model is the best one

## Observations

### VIF

sklearn does not provide utilities or methods to calculate this metrics automatically, so I had to manually compute regression against each single feature

In order to do so, for each feature, I had to take it out of the input df, erase it from it (np.delete return a new array instance, so all references are okay), apply linear regression to df without target column and this last one.

From here, score returns R2 (practically, it fits data and analyze residuals in order to return R2) and finally, I can apply VIF formula to obtain the goal value

### PCA

Principal Component Analysis (PCA) is frequently used as a remedy for multicollinearity by transforming correlated variables into uncorrelated principal components.
Analyzing the outcome obtained from VIF calculation, I can tell that, having features that are already uncorrelated, this step is not necessary

### Feature engineering

[Reference for metrics](https://www.geeksforgeeks.org/software-engineering/software-engineering-halsteads-software-metrics/)

From Halstead metrics and other information available in raw dataset, I could compute

- Cyclo per LOC: Complexity density
- Operator ratio: operators/operands
- Code density: volume/length -> info per token, heavy code should be more error prone
- Control complexity: branch count x cyclomatic complexity -> many branches along with complexity, perfect receipe for production bugs
- Coupling, fan in + fan out: high coupled modules are more difficult to test, so they represent single points of failure
- Program effort (volume x difficulty): Measures the amount of mental activity needed to translate the existing algorithm into implementation in the specified program language
- Intelligence content (volume / difficulty): This parameter provides a measurement of program complexity, independently of the programming language in which it was implemented

### Hyperparameters tuning

During the experiments I tried the following scoring parameters:

- 'roc_auc': Best used when comparing models across different thresholds or ranking performance
- 'f1': Need a single metric balancing precision and recall

Outcome: switched back to roc_auc, better results

## Models Evaluation

[Reference](https://towardsdatascience.com/performance-metrics-for-binary-classifier-in-simple-words-be958535db49/)

**Accuracy Score**

TP = True Positives
TN = True Negatives
FP = False Positives
FN = False Negatives

Accuracy = TP + TN / (TP + TN + FP + FN)

It is unsuited when data is imbalanced and there are significantly more type 0 data than type 1 (or vice versa)
Consequently, in our case, this couldn't be the best metric to use for evaluation

**Recall (True Positive Rate)**

Recall = TP / (TP + FN)

**Specificity (True Negative Rate)**

Specificity = TN / (TN + FP)

**Precision**

Precision = TP / (TP + FP)

**F1 Score**

F1 = 2 x (Precision x Recall) / (Precision + Recall)

F1 is the harmonic mean of Precision and Recall, so you can’t get a high F1 if either one is very low. Unlike Balanced Accuracy, the F1 doesn’t take into account True Negatives - it’s easy to see if we expand the formula.
F1 only cares about the samples the model said are positive, and about the samples that actually are positive and doesn’t care at all about how many negative samples we have in dataset or how many were classified correctly.
That’s why this metric is quite popular when evaluating models aimed at finding anomalies.
