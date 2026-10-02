# Machine Learning

> Guoliang | AI Field Guides

[EN](AI-ML.en.md) · [中文](AI-ML.zh.md)

Build intuition for learning from tabular data through eight original stories, transparent calculations, and primary-source reading. Each chapter connects a modeling decision to the evidence needed to justify it.

## A route through the ideas

Problem framing, leakage, regression, optimization, classification, evaluation, trees, unsupervised learning, and generalization. All stories and numerical datasets are original synthetic teaching examples.

### Before you start

- Read a table and distinguish rows from columns.
- Work with averages, squares, fractions, and simple algebra.
- Recognize a vector as an ordered list; derivative intuition is helpful but introduced here.

### What you will learn

- Define a prediction task and prevent information leakage.
- Calculate losses, gradient updates, classification metrics, and simple model decisions.
- Explain what trees, clustering, and PCA learn and what they cannot establish.
- Choose validation and regularization that match the intended deployment setting.

## Knowledge framework

### Ask and measure

- [Define the question before dividing the data](#framing-splits-leakage)
- [Fit a line and account for every error](#linear-regression-mse)

### Learn and decide

- [Learn with controlled steps and comparable scales](#gradient-descent-scaling)
- [Separate probability estimates from decisions](#logistic-thresholds)
- [Count the mistakes that the task actually cares about](#metrics-imbalance)

### Find structure and test it

- [Build rules, then understand what combining them changes](#trees-ensembles)
- [Find structure without inventing labels](#clustering-pca)
- [Validate choices and prepare for a changing setting](#validation-regularization-shift)

<a id="framing-splits-leakage"></a>

## Define the question before dividing the data

### 01 / The story

Mira wants a small field logger to warn when a sensor will fail during its next recording session. Her first table contains many sessions from the same twelve devices, plus a maintenance note written after each failure. A random row split produces an exciting score. Then a newly borrowed device performs badly, and Mira notices that the maintenance note practically reveals the answer. She rewrites the task: predict a future failure using only information available before a session begins. She removes the note and reserves complete devices for validation and testing because her intended use involves unfamiliar hardware. The score falls, but the remaining mistakes now describe a real challenge. Her notebook begins with the prediction time, the target, and the unit being held out. These decisions become part of the model, not preliminary paperwork.

### 02 / The concept

A supervised learning problem specifies an input, a target, and the moment when a prediction must be made. Training data fit parameters; validation data guide choices; test data estimate performance after those choices are fixed. Leakage occurs when the learning process gains information unavailable in the intended prediction setting. It includes future measurements, shared identities across an inappropriate split, and preprocessing fitted on held-out data. The split should represent the question: new devices require group separation, whereas future sessions on existing devices may require chronological separation.

### 03 / Put the concept to work

Write one sentence naming the prediction unit, target horizon, and available features. Draw the route from raw records to the final score. Split before fitting imputation, scaling, or feature selection, and fit those steps within each training fold. Check duplicate records and shared entities. Keep a simple baseline and record the split rule so that later model comparisons answer the same question.

### 04 / How others use it

The linked Google dataset-splitting tutorial explains the distinct roles of training, validation, and test data. The linked scikit-learn common-pitfalls guide demonstrates how preprocessing can leak information and uses pipelines to keep transformations with an estimator. Apply those documented workflows to an original sensor table: inspect feature timestamps, hold out the appropriate units, and verify that every learned transformation sees training rows only.

### 05 / The formula, unpacked

```text
D = D_train ⊔ D_val ⊔ D_test
R_test = (1 / n_test) Σ_{i=1}^{n_test} I[f(xᵢ) ≠ yᵢ]
```

D denotes the complete dataset; D_train, D_val, and D_test are its training, validation, and test subsets. The symbol ⊔ means a disjoint union of records, with any required group or time separation enforced as well. n_test is the number of test examples. The index i selects one test example, xᵢ is its available input, and yᵢ is its true class. f is the fixed trained classifier. I is an indicator that equals one for an incorrect prediction and zero otherwise. Σ adds these errors, and R_test is their average.

### 06 / Work through the numbers

Construct 120 records from twelve devices, with ten sessions per device. Assign eight entire devices to training, two to validation, and two to testing. The resulting counts are 80, 20, and 20, and their sum is 120. Suppose the fixed classifier gets eighteen of the twenty test records right. There are two errors, so R_test = 2 / 20 = 0.10, or a 10% error rate. A separate, deliberately inappropriate row split might show nineteen correct predictions out of twenty, giving 5% error. That smaller number estimates a different, contaminated comparison if device identity carries information. Neither result proves performance on all future hardware. The two held-out devices, rather than twenty independent devices, also limit how much confidence this tiny demonstration deserves.

**Where the analogy stops:** Disjoint rows do not guarantee independent evidence. Related people, locations, recordings, or devices can cross a split without literal duplicates. A clean test set can still differ from future data. Small group counts make uncertainty especially large, and repeatedly selecting models using test results turns the test set into another validation set.

**Keep this idea:** A score becomes meaningful only after you specify what is predicted, when information becomes available, and what kind of unseen case the split represents.

### Sources for this topic

- [Google: Datasets: Dividing the original dataset](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets)

- [scikit-learn: Common pitfalls and recommended practices](https://scikit-learn.org/stable/common_pitfalls.html)

<a id="linear-regression-mse"></a>

## Fit a line and account for every error

### 01 / The story

Jun records the height of seedlings beside a window and wants to estimate tomorrow's height from elapsed growing time. He draws a line through a scatterplot, but two plausible lines look equally convincing by eye. One follows most points closely and misses a tall seedling; the other moves toward that seedling and misses several ordinary ones. Instead of choosing the prettier line, Jun writes down every prediction and its difference from the measured height. Squaring and averaging those differences gives him an explicit rule for comparison. He also notices that the score is in squared centimeters, so he reports its square root alongside it. The exercise does not establish that time alone causes growth. It gives him a transparent baseline, a visible error pattern, and a reason to collect light measurements next.

### 02 / The concept

Linear regression represents a numeric target as an intercept plus a weighted sum of features. In one dimension this is a line; with several features it is a plane or hyperplane. Mean squared error, or MSE, averages squared residuals and therefore gives large mistakes more influence than small ones. Minimizing it chooses parameters according to that particular preference. Residual plots can reveal curved patterns or changing error spread that a single average hides. A fitted coefficient describes a conditional association within the model, not automatically a causal effect.

### 03 / Put the concept to work

Start with a constant prediction, such as the training target mean, and compare a linear model on the same held-out examples. Keep measurement units beside each feature and coefficient. Examine residuals against predictions and important inputs. If large errors dominate the result, inspect their provenance before changing the loss. Report a unit-preserving metric such as root mean squared error when communicating error magnitude.

### 04 / How others use it

The linked Google loss tutorial contrasts absolute and squared regression errors and explains how the choice changes the influence of large residuals. Its role here is to ground the loss definition, not supply the seedling story or numbers. Use the tutorial's comparison as a reading prompt, then calculate both metrics on your own measurements and explain which errors each metric emphasizes.

### 05 / The formula, unpacked

```text
ŷᵢ = b + w xᵢ
MSE = (1 / n) Σᵢ₌₁ⁿ (ŷᵢ − yᵢ)²
RMSE = √MSE
```

The index i identifies an observation and n is the number being evaluated. xᵢ is its input, yᵢ its measured target, and ŷᵢ the model prediction; the hat distinguishes an estimate from a measurement. b is the intercept, expressed in target units. w is the slope, expressed in target units per input unit. The difference ŷᵢ − yᵢ is a signed residual. Σ sums over all observations, the superscript 2 squares each residual, and √ takes a square root. MSE has squared target units; RMSE returns to target units.

### 06 / Work through the numbers

Use three synthetic observations with input days 1, 2, and 3 and heights 3, 5, and 8 centimeters. A candidate line with b = 1 and w = 2 predicts 3, 5, and 7. Its residuals are 0, 0, and −1 centimeters; the squared errors sum to 1, giving MSE = 1 / 3 ≈ 0.333 and RMSE ≈ 0.577 centimeters. A constant prediction equal to the target mean, 16 / 3, has squared errors 49 / 9, 1 / 9, and 64 / 9. Its MSE is 38 / 9 ≈ 4.222. The candidate line improves this comparison, but it is not claimed to be the least-squares optimum. These three training points also provide no independent estimate of future prediction quality.

**Where the analogy stops:** A straight line can miss nonlinear relationships, interactions, and abrupt changes. Squared loss is sensitive to extreme residuals, whether they reflect meaningful events or measurement errors. Extrapolating beyond the observed feature range can be unreliable. Correlated inputs can make individual coefficients unstable even when predictions remain useful.

**Keep this idea:** Linear regression is a transparent baseline; its loss defines which mistakes matter, and its residuals reveal what the line leaves unexplained.

### Sources for this topic

- [Google: Linear regression: Loss](https://developers.google.com/machine-learning/crash-course/linear-regression/loss)

<a id="gradient-descent-scaling"></a>

## Learn with controlled steps and comparable scales

### 01 / The story

Asha builds a model of how far a small robot cart travels during a motor pulse. One input is pulse duration in seconds, while another is an encoder count measured in thousands. Her training loss jumps upward after a few updates, and she initially assumes that the model is too simple. Before adding features, she inspects the update sizes and finds that one coefficient moves far more sharply than the other. She rescales the inputs using statistics from the training recordings and reduces the learning rate. The loss now descends steadily. To understand the change, she repeats one update by hand on two invented observations. That small calculation turns a mysterious training curve into a sequence of understandable decisions. She learns to separate an optimization problem from a model that genuinely lacks useful information.

### 02 / The concept

Gradient descent updates parameters in the direction opposite the local slope of the loss. The learning rate controls how far each step travels; too large a step can overshoot, while very small steps can be slow. Feature scaling changes the geometry of the optimization problem and can make a shared learning rate more workable. Standardization subtracts a training mean and divides by a training standard deviation. It changes units, not the information available. Convergence of training loss alone says nothing about leakage, causal meaning, or performance on new examples.

### 03 / Put the concept to work

Fit scaling statistics on training data and reuse them unchanged for validation and testing. Plot loss against updates, check for exploding or non-finite values, and try a smaller learning rate when steps are unstable. Compare training and validation curves before deciding whether to train longer. Handle constant features explicitly because their standard deviation is zero. Save the fitted transformation together with the final model.

### 04 / How others use it

The linked Google gradient-descent tutorial follows repeated parameter updates and visualizes training loss. Its separate normalization tutorial discusses feature scales and their effect on optimization. Together they provide a documented route from a loss definition to a practical training diagnostic. Recreate the logic with the cart example below, then explain why the same numerical learning rate need not behave identically after changing input units.

### 05 / The formula, unpacked

```text
zᵢ = (xᵢ − μ_train) / s_train
L(w,b) = (1 / n) Σᵢ₌₁ⁿ (w zᵢ + b − yᵢ)²
g_w = (2 / n) Σᵢ₌₁ⁿ (w zᵢ + b − yᵢ) zᵢ
g_b = (2 / n) Σᵢ₌₁ⁿ (w zᵢ + b − yᵢ)
w_new = w − η g_w; b_new = b − η g_b
```

xᵢ is raw input i; μ_train and s_train are the training mean and population standard deviation, with s_train positive. zᵢ is the standardized input and yᵢ the target. n counts training examples, and Σ sums over them. w and b are the current slope and intercept. L is mean squared loss. g_w and g_b are its partial derivatives with respect to those parameters. η is the positive learning rate. The suffix new marks the updated value. Both gradients are evaluated at the same old parameters before either update is applied.

### 06 / Work through the numbers

Take raw inputs 2 and 6, with targets 1 and 3. The training mean is 4 and the population standard deviation is 2, so standardized inputs are −1 and 1. Start with w = 0 and b = 0. Predictions are both zero, giving L = (1 + 9) / 2 = 5. The weight gradient is (2 / 2)[(−1)(−1) + (−3)(1)] = −2, and the intercept gradient is −4. With learning rate 0.1, simultaneous updates give w_new = 0.2 and b_new = 0.4. New predictions are 0.2 and 0.6, so the new loss is (0.64 + 5.76) / 2 = 3.2. One step reduces loss by 1.8; it does not finish optimization or demonstrate generalization.

**Where the analogy stops:** Scaling does not repair mislabeled examples or missing explanatory variables. Standard deviation can be strongly affected by outliers. Gradient descent requires a suitable step size even for a convex objective; convexity alone does not make every update stable. More complex models may have nonconvex losses and different convergence behavior.

**Keep this idea:** Inspect the update rule, input units, and loss curve together; stable optimization is necessary for learning, but it is not evidence of generalization.

### Sources for this topic

- [Google: Linear regression: Gradient descent](https://developers.google.com/machine-learning/crash-course/linear-regression/gradient-descent)

- [Google: Numerical data: Normalization](https://developers.google.com/machine-learning/crash-course/numerical-data/normalization)

- [scikit-learn: Common pitfalls and recommended practices](https://scikit-learn.org/stable/common_pitfalls.html)

<a id="logistic-thresholds"></a>

## Separate probability estimates from decisions

### 01 / The story

Leo helps a backyard astronomy group decide whether to prepare cameras for a clear evening. He trains a classifier from weather measurements available before sunset and obtains values such as 0.35 and 0.72. A friend interprets these as final yes-or-no instructions, but Leo notices that the group has two different decisions. Setting out a portable camera is easy to reverse, while assembling a delicate tracking rig takes much longer. He keeps the same probability model and compares different decision thresholds on validation evenings. The portable camera can tolerate more false alarms; the tracking rig needs stronger evidence. They record the selected rule before checking the reserved test evenings. The lesson is that a probability estimate summarizes the model's belief, while a threshold expresses how a particular action will use that estimate.

### 02 / The concept

Binary logistic regression maps a linear score through the sigmoid function to produce a number between zero and one. That number is interpreted as an estimated probability of the chosen positive class. A threshold converts the estimate into a class decision, but changing it does not retrain the model. Lowering the threshold generally includes more positive predictions; raising it includes fewer. Probability calibration is a separate question: predictions near 0.7 should correspond to roughly 70% positives over suitable repeated cases if the model is calibrated.

### 03 / Put the concept to work

Name the positive class before training and keep that definition consistent in metrics. Use validation data to compare thresholds under the intended action costs or review capacity. Inspect both false positives and false negatives at the chosen operating point. If probabilities themselves inform decisions, check calibration as well as classification accuracy. Freeze the threshold before the final test, and document how ties at the threshold are handled.

### 04 / How others use it

The linked Google sigmoid tutorial explains how a linear score becomes a probability estimate. Its thresholding tutorial then connects probability cutoffs with confusion-matrix outcomes. Read these as two distinct stages of a classifier. In the original astronomy example, the model can remain fixed while the preparation rule changes; the official material supports that distinction without claiming any astronomy deployment or validating this invented dataset.

### 05 / The formula, unpacked

```text
z = b + w x
p = 1 / (1 + exp(−z))
ŷ = I[p ≥ τ]
```

x is one measured feature, w its learned coefficient, and b the intercept. z is the resulting linear score, interpreted as the model's log-odds for the positive class. exp is the exponential function with base e, approximately 2.71828. p is the estimated probability of that positive class. τ is a chosen decision threshold between zero and one. ŷ is the predicted binary label. I equals one when the bracketed condition is true and zero otherwise; this convention assigns an exact threshold tie to the positive class.

### 06 / Work through the numbers

Suppose an illustrative model uses b = −1.2, w = 0.8, and feature value x = 2. The linear score is z = −1.2 + 0.8 × 2 = 0.4. Since exp(−0.4) ≈ 0.6703, the estimated positive probability is 1 / 1.6703 ≈ 0.5987. With threshold 0.50, the model predicts the positive class; with threshold 0.65, it predicts the negative class. The probability and coefficients have not changed. For comparison, x = 0 gives z = −1.2 and p ≈ 0.2315. These are model outputs, not observed frequencies or guarantees about a particular evening. To justify either threshold, Leo would need labeled validation cases and an explicit preference between unnecessary preparation and missing a useful observing opportunity.

**Where the analogy stops:** A sigmoid output is not automatically a well-calibrated probability. A linear decision boundary can miss important interactions unless the features represent them. Threshold preferences may change with class prevalence, action costs, or available capacity. Choosing a threshold on the test set contaminates the final evaluation just as choosing model parameters there would.

**Keep this idea:** Train the probability model and choose the decision threshold as related but separate steps, then evaluate the complete rule on untouched data.

### Sources for this topic

- [Google: Logistic regression: Calculating a probability with the sigmoid function](https://developers.google.com/machine-learning/crash-course/logistic-regression/sigmoid-function)

- [Google: Thresholds and the confusion matrix](https://developers.google.com/machine-learning/crash-course/classification/thresholding)

<a id="metrics-imbalance"></a>

## Count the mistakes that the task actually cares about

### 01 / The story

Tessa builds a detector for a rare frog call in long evening recordings. Most clips contain wind, insects, or silence, so a classifier that always says no call looks impressive when she checks accuracy. Listening to its selected clips reveals the problem: there are no selected clips at all. She labels a small evaluation collection and writes four counts on a sheet: calls found, calls missed, false alarms, and correctly rejected background. Now two models that seemed similar have visibly different behavior. One finds more calls but asks her to listen to many extra clips; another provides cleaner selections but misses quiet calls. Tessa chooses a validation criterion that matches the time available for listening and reports the missed-call count separately. Her evaluation becomes a description of scientific usefulness instead of a single flattering percentage.

### 02 / The concept

Accuracy measures the fraction of all predictions that are correct. Precision asks how many predicted positives are truly positive, while recall asks how many actual positives are found. Their denominators answer different questions, especially when the positive class is rare. F1 is the harmonic mean of precision and recall, but it ignores true negatives and encodes a particular balance between the two quantities. No metric is universally best. Choose metrics that reflect the intended use, and retain the confusion-matrix counts so readers can reconstruct the tradeoffs.

### 03 / Put the concept to work

Report the positive-class definition, prevalence, threshold, and four confusion-matrix counts with your metrics. Compare against a simple baseline, including an always-negative classifier when appropriate. Use validation data to examine precision and recall across thresholds. Check important recording conditions separately, such as quiet versus windy evenings. When denominators are zero, state the undefined quantity or the explicit reporting convention instead of silently treating it as excellent performance.

### 04 / How others use it

The linked Google classification-metrics tutorial defines accuracy, precision, recall, and F1 and discusses how error priorities affect metric choice. Use that official framework to audit the original frog-detector example. Rebuild each metric from the four counts before drawing a conclusion, and explain why a high accuracy can coexist with no successful detections. The tutorial is the factual reference; the recording scenario and counts are original.

### 05 / The formula, unpacked

```text
N = TP + TN + FP + FN
Accuracy = (TP + TN) / N
Precision = TP / (TP + FP)
Recall = TP / (TP + FN)
F1 = 2 TP / (2 TP + FP + FN)
```

TP counts true positives: actual calls labeled as calls. TN counts true negatives: background clips labeled as background. FP counts false positives: background clips incorrectly labeled as calls. FN counts false negatives: actual calls that the detector misses. N is the total number of evaluated clips. Accuracy, Precision, Recall, and F1 name the four dimensionless metrics shown. Multiplication is implied in 2 TP. Each denominator must be checked before division; for example, precision is undefined when TP + FP is zero because no clips were predicted positive.

### 06 / Work through the numbers

Create one hundred labeled clips: ten contain calls and ninety contain background. Suppose a detector finds eight calls, misses two, and flags twelve background clips. Then TP = 8, FN = 2, FP = 12, and TN = 78. Accuracy is (8 + 78) / 100 = 86%. Precision is 8 / 20 = 40%, recall is 8 / 10 = 80%, and F1 is 16 / 30 ≈ 53.3%. An always-negative baseline reaches 90% accuracy because it rejects all ninety background clips, but its recall is zero. Its precision is undefined because it predicts no positives. Thus the detector has lower accuracy yet retrieves eight calls that the baseline misses. Whether twelve false alarms are acceptable depends on the intended listening workflow.

**Where the analogy stops:** A confusion matrix describes one threshold on one evaluation set. Precision can change when the positive-class prevalence changes, even if other behavior appears similar. F1 does not express every cost preference. Small numbers of positives make recall estimates unstable, and a pooled score can hide poor performance in particular conditions.

**Keep this idea:** Keep the confusion matrix close to every headline score; the right metric must reveal the errors that matter for the intended use.

### Sources for this topic

- [Google: Classification: Accuracy, recall, precision, and related metrics](https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall)

- [Google: Thresholds and the confusion matrix](https://developers.google.com/machine-learning/crash-course/classification/thresholding)

<a id="trees-ensembles"></a>

## Build rules, then understand what combining them changes

### 01 / The story

Niko tests paper kites with different wing angles and tail lengths. A linear classifier misses a pattern: long tails help at one wing angle but hurt at another. He draws a small decision tree that first asks about angle and then asks about tail length. The rules are easy to inspect, yet a deeper version memorizes nearly every flight and changes dramatically when one windy trial is removed. Niko limits the depth and compares the result with a collection of randomized trees. Their combined predictions vary less across his repeated training samples, although the model is harder to summarize as a single rule. He keeps a shallow tree for understanding and an ensemble as a candidate for prediction, evaluating both on flights reserved beforehand. More rules become useful only when they survive the same fair comparison.

### 02 / The concept

A decision tree repeatedly divides feature space into regions and predicts from the examples in each leaf. For binary classification, Gini impurity measures how mixed a node's labels are; a candidate split is judged by the weighted impurity of its children. Deep trees can fit complicated patterns and also memorize noise. Random forests average predictions from randomized trees, often reducing variance. Boosting instead builds a sequence of learners that improve a chosen objective. Both are ensembles, but their training logic and tuning choices differ.

### 03 / Put the concept to work

Fit a shallow tree first and inspect its conditions against the data. Tune depth and minimum leaf size within validation, then compare a forest or boosted trees using identical splits and metrics. Examine stability across reasonable training variations. For interpretation, distinguish a useful predictive split from a causal explanation. Record whether an ensemble combines class votes or probabilities, since these can yield different decisions.

### 04 / How others use it

The linked scikit-learn decision-tree guide demonstrates classification and regression trees and explains depth-related overfitting. Its ensemble guide distinguishes randomized forests from boosting and specifies that its forest classifier averages class probabilities. Those details ground the kite comparison and the averaging calculation below. They also explain why describing every forest implementation as a majority vote can obscure the actual prediction rule being used.

### 05 / The formula, unpacked

```text
G(p) = 2 p (1 − p)
ΔG = G(p) − (n_L / n) G(p_L) − (n_R / n) G(p_R)
p_forest = (1 / T) Σₜ₌₁ᵀ qₜ
```

p is the positive-class fraction in a parent node and G is its binary Gini impurity. n is the parent sample count; n_L and n_R count samples sent to the left and right children, so n = n_L + n_R. p_L and p_R are their positive fractions. ΔG is the impurity reduction from that split. T is the number of trees, t indexes a tree, and qₜ is that tree's predicted positive probability for the same input. Σ adds these probabilities; p_forest is their unweighted average.

### 06 / Work through the numbers

A parent node contains six successful flights and four unsuccessful ones, so p = 0.6 and G = 2 × 0.6 × 0.4 = 0.48. A proposed split sends four successes and one failure left, and two successes and three failures right. The child impurities are 0.32 and 0.48. Each child has five examples, so weighted impurity is 0.5 × 0.32 + 0.5 × 0.48 = 0.40. The reduction is 0.08, a local improvement rather than proof of better test performance. Separately, suppose three trees predict positive probabilities 0.2, 0.7, and 0.9 for a new flight. Their average is 1.8 / 3 = 0.6, producing a positive decision at threshold 0.5. This probability average is the stated ensemble rule.

**Where the analogy stops:** Greedy splits optimize local choices and need not produce a globally optimal tree. Forests can still fail when many trees share the same misleading signal. Large ensembles require more resources and are harder to inspect. Feature importance describes model behavior under particular assumptions; it does not establish that changing a feature will change the outcome.

**Keep this idea:** Trees turn interactions into explicit regions; ensembles can stabilize predictions, but every added layer of complexity still needs validation on the intended task.

### Sources for this topic

- [scikit-learn: Decision Trees](https://scikit-learn.org/stable/modules/tree.html)

- [scikit-learn: Ensembles: Gradient boosting, random forests, bagging, voting, stacking](https://scikit-learn.org/stable/modules/ensemble.html)

<a id="clustering-pca"></a>

## Find structure without inventing labels

### 01 / The story

Imani measures the length, width, mass, and surface texture of stones collected along a river walk. She has no geological labels and wants a compact view of the collection. A clustering routine returns three groups, which she initially names as if they were established rock types. Looking more carefully, she sees that changing the units of mass reshapes the groups. She standardizes the measurements for a clearly stated comparison and uses principal component analysis to inspect the largest directions of variation. The plot reveals a broad size trend, while clustering proposes divisions within that representation. Imani replaces her confident labels with neutral group identifiers and compares representative stones by hand. The analysis now helps her form questions for further study. It does not magically supply the missing geological ground truth.

### 02 / The concept

Clustering groups observations according to a chosen similarity structure. K-means minimizes the sum of squared distances from points to their assigned centroids, so feature units and cluster shape matter. Principal component analysis, or PCA, instead finds orthogonal directions that preserve the most variance in centered data. It produces coordinates, not class labels. PCA can precede clustering, but discarded low-variance directions may still contain meaningful distinctions. Both methods reveal structure relative to their assumptions; neither independently proves that a group corresponds to a natural category.

### 03 / Put the concept to work

Choose features and scaling according to the comparison you intend, and preserve the transformation for later observations. Inspect representative members of each cluster and compare several plausible cluster counts or initializations. For PCA, report retained variance and examine the component loadings. If the representation will feed a supervised model, fit it inside training folds. Use domain evidence to interpret groups rather than treating cluster identifiers as discovered truth.

### 04 / How others use it

The linked scikit-learn clustering guide describes the k-means objective and the shapes it handles poorly. The linked decomposition guide illustrates PCA with a lower-dimensional view of the Iris measurements and notes that PCA centers inputs without automatically scaling each feature. These official examples clarify the different jobs of grouping and projection. The river-stone story and rectangular dataset below are original illustrations of those distinctions.

### 05 / The formula, unpacked

```text
J = Σᵢ₌₁ⁿ ‖xᵢ − μ_cᵢ‖²
S = (1 / n) Σᵢ₌₁ⁿ (xᵢ − x̄)(xᵢ − x̄)ᵀ
S vⱼ = λⱼ vⱼ
r₁ = λ₁ / Σⱼ₌₁ᵈ λⱼ
```

n counts observations and i selects one. xᵢ is a vector of d features; cᵢ identifies its cluster and μ_cᵢ is that cluster's centroid. The squared norm ‖·‖² sums squared coordinate differences, and J is total within-cluster squared distance. x̄ is the mean vector. S is the covariance matrix using divisor n here. Superscript T transposes a vector, making the product an outer product. vⱼ is principal direction j and λⱼ its variance, ordered largest first. Σ denotes summation. r₁ is the variance fraction retained by the first component, assuming positive total variance.

### 06 / Work through the numbers

Consider four two-dimensional points: (0,0), (0,2), (4,0), and (4,2), with both axes already in comparable units. Two clusters divided by the first coordinate have centroids (0,1) and (4,1). Every point has squared distance 1 from its centroid, so J = 4. A single centroid at (2,1) gives squared distance 5 per point and J = 20. For PCA, subtract the mean (2,1). The population covariance matrix is diagonal with entries 4 and 1, so the first principal direction is (1,0), up to its arbitrary sign. It preserves 4 / (4 + 1) = 80% of total variance. Keeping one component discards the vertical distinction. Lower clustering loss and high retained variance describe geometry, not the correctness of imagined category labels.

**Where the analogy stops:** K-means can struggle with irregular shapes, unequal densities, and outliers; its objective also decreases as more clusters are allowed. PCA captures linear variance, which may reflect nuisance variation instead of useful signal. Scaling choices alter both analyses, and a visually separated projection does not establish a meaningful scientific distinction.

**Keep this idea:** Use clustering to propose groups and PCA to compress variation, then test your interpretation with evidence that neither method supplied.

### Sources for this topic

- [scikit-learn: Clustering](https://scikit-learn.org/stable/modules/clustering.html)

- [scikit-learn: Decomposing signals in components: Principal component analysis](https://scikit-learn.org/stable/modules/decomposition.html#principal-component-analysis-pca)

<a id="validation-regularization-shift"></a>

## Validate choices and prepare for a changing setting

### 01 / The story

Ren models humidity in a small greenhouse using many correlated sensor readings. A flexible fit follows the first month almost perfectly, yet its estimates deteriorate on later days. He tries regularization to discourage large coefficients and compares strengths using folds that respect time. The model with the smallest training error no longer wins. After selecting a simpler candidate, he evaluates it on a final untouched period and records the result. Weeks later, new ventilation equipment changes the relationship between temperature and humidity. Ren sees that the old test result cannot promise performance under this new condition. He checks input ranges, obtains new labeled measurements, and reevaluates before relying on the model again. His notebook now treats validation as a decision process and monitoring as a continuing responsibility, with regularization helping only one part of the problem.

### 02 / The concept

Validation estimates how a modeling choice performs beyond the examples used to fit it. Cross-validation repeats this comparison across splits, but the split structure must reflect dependencies and the intended use. L2 regularization adds a penalty for large coefficients, trading some training fit for a simpler parameter solution. Its strength is selected using validation, not the final test. Distribution shift means the future input or target relationship differs from the evaluated setting. Regularization can reduce overfitting without protecting against every shift, so a good development score remains conditional evidence.

### 03 / Put the concept to work

Define a modest set of candidate settings and compare them on the same validation folds. Place every learned preprocessing step inside each fold. Use group or chronological splits when the task requires them, and keep a final evaluation period untouched by selection. Record input ranges, class proportions when relevant, and error patterns. After deployment changes, obtain fresh labeled evidence rather than treating input monitoring alone as a performance measurement.

### 04 / How others use it

The linked scikit-learn cross-validation guide documents group-aware and time-ordered splitters. Its linear-model guide presents ridge regression and validation of regularization strength. The linked Google dataset guide also discusses mismatches between evaluation data and later use. These sources support the workflow, while the greenhouse narrative is original. Note that the averaged-loss objective below uses a different penalty normalization from scikit-learn Ridge's summed-loss convention. With otherwise matching conventions, the Ridge penalty parameter equals the training sample count times λ.

### 05 / The formula, unpacked

```text
L_λ(w,b) = (1 / n) Σᵢ₌₁ⁿ (b + wᵀxᵢ − yᵢ)² + λ Σⱼ₌₁ᵈ wⱼ²
CV(λ) = (1 / K) Σₖ₌₁ᴷ MSEₖ(λ)
```

n is the training sample count; i indexes observations and j indexes d features. xᵢ is an input vector, yᵢ its target, w the coefficient vector, and b the unpenalized intercept. Superscript T denotes transpose, so wᵀxᵢ is a dot product. λ is a nonnegative penalty strength and L_λ the penalized training objective. Σ denotes summation. K is the number of validation folds and k selects one. MSEₖ is unpenalized error on fold k after fitting its corresponding training portion. CV is their unweighted mean; unequal fold sizes would require weights for a pooled per-example mean.

### 06 / Work through the numbers

Compare two synthetic coefficient vectors under the stated averaged-loss convention. Candidate A has training MSE 1.0 and squared coefficient sum 9; candidate B has training MSE 1.4 and squared coefficient sum 1. At λ = 0.1, their penalized objectives are 1.9 and 1.5, so B has the smaller objective despite worse raw training fit. This comparison illustrates the penalty and does not assert either vector is the optimized solution. Separately, suppose a validation search gives three equal-sized fold errors of 1.0, 1.4, and 1.2 for λ = 0, versus 0.9, 1.0, and 1.1 for λ = 0.1. Their means are 1.2 and 1.0. Choose the latter setting by validation, refit on development data, and evaluate once on the reserved final period.

**Where the analogy stops:** Repeatedly searching many settings can overfit validation data. Cross-validation is not automatically valid for dependent observations or future forecasting. Regularization depends on feature scale and cannot supply missing information. Detecting a change in inputs does not prove accuracy fell, while stable input summaries do not guarantee that the target relationship remained stable.

**Keep this idea:** Use validation to choose complexity, reserve testing for the completed choice, and gather fresh evidence whenever the intended prediction setting changes.

### Sources for this topic

- [scikit-learn: Cross-validation: evaluating estimator performance](https://scikit-learn.org/stable/modules/cross_validation.html)

- [scikit-learn: Linear Models: Ridge regression and classification](https://scikit-learn.org/stable/modules/linear_model.html#ridge-regression-and-classification)

- [Google: Datasets: Dividing the original dataset](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets)

## The reference desk

### [Audit information before scoring](#framing-splits-leakage)

State the prediction time and holdout unit. Fit preprocessing only on training data, and check identities, duplicates, and future-derived features.

### [Read the residuals](#linear-regression-mse)

Calculate errors before trusting a regression score. MSE emphasizes large mistakes; RMSE restores target units. Neither makes a coefficient causal.

### [Check scale and step size](#gradient-descent-scaling)

Use training statistics for scaling, evaluate gradients at the same old parameters, and inspect both training and validation curves.

### [Name the decision rule](#logistic-thresholds)

A probability and a threshold play different roles. Select the threshold on validation data and state the positive class and tie convention.

### [Keep the four counts](#metrics-imbalance)

Report true positives, true negatives, false positives, and false negatives. Check prevalence and denominators before interpreting accuracy, precision, recall, or F1.

### [Validate the rules you combine](#trees-ensembles)

Limit tree complexity and compare ensembles on the same split. Local impurity reduction and feature importance do not establish causality.

### [Interpret geometry cautiously](#clustering-pca)

Clusters propose groups; principal components preserve variance. Scaling changes both, and neither supplies the missing scientific labels.

### [Treat generalization as conditional](#validation-regularization-shift)

Tune regularization with appropriate validation, then test the finished choice. When the setting changes, collect fresh labels and reevaluate.

## Official tutorials & original research

Original stories, explanations and examples by Guoliang. The linked tutorials and research belong to their respective authors; these independent companions are not official translations or endorsed courses.

- [Datasets: Dividing the original dataset](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets) — Google

- [Common pitfalls and recommended practices](https://scikit-learn.org/stable/common_pitfalls.html) — scikit-learn

- [Linear regression: Loss](https://developers.google.com/machine-learning/crash-course/linear-regression/loss) — Google

- [Linear regression: Gradient descent](https://developers.google.com/machine-learning/crash-course/linear-regression/gradient-descent) — Google

- [Numerical data: Normalization](https://developers.google.com/machine-learning/crash-course/numerical-data/normalization) — Google

- [Logistic regression: Calculating a probability with the sigmoid function](https://developers.google.com/machine-learning/crash-course/logistic-regression/sigmoid-function) — Google

- [Thresholds and the confusion matrix](https://developers.google.com/machine-learning/crash-course/classification/thresholding) — Google

- [Classification: Accuracy, recall, precision, and related metrics](https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall) — Google

- [Decision Trees](https://scikit-learn.org/stable/modules/tree.html) — scikit-learn

- [Ensembles: Gradient boosting, random forests, bagging, voting, stacking](https://scikit-learn.org/stable/modules/ensemble.html) — scikit-learn

- [Clustering](https://scikit-learn.org/stable/modules/clustering.html) — scikit-learn

- [Decomposing signals in components: Principal component analysis](https://scikit-learn.org/stable/modules/decomposition.html#principal-component-analysis-pca) — scikit-learn

- [Cross-validation: evaluating estimator performance](https://scikit-learn.org/stable/modules/cross_validation.html) — scikit-learn

- [Linear Models: Ridge regression and classification](https://scikit-learn.org/stable/modules/linear_model.html#ridge-regression-and-classification) — scikit-learn
