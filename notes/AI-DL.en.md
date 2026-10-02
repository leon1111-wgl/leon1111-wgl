# Deep Learning

> Guoliang | AI Field Guides

[EN](AI-DL.en.md) · [中文](AI-DL.zh.md)

Follow eight connected ideas through original miniature stories, explicit equations, and checked calculations. Learn how neural networks represent inputs, receive gradients, change during training, and earn trust on unseen data. The stories are illustrative; documented uses are identified separately and linked to primary sources.

## A route through the ideas

8 topics · tensors → representations → gradients → optimization → regularization → convolution → attention → transfer

### Before you start

- Vectors and matrix multiplication
- Functions, derivatives, and the chain rule
- Training, validation, and test splits
- Basic probability and logarithms

### What you will learn

- Track a batch through a network without losing axis meaning
- Derive a small backward pass and compare optimizer updates
- Separate training behavior from evaluation behavior
- Explain convolution, residual paths, and attention numerically
- Plan transfer learning with an honest validation boundary

## Knowledge framework

### Represent and differentiate

- [Tensors: give every axis a meaning](#dl-tensors)
- [MLPs: learn useful intermediate features](#dl-representations)
- [Backpropagation: follow the chain of dependence](#dl-autograd)

### Optimize and control

- [Minibatches and optimizers: turn gradients into steps](#dl-optimization)
- [Regularization: train with noise, evaluate deliberately](#dl-regularization)

### Build structure and adapt

- [Convolutions and residual paths: local evidence, preserved routes](#dl-convolution)
- [Attention: retrieve context with learned comparisons](#dl-attention)
- [Transfer learning: adapt features without losing the evaluation boundary](#dl-transfer)

<a id="dl-tensors"></a>

## Tensors: give every axis a meaning

### 01 / The story

Mina is building a small classifier for recordings from three laboratory sensors. Each recording becomes three summary numbers, and she wants to process several recordings together. Her first version runs without an error, yet its predictions change when she replaces the other recordings in the batch. The problem is not mysterious learning behavior: she has averaged across the batch axis while preparing each example. Mina draws a table with recordings as rows and sensor features as columns. She labels the intended shape before every operation, then checks one row by hand. After moving the reduction to the feature axis, each recording has its own summary again. This repair gives her a durable habit: a tensor shape describes both the amount of data and the meaning of its organization.

### 02 / The concept

A tensor is an indexed collection of numbers. Its axes can represent examples, channels, positions, or learned features; the numbers alone do not encode those roles. A dense layer combines the feature axis with a weight matrix while preserving the batch axis. Broadcasting can add one bias vector to every example, but compatible shapes do not guarantee compatible meanings. Reshaping changes the grouping of entries, whereas transposing changes their axis order. Tracking shape, data type, and device together turns many apparent modeling failures into ordinary, inspectable data transformations.

### 03 / Put the concept to work

Write a shape contract at the data loader boundary and at each layer boundary. State which axis is the batch, how features are ordered, and whether a reduction should preserve one result per example. Before a large run, send two deliberately different examples through the pipeline. Inspect whether changing one example unexpectedly changes the other, and distinguish intended batch statistics from accidental mixing.

### 04 / How others use it

The official PyTorch Tensors tutorial represents inputs and model parameters with tensors, inspects their shape, data type, and device, and distinguishes matrix multiplication from elementwise multiplication. These are concrete preparation and inspection operations used before neural network training. The tutorial also demonstrates explicit device transfers, showing why a correct mathematical expression still requires compatible storage locations in an actual implementation.

### 05 / The formula, unpacked

```text
X ∈ ℝ^(B×d), W ∈ ℝ^(d×k), b ∈ ℝ^k
Y = XW + b
Y[i,j] = Σ(r=1…d) X[i,r]W[r,j] + b[j]
```

X is the input matrix; B counts examples and d counts features per example. W is the learned weight matrix, and k is the number of output features. b is a length k bias vector broadcast across rows. Y is the resulting B by k output matrix. i identifies an example, j identifies an output feature, and r indexes an input feature being summed. ℝ denotes real numbers, × specifies axis sizes, and Σ adds the products over all d input features. Brackets select individual entries.

### 06 / Work through the numbers

Take two recordings with X = [[2, 1, 0], [0, 3, 1]]. Choose W = [[1, −1], [2, 0], [0, 3]] and b = [0.5, −0.5]. The first row produces [2×1 + 1×2 + 0×0 + 0.5, 2×(−1) + 1×0 + 0×3 − 0.5] = [4.5, −2.5]. The second produces [6.5, 2.5], so Y has shape 2 by 2. Averaging across recordings gives [5.5, 0], one mean per output feature. Averaging across features instead gives [1, 4.5], one mean per recording. Both operations return two numbers; only axis meaning tells us which answers the intended question. The dense layer uses six weights and two biases, independently of this batch size.

**Where the analogy stops:** Shape checks cannot detect swapped feature names, mismatched physical units, or labels attached to the wrong rows. Broadcasting may silently produce a larger result than intended. Batch dependent layers also create legitimate interactions between examples, so independence checks must be interpreted with the architecture and its training mode in mind.

**Keep this idea:** Treat every tensor axis as a named contract; matching dimensions is necessary, but preserving their meaning is what makes the computation correct.

### Sources for this topic

- [PyTorch: Tensors — Learn the Basics](https://docs.pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html)

<a id="dl-representations"></a>

## MLPs: learn useful intermediate features

### 01 / The story

Ravi monitors two gauges that should normally agree. A large reading on either gauge is harmless when the other rises with it, so a simple weighted average produces many false alarms. He first adds another linear layer, hoping that extra depth will uncover the disagreement. The model still behaves like one straight transformation. Ravi then introduces two hidden units: one responds when the first gauge exceeds the second by a margin, and the other responds to the reverse situation. A rectifier suppresses negative responses, allowing the final layer to combine two directions of disagreement. His small demonstration now distinguishes common movement from mismatch. The important change was not the layer count alone; it was a representation that preserved the particular relationship the task needed.

### 02 / The concept

A multilayer perceptron alternates affine transformations with nonlinear activations. Hidden units construct intermediate features that a later layer recombines. Without nonlinearities, a sequence of affine layers collapses into a single affine map, regardless of depth. ReLU keeps positive inputs and maps negative inputs to zero, producing different linear behavior in different regions of input space. Representation learning means choosing these intermediate transformations through training rather than specifying every feature manually. The resulting features can help a task without corresponding to recognizable human concepts or providing a causal explanation.

### 03 / Put the concept to work

Start with a compact network whose input features and output meaning are explicit. Choose the last layer and loss together: classification logits, probabilities, and continuous predictions have different roles. Inspect activation distributions to find units that are always zero or unusually large. Increase width or depth only after checking data quality and validation behavior, so additional capacity addresses an observed limitation.

### 04 / How others use it

PyTorch’s Build the Neural Network tutorial constructs a FashionMNIST classifier from a flattening operation, linear layers, and ReLU activations. It separates the network’s raw class scores from probabilities obtained by a later softmax operation. This official example shows how a basic MLP connects image entries to class outputs; the gauge scenario and all numbers here are independent illustrations.

### 05 / The formula, unpacked

```text
h = ReLU(W₁x + b₁), ReLU(u) = max(0,u)
ŷ = W₂h + b₂
P = Hd + H + kH + k
```

x is a column vector containing d input features. W₁ has H rows and d columns, while b₁ contains H hidden biases. h is the length H hidden representation. W₂ has k rows and H columns, and b₂ contains k output biases. ŷ is the length k prediction vector. ReLU applies max(0,u) separately to each scalar preactivation u. P counts every weight and bias in this two layer network. Subscripts 1 and 2 identify the two affine layers; they are not powers or time steps.

### 06 / Work through the numbers

Let d = 2, H = 2, and k = 1. Set W₁ = [[1, −1], [−1, 1]], b₁ = [−1, −1], W₂ = [[1, 1]], and b₂ = 0. For x = [3, 1], the hidden preactivations are [1, −3], so h = [1, 0] and ŷ = 1. Swapping the inputs to [1, 3] gives h = [0, 1], again producing 1. Equal inputs [2, 2] yield [−1, −1] before ReLU and a prediction of 0. This network measures disagreement beyond a one unit tolerance in either direction. Its parameter count is 2×2 + 2 + 1×2 + 1 = 9. These chosen weights demonstrate representational capacity; they are not a claim that training must discover this solution.

**Where the analogy stops:** An MLP does not automatically exploit image locality or sequence order. More parameters can increase memorization, computation, and sensitivity to preprocessing. ReLU units receiving negative inputs throughout training may receive no useful gradient through that branch. A convincing fitted relationship also remains different from evidence that the relationship will generalize.

**Keep this idea:** Nonlinear hidden layers matter because they change the available representations; extra linear depth alone cannot create a nonlinear decision rule.

### Sources for this topic

- [PyTorch: Build the Neural Network — Learn the Basics](https://docs.pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html)

<a id="dl-autograd"></a>

## Backpropagation: follow the chain of dependence

### 01 / The story

Elena adds a trainable scaling factor to a tiny sensor model, then watches the loss stay unchanged through several iterations. The optimizer exists, the forward calculation works, and the printed output looks plausible. Rather than replacing the optimizer, she writes the computation as a chain: input, affine value, activation, prediction, loss. She calculates the derivative along each link and expects a nonzero gradient at the first weight. The implementation reports no gradient there. A conversion made for logging had detached the activation before it reached the prediction. Elena keeps the original tensor in the model and converts only a separate logging value. The next backward pass reaches the weight. Her debugging question has changed from whether learning is happening to exactly which dependencies the program has preserved.

### 02 / The concept

Backpropagation applies the chain rule to a recorded computation, carrying the loss sensitivity backward through intermediate values. Automatic differentiation combines local derivatives using the executed graph; it does not guess gradients by repeatedly perturbing each parameter. The forward pass supplies both a prediction and information needed for the backward pass. A gradient describes local change in a specified objective, with other quantities held fixed. Computing that gradient and using it to update parameters are separate actions. Graph breaks, disabled gradient recording, and unsuitable operations can interrupt the intended dependency path.

### 03 / Put the concept to work

For a suspicious model, shrink the forward computation until a single example and a few parameters can be differentiated by hand. Check whether each trainable parameter receives a gradient and whether its sign makes sense. Clear accumulated gradients at the intended update boundary. Keep logging, conversion, and inference operations separate from the tensor path whose derivatives training requires.

### 04 / How others use it

The official autograd tutorial enables gradient tracking for parameters, constructs a loss, calls backward, and reads parameter gradients. It also demonstrates disabling tracking and detaching tensors. The optimization tutorial documents gradient accumulation and resetting. Together these examples show actual framework mechanisms behind the dependency chain: a valid forward result is insufficient evidence that the required backward route still exists.

### 05 / The formula, unpacked

```text
z = wx + b, a = max(0,z), ŷ = va
L = ½(ŷ − y)²
∂L/∂v = (ŷ − y)a
∂L/∂w = (ŷ − y)v·1[z>0]·x
∂L/∂b = (ŷ − y)v·1[z>0]
θ_new = θ − η·∂L/∂θ
```

x and y are one scalar input and its target. w and b define the first affine operation, z is its preactivation, and a is the rectified activation. v scales a into prediction ŷ. L is half the squared prediction error. The symbol ∂ denotes a partial derivative with other independent inputs fixed. 1[z>0] is one for positive z and zero for negative z; at zero this example uses derivative zero. θ stands for any of w, b, or v, θ_new is its updated value, and η is the learning rate.

### 06 / Work through the numbers

Use x = 2, y = 1, w = 0.5, b = 0, and v = 2. Forward evaluation gives z = 1, a = 1, ŷ = 2, and L = 0.5. The prediction error is 1, so the gradients are ∂L/∂v = 1, ∂L/∂w = 4, and ∂L/∂b = 2. With η = 0.05, update all three parameters from these same old gradients: v becomes 1.95, w becomes 0.3, and b becomes −0.1. The new z is 0.3×2 − 0.1 = 0.5, making ŷ = 0.975. The new loss is 0.5×(−0.025)² = 0.0003125. This decrease verifies this particular step, not a universal guarantee for every learning rate or example.

**Where the analogy stops:** Gradients can vanish, explode, or fail to reflect useful progress across nondifferentiable choices. Autograd differentiates the implemented objective, including any mistakes in that objective. Floating point arithmetic also limits precision. A small finite difference check can expose errors in a smooth toy case, but cannot certify an entire training pipeline.

**Keep this idea:** A gradient is a trace of dependency through the actual computation; preserve that trace before expecting an optimizer to improve the model.

### Sources for this topic

- [PyTorch: Automatic Differentiation with torch.autograd](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html)

- [PyTorch: Optimizing Model Parameters — Learn the Basics](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)

<a id="dl-optimization"></a>

## Minibatches and optimizers: turn gradients into steps

### 01 / The story

Noah trains a model on measurements collected over many days. Processing the entire archive before every update is slow, so he switches to small batches. The displayed loss begins to bounce, and he assumes the new procedure is broken. Looking closer, he finds that different batches contain different weather conditions and therefore different difficulty. He compares a moving training trend with a fixed validation set instead of judging one batch at a time. He also discovers that changing from SGD to Adam while keeping every setting unchanged changes the scale of early parameter updates. Noah records batch size, learning rate, and optimizer state together. The experiment becomes understandable once he treats the gradient estimate and the rule that converts it into a step as two separate design choices.

### 02 / The concept

A minibatch gradient averages loss derivatives over a subset of examples. It is a noisy estimate of the dataset gradient under appropriate sampling, trading statistical variability for cheaper updates. Basic SGD multiplies this estimate by a learning rate. Adam also maintains moving averages of the gradient and its square, corrects their initial bias, and rescales each parameter’s step. Batch size, loss reduction, sampling, and optimizer settings therefore interact. An epoch counts a pass through the dataset; an optimization step counts an update, so the two are not interchangeable units of progress.

### 03 / Put the concept to work

Define whether the loss is averaged or summed before selecting a learning rate. Shuffle training examples when that matches the data assumptions, and preserve grouping where observations are dependent. Record update counts as well as epochs. Compare optimizers under a controlled validation procedure, and save optimizer state when a resumed run should continue its existing momentum and adaptation history.

### 04 / How others use it

PyTorch’s optimization tutorial uses an explicit training loop with loss calculation, backward propagation, parameter updates, and gradient resetting. Its Adam reference gives the moving average and bias correction algorithm. These primary sources support two concrete implementations of the same training interface: gradients supply local information, while an optimizer determines how stored state and hyperparameters turn that information into changed weights.

### 05 / The formula, unpacked

```text
gₜ = (1/B) Σ(i=1…B) ∇θ ℓᵢ(θₜ₋₁)
SGD: θₜ = θₜ₋₁ − ηgₜ
Adam: mₜ = β₁mₜ₋₁ + (1−β₁)gₜ
vₜ = β₂vₜ₋₁ + (1−β₂)gₜ²
m̂ₜ = mₜ/(1−β₁ᵗ), v̂ₜ = vₜ/(1−β₂ᵗ)
θₜ = θₜ₋₁ − ηm̂ₜ/(√v̂ₜ + ε), m₀ = v₀ = 0
```

θ is the parameter vector, t counts updates, and η is the learning rate. B is batch size; i indexes its examples. ℓᵢ is example i’s loss, ∇θ means its parameter gradient, Σ sums those gradients, and gₜ is their average. mₜ and vₜ track first and second gradient moments. β₁ and β₂ are decay factors between zero and one; their superscript t means a power. Hats mark bias correction. ε is a positive stabilizer. Squares, roots, products, and division act elementwise. Initial moments are zero; these formulas omit momentum for SGD and weight decay for both optimizers.

### 06 / Work through the numbers

Consider two scalar targets, 2 and 4, with predictions θ and per example loss ½(θ−y)². At θ₀ = 0, the gradients are −2 and −4, so g₁ = −3. SGD with η = 0.1 gives θ₁ = 0.3 and mean loss 4.145, down from 5. For Adam, independently restart at zero with β₁ = 0.9, β₂ = 0.999, and ε = 10⁻⁸. Its first moments are m₁ = −0.3 and v₁ = 0.009. Bias correction gives m̂₁ = −3 and v̂₁ = 9. The update is approximately +0.1, producing mean loss approximately 4.705. Equal learning rates thus need not mean equal steps. This single batch calculation compares update mechanics, not eventual generalization or which optimizer is better.

**Where the analogy stops:** A noisy batch loss alone does not diagnose divergence. Conversely, a smooth training curve does not establish generalization. Adam’s adaptation cannot repair mislabeled targets, leakage, or a poor objective. Gradient accumulation also requires consistent normalization; accumulating several batch means without appropriate scaling changes the effective gradient and may change the intended step.

**Keep this idea:** Separate the gradient estimate from the update rule, and compare learning dynamics with batch size, normalization, and optimizer state visible.

### Sources for this topic

- [PyTorch: Optimizing Model Parameters — Learn the Basics](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)

- [PyTorch: Adam — optimizer reference](https://docs.pytorch.org/docs/main/generated/torch.optim.Adam.html)

<a id="dl-regularization"></a>

## Regularization: train with noise, evaluate deliberately

### 01 / The story

Sofia trains a network to recognize a small collection of instrument sounds. Training accuracy rises steadily while validation accuracy stops improving. She adds dropout, and the next run learns more slowly but performs more consistently on the reserved recordings. During a demonstration, however, the same recording receives slightly different scores each time. Sofia initially suspects file corruption. She then checks the model’s mode and finds that the demonstration still uses training behavior, so different activations disappear on every pass. Switching to evaluation mode removes that source of randomness. She keeps gradient recording disabled separately for ordinary inference. The episode connects two lessons: regularization changes how a model learns, and deploying that model requires an explicit decision about how its layers should behave.

### 02 / The concept

Regularization changes the learning problem to discourage brittle solutions that fit the training data too specifically. Dropout does this by randomly removing selected activations during training. In inverted dropout, surviving activations are divided by their survival probability, preserving each activation’s expectation. At evaluation, that dropout layer passes inputs through unchanged. This expectation statement concerns the layer output, not the exact prediction of an arbitrary nonlinear network. Training mode and gradient recording are separate controls: evaluation mode changes certain modules, while disabling gradients controls whether derivative history is recorded.

### 03 / Put the concept to work

Compare regularization settings using the same reserved data and a clearly defined selection metric. Keep training and evaluation mode changes visible in the workflow. During ordinary validation, select evaluation behavior and avoid recording gradients unless the analysis needs them. If scores remain unstable, inspect augmentation and other random operations as well; changing the dropout mode cannot remove every source of variation.

### 04 / How others use it

PyTorch’s Dropout reference specifies random zeroing and survival scaling during training, followed by identity behavior during evaluation. The Module reference documents evaluation mode as affecting modules such as dropout and batch normalization. These are operational distinctions in a real library, not merely terminology. They explain why a saved set of weights must be paired with an appropriate evaluation procedure.

### 05 / The formula, unpacked

```text
mⱼ ∼ Bernoulli(1−p), 0 ≤ p < 1
h̃ⱼ = mⱼhⱼ/(1−p)
E[h̃ⱼ | hⱼ] = hⱼ
Var(h̃ⱼ | hⱼ) = hⱼ²p/(1−p)
h_eval,ⱼ = hⱼ
```

hⱼ is activation j before dropout, treated as fixed when computing the expectation. p is the probability of dropping that activation, so 1−p is its survival probability. mⱼ is a binary mask drawn from a Bernoulli distribution: one means retained and zero means removed. h̃ⱼ is the random training output after survival scaling. E denotes expectation, Var denotes variance, and the vertical bar means conditioning on the original activation. h_eval,ⱼ is the corresponding evaluation output. The subscript j selects one element; ordinary elementwise dropout samples a mask for each element.

### 06 / Work through the numbers

Take a fixed activation hⱼ = 4 and dropout probability p = 0.25. With probability 0.75 the output is 4/0.75 = 16/3; otherwise it is zero. Its expectation is 0.75×16/3 = 4. Its second moment is 0.75×(16/3)² = 64/3, so the variance is 64/3 − 4² = 16/3, approximately 5.3333. For a vector [2, 4] and one sampled mask [1, 0], the training output becomes [8/3, 0]. In evaluation it is [2, 4]. One random pass clearly differs from the expected value. Preserving the mean therefore does not remove training noise, nor does it promise that a downstream nonlinear prediction equals the average prediction across all masks.

**Where the analogy stops:** Dropout can hurt when it removes information a small model already struggles to use. Its rate and placement need validation. Evaluation mode does not itself freeze parameters or disable gradients, and disabling gradients does not switch dropout off. Other regularizers, augmentations, and normalization layers have their own behavior and should not be treated as interchangeable.

**Keep this idea:** Regularization is a training choice; evaluation mode and gradient recording are separate execution choices that must match the purpose of each pass.

### Sources for this topic

- [PyTorch: Dropout — layer reference](https://docs.pytorch.org/docs/main/generated/torch.nn.Dropout.html)

- [PyTorch: Module — training and evaluation modes](https://docs.pytorch.org/docs/main/generated/torch.nn.Module.html)

- [PyTorch: Autograd mechanics — gradient and evaluation modes](https://docs.pytorch.org/docs/main/notes/autograd.html)

<a id="dl-convolution"></a>

## Convolutions and residual paths: local evidence, preserved routes

### 01 / The story

Jun photographs metal samples whose scratches can appear anywhere in the frame. A dense network treats each pixel position separately, so the same scratch shifted sideways looks unnecessarily different. He replaces the first transformation with a small sliding filter that reuses its weights across the surface. The model now has a direct way to detect the same local contrast at different positions. When Jun stacks many such transformations, training becomes harder, even though the model has more capacity. He adds a shortcut around a small group of layers, making the group learn a correction to the incoming features. His diagrams now distinguish two ideas: convolution shares a local detector across space, while a residual path preserves a direct route through a deeper computation.

### 02 / The concept

Convolutional layers combine nearby entries with shared weights, introducing a useful preference for repeated local patterns. The operation commonly called convolution in neural network libraries is cross correlation, without reversing the kernel. Stride, padding, and kernel size determine spatial output dimensions. Residual connections address a different concern: they add an incoming representation to a learned transformation of it. An identity shortcut requires equal shapes; a projection can reconcile different channel counts or spatial sizes. The addition creates another route for information and derivatives, but does not make arbitrary depth effortless to train.

### 03 / Put the concept to work

Use local filters when nearby structure and repeated spatial patterns are useful assumptions. Track the spatial size after every change in stride or padding. Before adding a residual branch, confirm that both branches agree in shape and feature alignment. Compare training and validation behavior separately: an optimization improvement from a shortcut does not by itself establish a gain on unseen images.

### 04 / How others use it

The original ResNet paper evaluates residual networks for image recognition and also uses their features in object detection experiments. It describes identity shortcuts and projections for mismatched dimensions. PyTorch’s Conv2d reference specifies the cross correlation operation and spatial sizing rules. Together they connect an implemented local operator with a documented architecture that places learned transformations alongside shortcut paths.

### 05 / The formula, unpacked

```text
Z[i,j] = b + Σ(u=0…k−1) Σ(v=0…k−1) K[u,v]X[i+u,j+v]
H_out = floor((H + 2p − k)/s) + 1
y = x + F(x;θ)
```

X is one input image channel, K is a square kernel of width k, b is a scalar bias, and Z is its output. i and j select an output location; u and v index kernel entries. The first equation assumes unit stride and no padding. H is input height, p is padding on each side, s is stride, and H_out is output height with unit dilation; floor rounds downward. In the residual equation, x and y are compatible feature tensors, F is the learned branch, and θ contains its parameters. Σ denotes summation.

### 06 / Work through the numbers

Let X = [[1, 0, 2], [2, 1, 0], [0, 3, 1]], K = [[1, 0], [0, −1]], and b = 0. With no padding and unit stride, the output height is floor((3−2)/1)+1 = 2, and the width is also 2. The four window calculations are 1−1 = 0, 0−0 = 0, 2−3 = −1, and 1−1 = 0. Thus Z = [[0, 0], [−1, 0]]. Separately, consider a residual input x = [2, −1] and a learned correction F(x;θ) = [0.5, 0.25]. Their sum is [2.5, −0.75]. If this block applies ReLU after the addition, its final output is [2.5, 0]. Distinguishing the sum from the subsequent activation prevents an incorrect shortcut calculation.

**Where the analogy stops:** Weight sharing does not create complete invariance to translation, rotation, or scale; boundaries and downsampling matter. A shortcut cannot add tensors whose dimensions or semantic alignment disagree. Residual networks still depend on suitable initialization, optimization, data, and capacity. The two dimensional toy filter here illustrates arithmetic, not a complete scratch detector.

**Keep this idea:** Convolution shares local evidence across positions; residual connections preserve a route around transformations. Their benefits come from different structural choices.

### Sources for this topic

- [PyTorch: Conv2d — convolution reference](https://docs.pytorch.org/docs/main/generated/torch.nn.Conv2d.html)

- [He et al. / arXiv: Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)

<a id="dl-attention"></a>

## Attention: retrieve context with learned comparisons

### 01 / The story

Amara builds a model for short maintenance notes. One note says a pump was replaced after a valve failed; another reverses which component failed. Averaging all word vectors makes the two notes frustratingly similar. She sketches a mechanism that lets each position ask for useful context instead of receiving the same pooled summary. A query compares against keys at other positions, and the resulting weights mix their value vectors. She then notices that the mechanism alone does not explain word order, so she adds positional information to the design. For a version that predicts the next word, she also blocks access to future positions. The model sketch becomes a Transformer only when this contextual mixing is combined with the surrounding feedforward, normalization, and residual components.

### 02 / The concept

Attention produces a weighted combination of value vectors using similarities between queries and keys. Scaled dot product attention divides those similarities by the square root of key dimension before normalization. A mask excludes connections that a task must not permit, such as future tokens in autoregressive prediction. Self attention obtains queries, keys, and values from the same sequence; cross attention can obtain them from different sequences. Multiple heads learn different projections. A Transformer additionally organizes attention with feedforward transformations, residual connections, normalization, and a way to represent position.

### 03 / Put the concept to work

Specify what each query may read before choosing an attention mask. Track query length, key length, and feature dimensions separately, especially in cross attention. Test a tiny case in which a forbidden position contains an extreme value; changing it should not change an output that cannot attend to it. Treat padding and causal restrictions as distinct masking requirements.

### 04 / How others use it

Vaswani and colleagues introduced the Transformer in Attention Is All You Need and evaluated it on machine translation. The original paper specifies scaled dot product attention, multiple heads, positional encodings, and masked decoder attention. This is a documented sequence modeling use of the mechanism. The maintenance narrative and numerical vectors here explain its operation without reproducing the paper’s experiments or claiming their results.

### 05 / The formula, unpacked

```text
S = QKᵀ/√dₖ + M
A[i,j] = exp(S[i,j]) / Σ(r=1…nₖ) exp(S[i,r])
O = AV
```

Q contains n_q query rows with dₖ features each. K contains nₖ key rows with the same dₖ features; Kᵀ is its transpose. V contains nₖ value rows with dᵥ features. S is the score matrix and M an additive mask, zero for allowed connections and negative infinity for blocked ones. A contains attention weights, and O contains n_q output rows with dᵥ features. i indexes queries; j and r index keys. exp is the exponential function, Σ sums over keys, and √dₖ is the positive square root. Each query must have an allowed key.

### 06 / Work through the numbers

Use one query Q = [[√2, 0]], two keys K = [[1, 0], [0, 1]], and values V = [[2, 0], [0, 4]]. The key dimension dₖ is 2. Before masking, scaled scores are [√2/√2, 0/√2] = [1, 0]. Softmax gives [exp(1)/(exp(1)+1), 1/(exp(1)+1)] ≈ [0.731059, 0.268941]. The output is therefore approximately [1.462117, 1.075766], a weighted combination of the two value vectors. If the second key is forbidden, use mask [0, −∞]. Its weight becomes zero and the first weight becomes one, yielding [2, 0]. The mask changes what information is available, not merely how strongly a forbidden position is preferred. These values describe one head before any output projection.

**Where the analogy stops:** Dense attention forms a score for every query and key pair, which can be costly for long sequences. Attention weights are not automatically faithful causal explanations. Missing positional information, incorrect masks, or entirely masked rows can invalidate an otherwise plausible computation. The small example omits learned projections and the other components needed for a complete Transformer.

**Keep this idea:** Attention chooses how to mix available context; dimensions, positional information, and masks determine what that choice can actually mean.

### Sources for this topic

- [Vaswani et al. / arXiv: Attention Is All You Need](https://arxiv.org/abs/1706.03762)

<a id="dl-transfer"></a>

## Transfer learning: adapt features without losing the evaluation boundary

### 01 / The story

Lina has a modest collection of microscope photographs from several specimen preparation sessions. Training a large image model from random weights quickly memorizes the available pictures. She tries a pretrained encoder and learns only a new classifier on top of its features. The first validation result looks excellent, until she notices that nearly identical photographs of the same specimen appear in both splits. Lina rebuilds the split by specimen and session, then establishes a more modest frozen encoder baseline. She next allows a small portion of the encoder to adapt, using validation results to choose whether the extra flexibility helps. A separate test set remains untouched. Her central decision is no longer simply which weights to unfreeze, but which evidence can fairly justify doing so.

### 02 / The concept

Transfer learning reuses parameters learned on an earlier task. A frozen encoder provides features while a new prediction head learns the target mapping. Fine tuning updates some or all encoder parameters as well. Success depends on how useful the inherited representation is for the new data and objective. Freezing parameter gradients does not automatically fix mutable layer state, such as batch normalization statistics. Validation guides architecture, hyperparameters, and checkpoint selection; a separate test set estimates performance after those choices are settled. Data grouping must reflect the dependence structure of the intended application.

### 03 / Put the concept to work

Begin with a frozen feature baseline and preprocessing compatible with the selected pretrained weights. Define train, validation, and test groups before tuning. When unfreezing layers, explicitly include their parameters in the optimizer and decide how normalization statistics should behave. Compare changes on the same validation protocol, record the selected checkpoint, and evaluate the held out test set only after model selection is complete.

### 04 / How others use it

PyTorch’s transfer learning tutorial adapts an ImageNet pretrained ResNet for classifying ants and bees. It demonstrates both fine tuning and a fixed feature extractor with a newly trained final layer. Its training function separates training and validation phases and retains the best validation checkpoint. These documented mechanics motivate the workflow here; the microscope story and binary head calculation are original examples.

### 05 / The formula, unpacked

```text
z = fθ(x), s = wᵀz + b, p = 1/(1+exp(−s))
L = −y log(p) − (1−y) log(1−p)
w_new = w − η(p−y)z
b_new = b − η(p−y)
θ_new = θ
```

x is an input and fθ is the pretrained encoder with parameters θ. z is its fixed feature column vector. w is the classifier’s weight vector, wᵀ is its transpose, b is its scalar bias, and s is the raw score. p is the sigmoid probability of class one; y is a binary target, either zero or one. L is binary cross entropy, log is the natural logarithm, and exp is the exponential. η is the learning rate. The new subscripts denote simultaneous updates; unchanged θ specifies a frozen encoder for this calculation.

### 06 / Work through the numbers

Suppose the frozen encoder returns z = [2, −1]. Start the head at w = [0.1, 0.2], b = 0, and use target y = 1. The raw score is 0.1×2 + 0.2×(−1) = 0, so p = 0.5 and L ≈ 0.693147. The weight gradient is (0.5−1)[2, −1] = [−1, 0.5], and the bias gradient is −0.5. With η = 0.1, the new weights are [0.2, 0.15] and the new bias is 0.05. The new score is 0.4 − 0.15 + 0.05 = 0.3. Thus p ≈ 0.574443 and L ≈ 0.554355. The encoder did not change. This lower loss on one training example says nothing by itself about whether fine tuning would improve independent validation data.

**Where the analogy stops:** Pretraining can transfer irrelevant features or biases, and aggressive fine tuning can erase useful ones. Repeated validation comparisons can overfit the validation set even without direct gradient updates. Small datasets leave substantial uncertainty. A frozen backbone also needs an explicit policy for running statistics and preprocessing; parameter freezing alone is not a complete reproducibility plan.

**Keep this idea:** Reuse useful representations, change only what evidence supports, and protect the validation and test boundaries that make adaptation claims credible.

### Sources for this topic

- [PyTorch: Transfer Learning for Computer Vision Tutorial](https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)

- [PyTorch: Module — training and evaluation modes](https://docs.pytorch.org/docs/main/generated/torch.nn.Module.html)

- [PyTorch: BatchNorm2d — running statistics reference](https://docs.pytorch.org/docs/main/generated/torch.nn.BatchNorm2d.html)

## The reference desk

### [Axis meaning comes first](#dl-tensors)

Record batch and feature axes before multiplication or reduction. Equal output sizes can hide entirely different computations.

### [Nonlinearity creates new representations](#dl-representations)

Hidden features help only when their transformations suit the task. Stacking affine layers without activations still produces one affine map.

### [Trace the backward path](#dl-autograd)

A plausible prediction can coexist with a broken gradient route. Check a small chain by hand before blaming the optimizer.

### [A learning rate is not a step size](#dl-optimization)

Averaging versus summing the loss and the optimizer’s state affect the update. Equal learning rates across SGD and Adam need not move weights equally.

### [Mode and gradients are separate](#dl-regularization)

Dropout changes behavior between training and evaluation. Evaluation mode does not disable autograd, and disabled autograd does not disable dropout.

### [Local filters and shortcuts solve different problems](#dl-convolution)

Convolution shares weights over local regions. A residual connection adds a compatible incoming representation to a learned correction.

### [Masks define available context](#dl-attention)

Attention mixes values according to query and key comparisons. Correct positions and masks are part of the model’s information boundary.

### [Adaptation needs independent evidence](#dl-transfer)

A frozen feature baseline makes adaptation measurable. Grouped splits, validation selection, and an untouched test set make the comparison credible.

## Official tutorials & original research

Original stories, explanations and examples by Guoliang. The linked tutorials and research belong to their respective authors; these independent companions are not official translations or endorsed courses.

- [Tensors — Learn the Basics](https://docs.pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html) — PyTorch

- [Build the Neural Network — Learn the Basics](https://docs.pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html) — PyTorch

- [Automatic Differentiation with torch.autograd](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html) — PyTorch

- [Optimizing Model Parameters — Learn the Basics](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html) — PyTorch

- [Adam — optimizer reference](https://docs.pytorch.org/docs/main/generated/torch.optim.Adam.html) — PyTorch

- [Dropout — layer reference](https://docs.pytorch.org/docs/main/generated/torch.nn.Dropout.html) — PyTorch

- [Module — training and evaluation modes](https://docs.pytorch.org/docs/main/generated/torch.nn.Module.html) — PyTorch

- [Conv2d — convolution reference](https://docs.pytorch.org/docs/main/generated/torch.nn.Conv2d.html) — PyTorch

- [Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385) — He et al. / arXiv

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — Vaswani et al. / arXiv

- [Transfer Learning for Computer Vision Tutorial](https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html) — PyTorch

- [Autograd mechanics — gradient and evaluation modes](https://docs.pytorch.org/docs/main/notes/autograd.html) — PyTorch

- [BatchNorm2d — running statistics reference](https://docs.pytorch.org/docs/main/generated/torch.nn.BatchNorm2d.html) — PyTorch
