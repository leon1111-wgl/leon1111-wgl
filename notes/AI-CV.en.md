# Computer Vision: From Pixels to Perception

> Guoliang | AI Field Guides

[EN](AI-CV.en.md) · [中文](AI-CV.zh.md)

Eight connected stories turn images into inspectable models: pixel contracts, local filters, geometry, recognition, detection, segmentation, visual tokens and reliable evaluation. Follow the calculations, then continue with official tutorials and original research.

## A route through the ideas

An original conceptual companion to official OpenCV and PyTorch materials, Stanford teaching and foundational vision research. Examples use synthetic numbers; this is a connected introduction, not a reproduction of a particular course or a production deployment manual.

### Before you start

- Basic arrays and Python-style indexing
- Vectors, matrix multiplication and simple probability
- The difference between training and evaluation

### What you will learn

- Trace an image through shape, scale and coordinate changes
- Choose classification, detection or segmentation for the actual question
- Read a convolution or patch model with explicit dimensions
- Evaluate performance without leaking related images

## Knowledge framework

### Represent and transform

- [Pixels are measurements with a contract](#pixels-contracts)
- [Local filters ask local questions](#filters-neighborhoods)
- [Move the picture and its meaning together](#geometry-augmentation)

### Recognize and locate

- [Borrow a visual vocabulary, then teach a new decision](#recognition-transfer)
- [Boxes locate candidates; overlap resolves duplicates](#detection-overlap)
- [From a rectangle to the pixels that belong](#segmentation-regions)

### Connect and evaluate

- [Let image patches exchange information](#visual-tokens)
- [Test on the next capture, not a familiar neighbour](#evaluation-shift)

<a id="pixels-contracts"></a>

## Pixels are measurements with a contract

### 01 / The story

Maya volunteers at a community archive that is digitizing painted theatre posters. One morning, every blue costume appears red in the new catalogue. The scanner seems fine, and the files open without errors, so the team initially suspects the display. Maya follows one known blue patch through the pipeline instead. The loader stores blue first, while the next component interprets the first channel as red. She writes down the channel order, array shape and numeric range at every boundary, corrects the conversion, and checks the same patch again. The costume returns to blue. The incident changes the team's routine: before asking whether a model understands a picture, they verify that each component receives the same picture. A pixel array needs a contract, just as a parcel needs a label that every handler interprets consistently.

### 02 / The concept

An image tensor is a numerical representation with spatial axes, channels, a data type and an intensity convention. A height-by-width RGB image and a channel-first batch encode related information in different layouts. Changing layout is not the same as swapping colour channels. Converting an unsigned byte to floating point also does not automatically scale its values. Preprocessing must match the model's expected channel order, range and normalization statistics. Coordinate indexing commonly uses row then column, whereas geometric points are often written as horizontal x then vertical y. These conventions must be explicit wherever data crosses a boundary.

### 03 / Put the concept to work

Start a vision pipeline with a tiny diagnostic image whose colours and locations you know. Inspect shape, type, minimum and maximum values, and one selected pixel after each conversion. Apply normalization using the statistics specified by the pretrained weights, or training-only estimates when designing your own pipeline. Keep the unmodified input available so that visualization does not accidentally display standardized values as ordinary colours.

### 04 / How others use it

OpenCV's Basic Operations on Images tutorial makes pixel access, array properties and channel manipulation visible rather than treating an image as an opaque file. TorchVision's transforms documentation explains transformations across images and structured targets. Together they illustrate the practical boundary that the archive story exposes: representation choices are part of the computation, and must remain consistent before learned inference begins.

### 05 / The formula, unpacked

```text
z = (v / 255 − μ) / σ
HWC → CHW: (H, W, C) → (C, H, W)
```

v is an eight-bit channel value between zero and 255. Dividing by 255 maps it to the unit interval; μ and σ are the chosen mean and positive standard deviation on that same scale. z is the standardized value and can be negative. H, W and C denote height, width and channel count. HWC and CHW describe axis order only, not whether the channels mean red, green or blue. This equation assumes the stated byte scale; a floating image already in the unit interval should not be divided again.

### 06 / Work through the numbers

Use a synthetic channel value v = 153 with μ = 0.5 and σ = 0.25. First scale: 153 / 255 = 0.6. Then centre: 0.6 − 0.5 = 0.1. Finally divide by the standard deviation: z = 0.4. If the value 0.6 had already been scaled, another division by 255 would instead produce approximately −1.9906 after standardization. The shape offers a separate check: a 4-by-6 RGB image has shape (4, 6, 3), and moving its channel axis first gives (3, 4, 6), still containing 72 numbers. Neither operation by itself converts BGR to RGB. Compare both numeric values and channel semantics before declaring the input correct.

**Where the analogy stops:** The parcel-label analogy explains interface agreement, not colour science. Camera response, gamma encoding and illumination also affect pixels. Correct shapes and ranges cannot prove that an image represents the same physical scene under different capture conditions; they only eliminate a useful class of avoidable errors.

**Keep this idea:** Before learning from pixels, establish their axes, colour meaning, scale and normalization contract at every boundary.

### Sources for this topic

- [OpenCV: Basic Operations on Images](https://docs.opencv.org/4.x/d3/df2/tutorial_py_basic_ops.html)

- [TorchVision: Transforming images, videos, boxes and more](https://docs.pytorch.org/vision/stable/transforms.html)

<a id="filters-neighborhoods"></a>

## Local filters ask local questions

### 01 / The story

Jon is restoring a scanned star chart for a small observatory. Dust from the scanner produces bright specks, but faint pencil lines mark the constellations. His first repair replaces each pixel by a neighbourhood average. The specks soften, yet some important pencil lines disappear too. Instead of declaring the repair successful because the image looks smoother, Jon compares a few known lines and blank regions. He uses a smaller smoothing window where appropriate and keeps an edge response alongside the original image to inspect changes. The restored chart is useful because he has chosen a local question rather than a universal beautification rule. A neighbourhood filter resembles a committee listening to nearby witnesses: averaging can reduce isolated noise, but a majority can also erase a rare observation that matters.

### 02 / The concept

A linear image filter computes a weighted sum of nearby values at each location. A normalized averaging kernel smooths variation, while kernels with positive and negative coefficients respond to changes. Applying one kernel repeatedly across an image shares the same local operation spatially. Boundary padding determines what happens when part of the neighbourhood lies outside the image. Many software operations described casually as convolution actually compute cross-correlation, without flipping the kernel. For symmetric averaging kernels the results coincide, but directional filters can change sign or orientation under a flip.

### 03 / Put the concept to work

Specify the question before choosing a filter: suppress isolated noise, estimate a gradient, or prepare an image for a downstream task. Inspect representative boundaries as well as flat areas, record the padding rule, and retain a floating-point output when negative responses matter. Compare downstream accuracy or annotation quality rather than assuming that visual smoothness is automatically an improvement.

### 04 / How others use it

OpenCV's Smoothing Images tutorial presents several neighbourhood filters, while its filter2D reference specifies the correlation convention used by that operation. These are useful complementary sources: the tutorial explains the workflow and the reference resolves an implementation detail. Learned convolutional networks extend the shared-local-operation idea by fitting many kernels from data, although training and nonlinear layers make them much more than fixed smoothing filters.

### 05 / The formula, unpacked

```text
y[r,c] = Σ_i Σ_j K[i,j] x[r+i,c+j]
Mean kernel: K[i,j] = 1 / (k²)
```

x is the input intensity array and y is the output. r and c identify the output location. i and j run over the kernel's neighbourhood offsets; K supplies the weight at each offset. The displayed convention is cross-correlation. For a square k-by-k mean filter, each of its k² weights equals 1/k² and their sum is one. The formula does not specify how out-of-bounds values are supplied, so padding must be stated separately. With multiple channels, filtering can operate independently per channel or also sum across them, depending on the layer.

### 06 / Work through the numbers

Consider a 3-by-3 patch with eight entries equal to 10 and a centre entry equal to 19. A uniform mean filter gives (8 × 10 + 19) / 9 = 11 at the centre. The bright speck is reduced, but not removed without consequence: a genuine isolated star would also be weakened. For a separate one-dimensional edge probe, apply the correlation kernel [−1, 0, 1] to [2, 5, 8]. The response is −2 + 0 + 8 = 6. Reversing the input order gives −6. Taking an unsigned output carelessly could hide the negative response. These two calculations answer different questions, so choose and evaluate them according to the information you need to preserve.

**Where the analogy stops:** Neighbouring witnesses can share the same mistake. Averaging cannot recover details already absent from the measurement, and strong smoothing can damage boundaries. An edge response identifies local intensity change, not a semantic object boundary: shadows, texture and sensor noise can all generate responses.

**Keep this idea:** A filter is a local question expressed as weights; evaluate what it preserves as carefully as what it removes.

### Sources for this topic

- [OpenCV: Smoothing Images](https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html)

- [OpenCV: Image filtering: filter2D](https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html)

<a id="geometry-augmentation"></a>

## Move the picture and its meaning together

### 01 / The story

Lina builds a small camera system to recognize tools on a workshop wall. It performs well until the camera is mounted higher and the tools appear at unfamiliar positions. She decides to train with translated and resized images. At first, she moves the pictures but leaves the annotated rectangles untouched; the new training set now teaches the model that the hammer is somewhere else. A side-by-side overlay reveals the mistake immediately. Lina makes each transformation operate on the image and its labels together, then rejects crops that remove the object completely. Recognition improves on a held-out camera position. Her lesson is about shared geometry: moving a theatre stage while leaving the actors' floor marks fixed creates confusion, even when both the stage and the marks are individually well made.

### 02 / The concept

A geometric transform maps coordinates from one reference frame into another. Translation changes position, scaling changes extent, and affine maps can combine translation with linear transformations. Rendering transformed images usually samples the source through an inverse mapping, using interpolation for noninteger coordinates. Data augmentation uses selected transforms to express variations that should preserve the target meaning. That assumption depends on the task: a horizontal flip may preserve a tool category but change a left-pointing arrow's label. Bounding boxes, masks and keypoints require coordinated transformations, not merely the same output image dimensions.

### 03 / Put the concept to work

Write down which variations are plausible in the intended camera setting and which annotations must change with them. Preview augmented samples with boxes and masks overlaid, including extreme crops and border cases. Apply randomness only in the training pipeline; use a defined evaluation transform. Keep related frames within one split so augmentation does not disguise leakage between training and evaluation.

### 04 / How others use it

OpenCV's Geometric Transformations tutorial connects coordinate maps with image resampling. TorchVision's transforms documentation demonstrates why images, boxes, masks and videos need compatible operations. In the official TorchVision detection tutorial, image and target transformations are part of preparing training data. These sources motivate the workshop workflow without suggesting that every transformation is valid for every detection task or label vocabulary.

### 05 / The formula, unpacked

```text
[x′, y′, 1]ᵀ = [[sₓ, 0, tₓ], [0, sᵧ, tᵧ], [0, 0, 1]] [x, y, 1]ᵀ
x′ = sₓx + tₓ; y′ = sᵧy + tᵧ
```

x and y are horizontal and vertical coordinates in the original frame; primed coordinates belong to the transformed frame. sₓ and sᵧ are scale factors, while tₓ and tᵧ are translations measured in output-coordinate units. The appended one allows translation to appear inside matrix multiplication; the superscript T denotes a column vector. This restricted affine map contains scaling and translation, not rotation or perspective. For positive scales, transform both corners of an axis-aligned box; more general transformations require considering all corners and the intended output representation.

### 06 / Work through the numbers

A synthetic tool box has corners (10, 20) and (30, 50). Choose sₓ = sᵧ = 2, tₓ = 5 and tᵧ = −3. The first corner becomes (2 × 10 + 5, 2 × 20 − 3) = (25, 37). The second becomes (65, 97). Width changes from 20 to 40 and height from 30 to 60, so area changes from 600 to 2400 square coordinate units. Translation changes neither width nor area. If the output canvas ends at y = 80, the box extends beyond it; clipping and the retained-object rule must now be applied consistently. Updating only the pixels would leave the original box at an unrelated location.

**Where the analogy stops:** The moving-stage analogy does not guarantee that identity survives a transformation. Cropping can remove decisive evidence, and interpolation can change small patterns. Augmentation improves robustness only to useful, label-consistent variation; it cannot substitute for representative real images from the intended environment.

**Keep this idea:** Every geometric change must carry its targets along, and every augmentation must justify why the label still means the same thing.

### Sources for this topic

- [OpenCV: Geometric Transformations of Images](https://docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html)

- [TorchVision: Transforming images, videos, boxes and more](https://docs.pytorch.org/vision/stable/transforms.html)

- [PyTorch: TorchVision Object Detection Finetuning Tutorial](https://docs.pytorch.org/tutorials/intermediate/torchvision_tutorial.html)

<a id="recognition-transfer"></a>

## Borrow a visual vocabulary, then teach a new decision

### 01 / The story

A community garden asks Noor to sort camera images into three plant categories. She has only a small labelled collection, so training a large recognition model from random weights produces unstable results. Noor instead starts with a network that has already learned reusable visual patterns from other images. She freezes its feature extractor and trains a small new decision layer. The first results improve, but close inspection shows mistakes under the garden's unusual evening lighting. She then cautiously fine-tunes selected layers using a lower learning rate and keeps a separate set of garden visits for evaluation. The process resembles hiring an experienced illustrator to learn a new field guide: drawing experience transfers, but the illustrator still needs local examples, clear categories and an honest check of unfamiliar pages.

### 02 / The concept

A classifier maps an image to scores for a defined set of classes. A feature extractor converts pixels into a representation, and a prediction head turns that representation into class logits. Transfer learning reuses pretrained parameters instead of learning every feature from scratch. A frozen backbone updates no backbone parameters; fine-tuning updates some or all of them under the new objective. Softmax converts logits into a normalized distribution over the provided classes. Its largest value is not a guarantee that the predicted label is correct, especially for inputs unlike the training distribution.

### 03 / Put the concept to work

Begin with a simple frozen-feature baseline, match the pretrained preprocessing, and replace the head to match your own label set. Split by capture session or source when neighbouring images are related. Compare fine-tuning against that baseline using the same held-out groups. Inspect mistakes by lighting and viewpoint, and reserve enough evaluation data to notice when an apparently better model has merely memorized local patterns.

### 04 / How others use it

PyTorch's official Transfer Learning for Computer Vision tutorial contrasts adapting a pretrained network with using it as a fixed feature extractor. Stanford's CS231n teaching provides a broader account of learned visual representations and recognition. Noor's three-category garden example is original; the connection is the reusable workflow of adapting a learned representation and testing whether that adaptation actually generalizes to new images.

### 05 / The formula, unpacked

```text
h = fθ(x); z = Wh + b
pₖ = exp(zₖ) / Σⱼ exp(zⱼ)
L = −log(pᵧ)
```

x is an input image, fθ is a feature extractor with parameters θ, and h is its feature vector. W and b are the new head's weight matrix and bias. z contains one unnormalized logit per class; k and j index classes. pₖ is the corresponding softmax value. y denotes the correct class, and L is the negative log-likelihood for one labelled image. The logarithm is natural. With a frozen backbone, optimization changes W and b but leaves θ fixed; fine-tuning permits selected components of θ to change as well.

### 06 / Work through the numbers

For a transparent toy calculation, let h = [1, 2], set the three rows of W to [1, 0], [0, 1] and [0, 0], and use zero biases. The logits are [1, 2, 0]. Exponentiating gives approximately [2.7183, 7.3891, 1], whose sum is 11.1073. The class probabilities are therefore approximately [0.2447, 0.6652, 0.0900]. If the second class is correct, the loss is −log(0.6652), approximately 0.4076. The model predicts that class, yet still incurs loss because it assigns some probability elsewhere. This demonstrates the head calculation, not the millions of computations that created a realistic image representation. Test new images before interpreting a low training loss as useful recognition.

**Where the analogy stops:** The experienced-illustrator analogy can overstate what transfers. Pretraining may encode irrelevant shortcuts, and a confident softmax can still choose the wrong class. Frozen features are a useful baseline rather than a universal solution; the appropriate adaptation depends on dataset size, similarity and evaluation evidence.

**Keep this idea:** Transfer a representation, define the new decision carefully, and measure improvement on genuinely separate image groups.

### Sources for this topic

- [PyTorch: Transfer Learning for Computer Vision](https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)

- [Stanford University: CS231n: Deep Learning for Computer Vision](https://cs231n.stanford.edu/2025/schedule.html)

<a id="detection-overlap"></a>

## Boxes locate candidates; overlap resolves duplicates

### 01 / The story

Eli records seabird observations from a coastal hide. His detector reports seven gulls in a photograph where he can identify four. The overlay reveals several slightly different rectangles around the same bird, so simply counting predictions inflates the observation. Eli sorts candidates by score and removes strongly overlapping alternatives within the gull class. The count now agrees on this photograph. However, a second picture contains two birds standing close together, and an aggressive overlap threshold removes a real neighbour. He compares several thresholds on separately labelled images and keeps crowded scenes visible in the error review. The useful result is a defined counting procedure with known failures. Rectangles are proposed locations, like several pencil circles drawn around the same landmark; reconciling circles requires a rule, but the rule cannot see the landmark itself.

### 02 / The concept

Object detection predicts class labels, scores and locations for individual candidates. Intersection over union, or IoU, measures the overlap between two regions relative to their union; it is a geometric ratio, not classification accuracy. Greedy non-maximum suppression first keeps the highest-scoring remaining box, then removes lower-scoring boxes whose IoU with it exceeds a threshold, and repeats. Here suppression operates separately within each class. TorchVision's basic NMS operation receives no class labels, so that separation must be arranged by the caller. A suppression threshold and an evaluation matching threshold serve different purposes even when both use IoU.

### 03 / Put the concept to work

Define box coordinates and class handling before comparing detections. Inspect overlays containing isolated objects, crowded neighbours and partial occlusions. Choose score and suppression thresholds using validation data, then keep them fixed for the final evaluation. Record how predictions match annotations, including the rule preventing multiple predictions from claiming the same object. A plausible-looking box is evidence to inspect, not proof that the object count is correct.

### 04 / How others use it

The official TorchVision detection tutorial fine-tunes Mask R-CNN on Penn-Fudan pedestrian images, using boxes, labels and object masks as structured targets. The NMS reference separately documents score ordering and removal when overlap is strictly greater than the supplied threshold. Reading both distinguishes a complete detection example from one postprocessing operation, and makes the seabird story's duplicate-removal decision precise.

### 05 / The formula, unpacked

```text
IoU(A, B) = |A ∩ B| / (|A| + |B| − |A ∩ B|)
|A| = (x₂ − x₁)(y₂ − y₁)
score(B) < score(A) ∧ IoU(A, B) > τ ⇒ B ∉ K
```

A is a kept box and B is a lower-scoring candidate of the same class. Vertical bars denote continuous area, and ∩ denotes intersection. The coordinates (x₁, y₁) and (x₂, y₂) are A's opposite corners, with increasing horizontal and vertical coordinates. Area uses coordinate differences without an inclusive-pixel plus one. Both boxes have positive area. score assigns the ranking value, and τ is the chosen IoU suppression threshold. The displayed rule assumes unequal scores; a tie needs an implementation-specific selection rule. IoU ranges from zero to one. K is the retained set; ∧ means both conditions hold and ⇒ implies exclusion of B.

### 06 / Work through the numbers

Consider three synthetic gull boxes: A = (0, 0, 4, 4), B = (1, 1, 5, 5), and C = (6, 0, 8, 2), with scores 0.9, 0.8 and 0.7. A and B each have area 16. Their intersection has width 3 and height 3, hence area 9. Their union is 16 + 16 − 9 = 23, giving IoU = 9 / 23, approximately 0.3913. At τ = 0.3, keep A and suppress B. C does not overlap A, so keep C: two boxes remain. At τ = 0.5, B also remains, giving three boxes. These results demonstrate threshold mechanics; without annotations they cannot tell whether A and B describe one gull or two overlapping gulls.

**Where the analogy stops:** The pencil-circle analogy explains duplicate proposals, but high overlap does not prove shared identity. Greedy suppression can remove real neighbours, and a high score can belong to an inaccurate box. Different detectors may use other duplicate-handling designs; the rule here describes a common operation, not every detection architecture.

**Keep this idea:** Treat boxes as candidates, define overlap precisely, and validate duplicate removal separately from the rule used to judge detection quality.

### Sources for this topic

- [PyTorch: TorchVision Object Detection Finetuning Tutorial](https://docs.pytorch.org/tutorials/intermediate/torchvision_tutorial.html)

- [TorchVision: Non-maximum suppression](https://docs.pytorch.org/vision/stable/generated/torchvision.ops.nms.html)

<a id="segmentation-regions"></a>

## From a rectangle to the pixels that belong

### 01 / The story

Priya helps a river group compare photographs of floating leaves in a shallow observation tray. Bounding boxes locate each leaf, but they also include water, so adding box areas exaggerates leaf coverage. She switches to masks that label leaf pixels and measures the combined foreground region. That answers the coverage question until another volunteer asks how many leaves are present. Two touching leaves form one connected region, showing that a shared category mask does not preserve individual identity. Priya prepares separate instance annotations for counting and keeps the semantic mask for coverage. She also replaces overall pixel accuracy with foreground overlap because most tray pixels are water. The group now has two explicit questions and two suitable outputs, rather than one impressive number that silently answers the wrong question.

### 02 / The concept

Semantic segmentation assigns a class to each pixel; all leaves can share one class regardless of individual identity. Instance segmentation distinguishes separate objects as well as their pixels. A binary foreground mask can be compared with its reference using IoU or Dice overlap. Neither metric rewards correctly predicted background pixels directly, making the foreground comparison informative when background dominates. Dice counts the shared foreground twice and divides by the sum of mask sizes. These hard-mask metrics differ from differentiable training losses that may use probabilities, smoothing or other reductions. Specify which version and averaging convention you report.

### 03 / Put the concept to work

Choose semantic labels when the question concerns material coverage, and instance labels when separate objects matter. Overlay masks on originals to inspect boundaries and small regions. Keep foreground overlap alongside class frequencies and representative mistakes, and document whether scores average over images, objects or classes. Define empty-mask handling before evaluation, so images without foreground do not silently change the meaning of the reported average.

### 04 / How others use it

TorchVision documents an FCN model with a ResNet-50 backbone for semantic segmentation. Its detection tutorial instead uses Mask R-CNN and Penn-Fudan annotations to distinguish individual pedestrians and their masks. These are concrete examples of the two output types. The scikit-learn metrics guide supplies the related Jaccard and F-measure definitions, which can be applied to flattened binary pixel labels under an explicit foreground convention.

### 05 / The formula, unpacked

```text
IoU = |P ∩ G| / |P ∪ G|
Dice = 2|P ∩ G| / (|P| + |G|)
Dice = 2IoU / (1 + IoU)  (|P ∪ G| > 0)
```

P is the set of pixels predicted as foreground, and G is the reference foreground set. Vertical bars count pixels; ∩ selects pixels in both sets, while ∪ selects pixels in either set. IoU means intersection over union, and Dice is the overlap coefficient defined above. Both lie between zero and one when the denominator is positive. If both masks are empty, these raw fractions are undefined; choose and report a convention such as scoring agreement as one or excluding that case from a specified average.

### 06 / Work through the numbers

Use a synthetic image with 1000 pixels and 40 reference leaf pixels. An all-background prediction achieves 960 / 1000 = 96% pixel accuracy, yet foreground IoU and Dice are both zero because it finds no leaf pixels. A second prediction marks 50 pixels as leaves, with 30 correctly overlapping the reference. The union contains 50 + 40 − 30 = 60 pixels, so IoU = 30 / 60 = 0.5. Dice = 60 / 90, approximately 0.6667, matching 2 × 0.5 / 1.5. There are 20 false foreground pixels and 10 missed leaf pixels. The two overlap scores describe the same masks on different scales; neither should be compared numerically with pixel accuracy as if they measured the same quantity.

**Where the analogy stops:** A coloured region is only as meaningful as its annotation rules. Ambiguous boundaries, transparent objects and overlapping instances may require careful conventions. High average overlap can still hide missed tiny objects or important boundary errors, and foreground area alone cannot establish the number of individual objects.

**Keep this idea:** Match the mask to the question, inspect minority foreground, and state exactly how overlap and empty cases are scored.

### Sources for this topic

- [TorchVision: FCN with a ResNet-50 backbone](https://docs.pytorch.org/vision/stable/models/generated/torchvision.models.segmentation.fcn_resnet50.html)

- [PyTorch: TorchVision Object Detection Finetuning Tutorial](https://docs.pytorch.org/tutorials/intermediate/torchvision_tutorial.html)

- [scikit-learn: Metrics and scoring: quantifying prediction quality](https://scikit-learn.org/stable/modules/model_evaluation.html)

<a id="visual-tokens"></a>

## Let image patches exchange information

### 01 / The story

Mateo is building a teaching display that sorts photographs of handmade kites by their overall design. A stripe near one corner matters only in relation to the tail, so he wants to understand how a model can connect distant image regions. He draws a grid over each photograph and treats every square as a short numerical description. A transformer can let these descriptions exchange information before the final decision. Mateo initially assumes that halving the square width only doubles the work. Counting the grid changes his mind: there are four times as many patches, and many more pairs can interact. He keeps the first display small and shows the token count beside each image. The display now explains both the model's reach across the picture and the computational price of finer visual pieces.

### 02 / The concept

The original Vision Transformer divides an image into nonoverlapping patches, flattens each patch and applies a shared learned linear projection. Position embeddings preserve information about where tokens occur. A learned class token joins the sequence, and its final representation supports image classification. Self-attention allows tokens to combine information from other tokens. For full attention, the number of token pairs grows quadratically with sequence length. This describes an attention component, not a universal scaling law for total runtime: projections, other layers, hardware and implementation details also contribute. Patches are numerical units, not necessarily recognizable objects.

### 03 / Put the concept to work

Before choosing image resolution and patch size, calculate the patch count and the sequence length including special tokens. Check whether the image dimensions divide evenly or require an explicit resizing or padding policy. Compare detail retention against measured resource use, and preserve the pretrained model's positional handling. For a new task, inspect whether useful evidence is lost during resizing before attributing every error to attention.

### 04 / How others use it

The original ViT paper demonstrates image classification by combining projected patches with a transformer encoder and studies transfer after large-scale pretraining. TorchVision's VisionTransformer implementation makes patch projection and the added class token inspectable. The original Transformer paper explains the attention operation underlying this exchange. These sources support the design being illustrated; the handmade-kite display and its small numerical example are original teaching scenarios.

### 05 / The formula, unpacked

```text
N = (H / P)(W / P); L = N + 1
xᵢ ∈ ℝ^(P²C); E ∈ ℝ^(D × P²C); tᵢ = Exᵢ + eᵢ
S = L²
```

H and W are image height and width; P is square patch width, assumed to divide both. C is channel count, N is patch count, and L includes one class token. xᵢ is flattened patch i as a column vector. ℝ denotes real-valued entries. E projects it into D embedding dimensions; eᵢ is its positional vector and tᵢ the resulting patch token. This simplified expression omits projection bias. S counts token-pair score entries per full-attention head, not total operations or guaranteed allocated memory.

### 06 / Work through the numbers

Take a synthetic 32-by-32 RGB image and square patches of width 8. There are (32 / 8)² = 16 patches. Each patch contains 8² × 3 = 192 values. With embedding width D = 64, the projection matrix has shape 64 by 192 and produces one vector of 64 numbers per patch. Adding one class token gives L = 17 and S = 17² = 289 token-pair scores per head. Halving patch width to 4 produces 64 patches, L = 65 and S = 4225. The score count rises by 4225 / 289, approximately 14.62 times, rather than exactly sixteen because of the class token. This comparison fixes image size and embedding width; it does not predict an equal increase in complete model runtime.

**Where the analogy stops:** The exchange-of-descriptions analogy does not mean tokens reason like people or that attention weights explain every decision. The simplified arithmetic concerns ordinary full attention with fixed embedding width. Other architectures can use windows, pooling or different token designs, and finer patches alone do not guarantee better recognition.

**Keep this idea:** Count patches and special tokens explicitly: finer visual units increase possible interactions, while useful detail and actual runtime still require measurement.

### Sources for this topic

- [Dosovitskiy et al.: An Image is Worth 16x16 Words](https://arxiv.org/abs/2010.11929)

- [TorchVision: VisionTransformer implementation](https://docs.pytorch.org/vision/stable/_modules/torchvision/models/vision_transformer.html)

- [Vaswani et al.: Attention Is All You Need](https://arxiv.org/abs/1706.03762)

<a id="evaluation-shift"></a>

## Test on the next capture, not a familiar neighbour

### 01 / The story

Hana volunteers with a wildlife group whose cameras produce bursts of nearly identical photographs. A randomly shuffled evaluation looks excellent, but predictions deteriorate when the camera moves to a shaded trail. She discovers that neighbouring burst frames appeared in both training and evaluation, letting familiar backgrounds and animals cross the boundary. Hana rebuilds the split around capture groups and reserves a camera location for a separate shift check. The scores fall, yet the mistakes become useful: dark empty frames trigger false wildlife alerts, while small distant animals are missed. She reports precision and recall with the number of evaluated examples, then collects representative shaded-trail images for a later development cycle. The lower score gives the group a clearer picture of what the model can do when the next photograph is genuinely new.

### 02 / The concept

Evaluation estimates performance under a defined sampling process. Related frames, repeated subjects or shared capture sessions can leak information when split independently. Grouping them keeps the chosen source of dependence within one partition; the group definition should match the intended generalization question. Domain shift occurs when deployment images differ from development data, for example in camera location or illumination. Precision measures how many predicted positives are correct, while recall measures how many actual positives are found. Neither substitutes for checking groups, label quality, sample counts or the operational decision threshold.

### 03 / Put the concept to work

Write the future-use question before constructing a split: new frames from familiar cameras, new sessions, or new locations require different evidence. Group related captures accordingly and preserve a final test set. Select thresholds on validation data, inspect errors by relevant conditions, and report both aggregate and group-level counts. Treat a new environment as something to measure explicitly rather than assuming one pooled score transfers unchanged.

### 04 / How others use it

The WILDS research benchmark includes wildlife monitoring shifts across camera traps, giving a documented example of why image source matters. Scikit-learn's GroupKFold documentation shows how group identities can remain separate across training and test folds. Its evaluation guide defines precision and recall. These sources motivate capture-aware evaluation; a grouped split alone does not establish robustness to every future camera or season.

### 05 / The formula, unpacked

```text
Precision = TP / (TP + FP)
Recall = TP / (TP + FN)
F₁ = 2TP / (2TP + FP + FN)
```

TP counts positive examples correctly predicted positive, FP counts negative examples incorrectly predicted positive, and FN counts positive examples incorrectly predicted negative. Here an example is one image and positive means wildlife is present; these are not pixel counts or matched detection boxes. Precision and recall use the displayed denominators, and F₁ combines them through their harmonic mean when defined. Scores assume a fixed decision threshold. If a denominator is zero, report the chosen undefined-case convention and the underlying counts instead of silently inventing a value.

### 06 / Work through the numbers

Suppose a synthetic held-out group contains 100 images: 20 show wildlife and 80 are empty. At the chosen threshold, the model flags 25 images. Of these, 15 contain wildlife, so TP = 15 and FP = 10. It misses five wildlife images, giving FN = 5. Precision is 15 / 25 = 0.60, recall is 15 / 20 = 0.75, and F₁ is 30 / 45, approximately 0.6667. The remaining 70 empty images are correctly rejected. Overall accuracy is therefore 85 / 100 = 85%, but that number alone hides the ten false alerts and five misses. These counts describe this sampled group at this threshold, not a guarantee about an unseen camera location.

**Where the analogy stops:** The unfamiliar-photograph analogy helps expose leakage, but novelty has several dimensions. Separate sessions may still share the same camera background, and new locations can change class frequencies. Small evaluation groups produce uncertain estimates; always retain sample counts and avoid interpreting a single split as a universal performance certificate.

**Keep this idea:** A trustworthy vision score names its population, separates related captures, and reveals the false positives and missed positives behind the average.

### Sources for this topic

- [scikit-learn: Metrics and scoring: quantifying prediction quality](https://scikit-learn.org/stable/modules/model_evaluation.html)

- [scikit-learn: GroupKFold: cross-validation with non-overlapping groups](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html)

- [Koh et al.: WILDS: A Benchmark of in-the-Wild Distribution Shifts](https://arxiv.org/abs/2012.07421)

## The reference desk

### [Trace one pixel](#pixels-contracts)

Follow a known colour through channel order, axis layout, scaling and normalization. A valid shape does not guarantee a valid colour interpretation.

### [Name the local question](#filters-neighborhoods)

Explain which variation a filter should suppress or reveal. Check kernel orientation and boundary handling before judging whether smoothing preserves useful evidence.

### [Move the annotation too](#geometry-augmentation)

Transform images and targets together. Recalculate the box corners, then check clipping and whether the transformed image still supports its original label.

### [Separate features from decisions](#recognition-transfer)

Identify the reused backbone and new prediction head. State which parameters can change, and compare adaptation on independent capture groups.

### [Compute overlap before suppressing](#detection-overlap)

For the two area-16 boxes, intersection 9 gives IoU 9/23. A threshold of 0.3 suppresses the lower-scoring same-class box; 0.5 retains it.

### [Challenge background-heavy accuracy](#segmentation-regions)

An all-background mask can score 96% accuracy while finding no foreground. Explain semantic versus instance outputs, then state overlap averaging and empty-mask conventions.

### [Count the extra token](#visual-tokens)

Sixteen image patches plus one class token produce 17 tokens and 289 pairwise scores per full-attention head. Pair counts alone do not determine runtime.

### [Name the next image population](#evaluation-shift)

Choose groups that match the future-use question. Report the evaluated counts behind precision and recall, and inspect performance when camera conditions change.

## Official tutorials & original research

Original stories, explanations and examples by Guoliang. The linked tutorials and research belong to their respective authors; these independent companions are not official translations or endorsed courses.

- [Basic Operations on Images](https://docs.opencv.org/4.x/d3/df2/tutorial_py_basic_ops.html) — OpenCV

- [Smoothing Images](https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html) — OpenCV

- [Image filtering: filter2D](https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html) — OpenCV

- [Geometric Transformations of Images](https://docs.opencv.org/4.x/da/d6e/tutorial_py_geometric_transformations.html) — OpenCV

- [Transfer Learning for Computer Vision](https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html) — PyTorch

- [TorchVision Object Detection Finetuning Tutorial](https://docs.pytorch.org/tutorials/intermediate/torchvision_tutorial.html) — PyTorch

- [Non-maximum suppression](https://docs.pytorch.org/vision/stable/generated/torchvision.ops.nms.html) — TorchVision

- [FCN with a ResNet-50 backbone](https://docs.pytorch.org/vision/stable/models/generated/torchvision.models.segmentation.fcn_resnet50.html) — TorchVision

- [Transforming images, videos, boxes and more](https://docs.pytorch.org/vision/stable/transforms.html) — TorchVision

- [CS231n: Deep Learning for Computer Vision](https://cs231n.stanford.edu/2025/schedule.html) — Stanford University

- [An Image is Worth 16x16 Words](https://arxiv.org/abs/2010.11929) — Dosovitskiy et al.

- [Metrics and scoring: quantifying prediction quality](https://scikit-learn.org/stable/modules/model_evaluation.html) — scikit-learn

- [VisionTransformer implementation](https://docs.pytorch.org/vision/stable/_modules/torchvision/models/vision_transformer.html) — TorchVision

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — Vaswani et al.

- [GroupKFold: cross-validation with non-overlapping groups](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html) — scikit-learn

- [WILDS: A Benchmark of in-the-Wild Distribution Shifts](https://arxiv.org/abs/2012.07421) — Koh et al.
