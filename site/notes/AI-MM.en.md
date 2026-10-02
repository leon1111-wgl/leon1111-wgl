# Multimodal AI

> Guoliang | AI Field Guides

[EN](AI-MM.en.md) · [中文](AI-MM.zh.md)

An original field guide to how models connect different kinds of observations. Follow eight complete stories from representation to grounded evaluation, then unpack the mechanisms, calculations, research uses, and limits behind each story.

## A route through the ideas

Eight connected topics spanning image–text alignment, contrastive learning, fusion, conditional generation, visual instruction tuning, audio, video, and evidence-aware evaluation.

### Before you start

- Vectors, dot products, and basic probability
- Neural-network training and cross-entropy
- A first introduction to transformers and attention

### What you will learn

- Distinguish shared representations, fusion, and generation
- Calculate similarity, attention, conditional loss, and temporal overlap
- Explain the original CLIP, LLaVA, BLIP-2, Whisper, and CLAP design choices
- Evaluate visual claims against observations and state what remains uncertain

## Knowledge framework

### Represent and align

- [Different observations, a shared coordinate system](#modalities-alignment)
- [CLIP: learn by choosing the right partner](#clip-contrastive)

### Fuse and respond

- [Cross-attention: ask one stream to inspect another](#cross-attention-fusion)
- [Captioning and VQA: generate under visual conditions](#conditional-generation)
- [Visual instruction tuning: connect perception to a request](#visual-instruction-tuning)

### Listen and follow time

- [Audio and text: hearing words is one of several tasks](#audio-text-alignment)
- [Video: what happened, and when did it happen?](#video-temporal-grounding)

### Check the evidence

- [Evaluation: fluent claims still need observable support](#evaluation-hallucination)

<a id="modalities-alignment"></a>

## Different observations, a shared coordinate system

### 01 / The story

At Harbor Museum, curator Lin inherited two archives after a storage move: photographs of objects and handwritten descriptions. Their identification numbers had been lost. Searching for the word compass found descriptions, but the photographs contained no searchable words. Lin first asked volunteers to assign separate labels to each archive. That failed when one person wrote navigation instrument and another wrote brass dial. She then assembled a small collection of confirmed photograph–description pairs and used them to organize both archives around shared meanings. A photograph could now lead to nearby descriptions, including ones using unfamiliar vocabulary. Volunteers still inspected the suggested matches and rejected a decorative clock that looked similar. By evening, Lin had reunited several records without pretending that the photograph and its description contained identical information. Her workflow illustrates representation and alignment: preserve useful evidence while making different observations comparable.

### 02 / The concept

A modality is a form of observation, such as pixels, text tokens, or waveform samples. An encoder maps that observation into a representation useful for a task. Alignment trains representations from different modalities so that meaningful correspondences receive compatible coordinates or scores. Equal vector length alone does not create alignment: two unrelated encoders can produce equally sized vectors with incompatible meanings. A shared embedding usually compresses information, retaining task-relevant structure while discarding details. Global image–text similarity also differs from grounding, which connects a particular phrase to a specific region or time interval.

### 03 / Put the concept to work

For an archive search system, encode stored photographs once and compare their embeddings with an incoming text query. Maintain the original photographs beside the index so users can inspect evidence. Check whether captions describe appearance, function, or historical context: these supervision choices change what matching means. Separate evaluation by object identity and photography session so nearly identical images do not create misleading retrieval results.

### 04 / How others use it

The Hugging Face CLIP documentation describes separate image and text encoders whose outputs are projected into the same dimensional space. This is a concrete implementation of comparable representations. Our museum example uses that design as a retrieval pattern; it is an original teaching scenario, not a reported museum deployment. A production adaptation would still need corpus-specific checks for duplicates, ambiguous descriptions, and relevant details lost during image preprocessing.

### 05 / The formula, unpacked

```text
zᵢ = fᵢ(x) / ‖fᵢ(x)‖₂
zₜ = fₜ(y) / ‖fₜ(y)‖₂
s(x, y) = zᵢ · zₜ
```

Here x is one image and y is one text description. The functions fᵢ and fₜ are learned image and text encoders, including any projection into a common d-dimensional space. The subscript i marks the image modality, not a sample index. The vectors zᵢ and zₜ have unit Euclidean length; ‖·‖₂ denotes that length. The dot denotes a dot product, and s is cosine similarity between −1 and 1. Both raw embeddings must be nonzero. This equation defines a score, not the training process that makes the score meaningful.

### 06 / Work through the numbers

Suppose an illustrative image encoder returns (3, 4). Its length is √(9 + 16) = 5, so the normalized image is (0.6, 0.8). Description A has embedding (0, 2), which normalizes to (0, 1). Its similarity is 0.6 × 0 + 0.8 × 1 = 0.8. Description B has embedding (2, 0), giving normalized coordinates (1, 0) and similarity 0.6. The retrieval system therefore places A before B. Doubling A's raw embedding to (0, 4) changes its magnitude but leaves its normalized score at 0.8. None of these numbers means an 80 percent probability that A is factually correct. They show an ordering under a particular representation; a user must still inspect whether the matching description identifies the actual object.

**Where the analogy stops:** The archive analogy treats meanings as tidy categories, whereas learned coordinates can encode tangled correlations. A close match may reflect background scenery rather than the intended object. Alignment does not recover missing observations, establish object identity, or guarantee that every word in a description is supported by the image.

**Keep this idea:** A shared representation makes observations comparable only when training establishes useful correspondence; similarity remains a task-dependent score that requires evidence checks.

### Sources for this topic

- [Hugging Face: Hugging Face Transformers: CLIP model documentation](https://huggingface.co/docs/transformers/model_doc/clip)

- [OpenAI / arXiv: Learning Transferable Visual Models From Natural Language Supervision](https://arxiv.org/html/2103.00020)

<a id="clip-contrastive"></a>

## CLIP: learn by choosing the right partner

### 01 / The story

Mara ran a repair shop with drawers full of replacement parts. Customers emailed photographs, while suppliers listed parts using short descriptions. A search tool repeatedly confused a silver hinge with a silver latch because both shared color and background. Mara organized training rounds containing several confirmed photograph–description pairs. In each round, the tool had to find the correct description for every photograph and the correct photograph for every description. Merely calling every metal object similar no longer solved the round. She included confusing alternatives, then discovered that two differently numbered listings actually described the same hinge. After removing that accidental contradiction, the tool retrieved more useful candidates on a separate set of customer photographs. Mara kept final compatibility checks with the technician. This is the central contrastive idea: a matching pair must stand out against alternatives, and the quality of those alternatives shapes what gets learned.

### 02 / The concept

CLIP is a dual-encoder model: an image encoder and a text encoder produce normalized embeddings that can be compared without jointly processing each candidate pair. During training, a batch supplies matched pairs and other batch members supply competing candidates. The symmetric objective rewards the diagonal of the similarity matrix in both retrieval directions. Temperature controls how strongly score differences affect the softmax. At inference, candidate label descriptions can act as class prototypes. Selecting among these descriptions is zero-shot classification relative to that target task, not unrestricted understanding or text generation.

### 03 / Put the concept to work

For parts retrieval, cache image embeddings and rank them against encoded queries. Validate prompts with realistic synonyms and descriptions of confusing neighboring categories. Keep true duplicates together when splitting data, and check whether an apparent negative is another valid match. If the service must reject unsupported queries, evaluate an explicit rejection policy on held-out examples; the largest softmax score alone does not establish that a suitable part exists.

### 04 / How others use it

The original CLIP paper specifies a symmetric cross-entropy objective over image–text similarities. OpenAI's reference repository exposes separate image and text encoding and demonstrates comparison with candidate descriptions. Those public mechanisms explain efficient retrieval and label-based classification. They do not imply a caption decoder. The toy calculation below follows the objective's two directions with invented scores; it is not a result from a released checkpoint.

### 05 / The formula, unpacked

```text
Sᵢⱼ = uᵢ · vⱼ / τ
Lᵢ→ₜ = −(1/N) Σᵢ ln[exp(Sᵢᵢ) / Σⱼ exp(Sᵢⱼ)]
Lₜ→ᵢ = −(1/N) Σᵢ ln[exp(Sᵢᵢ) / Σⱼ exp(Sⱼᵢ)]
L = (Lᵢ→ₜ + Lₜ→ᵢ) / 2
```

N is the number of paired examples in a batch, and i and j index examples from 1 through N. Unit vectors uᵢ and vⱼ represent image i and text j in the same embedding space. Pair i with i is the designated match. Positive τ is temperature, and Sᵢⱼ is the scaled similarity logit. The arrow labels indicate image-to-text and text-to-image losses. Σ sums over the indicated index, exp is the exponential, and ln is the natural logarithm. L averages both directions, assuming one designated positive per row and column.

### 06 / Work through the numbers

Take two pairs with cosine similarities arranged as [[0.8, 0.2], [0.1, 0.7]], and set τ = 0.2. The scaled matrix is [[4, 1], [0.5, 3.5]]. Each row has a correct-versus-incorrect gap of 3, so each correct row probability is 1/(1 + exp(−3)) ≈ 0.9526. Thus the image-to-text loss is about 0.0486. For the first column the correct gap is 3.5, giving loss ln(1 + exp(−3.5)) ≈ 0.0298. For the second column it is 2.5, giving about 0.0789. The text-to-image average is therefore 0.0543, and the final symmetric loss is (0.0486 + 0.0543)/2 ≈ 0.0515. Row and column losses differ because their competing scores differ, even though both use the same matched pairs.

**Where the analogy stops:** Mara's rounds suggest every alternative is wrong, but real batches can contain several valid descriptions of similar images. Such false negatives complicate learning. The selected prompts also define the available choices. High relative confidence among unsuitable labels does not demonstrate calibration, factual correctness, or reliable recognition outside the evaluated domain.

**Keep this idea:** CLIP learns relative compatibility in two directions; its scores depend on the candidate set, temperature, and whether the assumed negatives are truly different.

### Sources for this topic

- [OpenAI / arXiv: Learning Transferable Visual Models From Natural Language Supervision](https://arxiv.org/html/2103.00020)

- [OpenAI: OpenAI CLIP: official repository and usage examples](https://github.com/openai/CLIP)

- [Hugging Face: Hugging Face Transformers: CLIP model documentation](https://huggingface.co/docs/transformers/model_doc/clip)

<a id="cross-attention-fusion"></a>

## Cross-attention: ask one stream to inspect another

### 01 / The story

Nadia supervised a workshop assembling small wooden boats. One afternoon a trainee sent a photograph and asked which clamp should be loosened before removing the hull. A general description of the photograph listed wood, tools, and a workbench, but missed the question. Nadia instead used the words hull and loosened to inspect particular places: the clamp near the bow, the support underneath, and the loose clamp on the table. She compared their relevance, concentrated on the bow clamp, and explained the next step with a reference to that visible location. The trainee released the correct clamp and removed the hull intact. Her reasoning changed with the question even though the photograph stayed the same. Cross-attention provides a mathematical mechanism for a related operation: representations from one stream select and combine information from another, producing an answer-specific view rather than one fixed summary.

### 02 / The concept

In cross-attention, queries originate from one representation stream and keys and values originate from another. A query scores the keys, softmax turns those scores into weights, and the weights combine the values. The result can vary with the question or decoder state. Fusion is the broader process of allowing modalities to interact; it can also use concatenated tokens with self-attention or other connectors. A dual encoder supports cheap independent indexing, while cross-attention usually requires candidate-specific interaction. The latter can preserve more detailed relationships but adds computation and does not automatically provide trustworthy explanations.

### 03 / Put the concept to work

For a visual assistant, keep image patch representations available while the question is processed. This allows different question tokens or learned queries to gather different evidence. In a large archive, first retrieve a small candidate set with independent embeddings, then use a more expensive fusion model to rerank candidates. Measure whether added interaction actually improves difficult relations, rather than assuming a more elaborate connector must help.

### 04 / How others use it

The Transformer paper defines scaled dot-product attention and explains decoder attention to encoder outputs. BLIP-2 applies cross-attention in its Q-Former: learned queries extract information from frozen image features. These are specific public examples of the general mechanism. The boat story does not claim that attention weights reproduce human inspection, and the calculation isolates one attention head rather than the full residual, normalization, and multilayer computation of a deployed model.

### 05 / The formula, unpacked

```text
A = softmax(QKᵀ / √dₖ)
O = AV
```

Q contains m query vectors, K contains n key vectors, and V contains n value vectors. Queries and keys each have dₖ coordinates; values have dᵥ coordinates. Thus Q is m × dₖ, K is n × dₖ, V is n × dᵥ, and the output O is m × dᵥ. The superscript T means transpose. A is an m × n matrix of attention weights. Softmax operates across each query's n candidate keys, so every row sums to one. This simplified formula omits masks, dropout, and the learned projections that create Q, K, and V.

### 06 / Work through the numbers

Consider one query Q = (1, 0), two keys (2, 0) and (0, 2), and value vectors (10, 0) and (0, 4). Here dₖ = 2, so the unscaled dot products 2 and 0 become logits √2 and 0 after division by √2. Exponentiation gives about 4.1133 and 1. Their normalized weights are therefore 0.8044 and 0.1956. The weighted value is (0.8044 × 10, 0.1956 × 4), approximately (8.0443, 0.7823). If the query changes to (0, 1), the weights reverse and the output becomes approximately (1.9557, 3.2177). The same stored visual values now contribute differently because the request changed. This is selective mixing, not copying the most highly weighted patch, and neither coordinate is inherently a human-readable object label.

**Where the analogy stops:** Nadia deliberately checks meaningful locations, whereas neural attention mixes learned vectors that may encode many overlapping properties. High weight does not prove causal importance or factual grounding. Information can also pass through residual connections and other layers, so displaying one attention map is not a complete account of the model's decision.

**Keep this idea:** Cross-attention makes information selection depend on a query; its weighted mixtures enable interaction but need separate tests of grounding and usefulness.

### Sources for this topic

- [arXiv: Attention Is All You Need](https://arxiv.org/abs/1706.03762)

- [Salesforce Research / arXiv: BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models](https://arxiv.org/html/2301.12597)

<a id="conditional-generation"></a>

## Captioning and VQA: generate under visual conditions

### 01 / The story

Jules prepared an accessible catalogue for a community ceramics exhibition. An early assistant described a photograph as a blue bowl on a table. That was useful until a visitor asked how many handles the bowl had. Repeating the caption did not answer the question, and the assistant's confident guess of two handles contradicted the visible single handle. Jules separated the tasks. The catalogue needed a concise description of prominent content, while the visitor needed a response conditioned on both the image and a specific question. She added examples with explicit handle counts and preserved uncertain cases where the far side was hidden. In the revised workflow, the assistant answered one visible handle and marked the unseen side as unknown. Jules published the checked entry. The outcome illustrates why fluent conditional text must remain tied to the exact observation and request that produced it.

### 02 / The concept

Image captioning predicts a text sequence conditioned on an image. Generative visual question answering adds a question to that condition. An autoregressive decoder predicts each token given the visual context and earlier tokens; multiplying those conditional probabilities gives the sequence probability. During teacher-forced training, earlier tokens come from the reference response, whereas inference consumes the model's own previous output. VQA can also be formulated as classification over a fixed answer set, so not every visual question answering model generates tokens. Both formulations still require evidence that the image influences the answer appropriately.

### 03 / Put the concept to work

Choose the output contract before choosing a decoder: a catalogue caption, an answer from a fixed vocabulary, or an open response serve different needs. Include difficult cases with occlusion, counting, and misleading question assumptions in evaluation. Compare answers after replacing or removing the image to detect language-only shortcuts. Keep image evidence available for review, especially when polished prose could hide a missing visual observation.

### 04 / How others use it

Hugging Face's image-captioning guide demonstrates image-conditioned text generation. Its VQA guide explicitly contrasts a ViLT classification head with generative answering using BLIP-2. These examples support the distinction between task and output mechanism: asking about an image does not dictate one architecture. Our calculation explains a generic autoregressive likelihood, not the exact tokenizer, loss masking, or decoding settings of every model in those guides.

### 05 / The formula, unpacked

```text
p(y | x, q) = ∏ₜ₌₁ᵀ p(yₜ | x, q, y₍₁:ₜ₋₁₎)
L = −(1/T) Σₜ₌₁ᵀ ln p(yₜ | x, q, y₍₁:ₜ₋₁₎)
```

x is the image, q is the question or task prompt, and y is the target sequence containing T supervised tokens. The index t identifies the current token yₜ, and y₍₁:ₜ₋₁₎ means all earlier target tokens, with an empty history at the first position. The product sign ∏ combines conditional probabilities, while Σ and ln produce mean negative log-likelihood L. All probabilities are strictly positive in this example. We treat any required ending token as part of T and exclude unsupervised prompt positions. This is a token-averaged illustrative loss, not a claim about every training implementation.

### 06 / Work through the numbers

Suppose a tiny illustrative tokenizer represents the checked answer as three tokens: one, handle, and an ending token. Under teacher forcing, their reference-token probabilities are 0.4, 0.5, and 0.9. The complete response probability is 0.4 × 0.5 × 0.9 = 0.18. Its summed negative log-likelihood is −ln(0.18) ≈ 1.7148, and the mean loss is 1.7148/3 ≈ 0.5716. Now imagine the incorrect sequence two, handles, and an ending token has conditional probabilities 0.5, 0.7, and 0.9. Its probability is 0.315, larger than 0.18. The two first-token probabilities sum to 0.9, so they are compatible alternatives. A decoder could prefer the wrong sequence. Likelihood measures what the model predicts, while visual correctness must be established independently. Low loss on familiar references therefore does not certify accurate answers to new images.

**Where the analogy stops:** Jules can deliberately distinguish visible evidence from hidden surfaces; a decoder may still complete a familiar linguistic pattern. The story therefore illustrates a desired workflow rather than an automatic guarantee of uncertainty awareness. Caption agreement, token likelihood, and answer fluency each measure something different from whether a particular visual claim is true.

**Keep this idea:** Conditional generation explains how an answer is produced; checking the conditioning evidence explains whether that answer deserves to be believed.

### Sources for this topic

- [Hugging Face: Hugging Face Transformers: image captioning](https://huggingface.co/docs/transformers/tasks/image_captioning)

- [Hugging Face: Hugging Face Transformers: visual question answering](https://huggingface.co/docs/transformers/tasks/visual_question_answering)

<a id="visual-instruction-tuning"></a>

## Visual instruction tuning: connect perception to a request

### 01 / The story

At a small botanical garden, engineer Sora built a kiosk that could describe plant photographs. Visitors immediately asked different questions: compare two leaves, explain a damaged edge, or summarize the sign in simpler language. The kiosk kept returning a generic description because its examples had taught only that behavior. Sora first ensured that the visual features could reach the language component, then assembled carefully checked image–request–response examples. She compared two adaptation plans: train a bridge while keeping existing specialists fixed, or also update the language specialist to follow the new requests. The second plan required different training resources and checks for changed behavior. After a limited trial, the kiosk could follow the supported request types, while uncertain plant identifications still went to a gardener. Sora learned that connecting an image pathway and teaching instruction following are related design decisions, but neither substitutes for the other.

### 02 / The concept

Visual instruction tuning uses image-conditioned requests and desired responses to teach task-following behavior. It should be distinguished from learning a compatible visual–language interface. In the original LLaVA, a linear projection connects CLIP visual features to a language model; initial alignment trains the projection, and subsequent instruction tuning updates the projection and language model while freezing the vision encoder. BLIP-2 instead pretrains a Q-Former using a frozen image encoder, then connects it to a frozen language model for generative learning. Its two-stage pretraining is not the same training recipe as LLaVA's visual instruction tuning.

### 03 / Put the concept to work

When adapting a visual assistant, record which components are frozen, which parameters receive updates, and which response tokens contribute to the loss. Build examples that require the image to answer the instruction, including carefully labeled uncertainty. Check whether the model follows formatting requests while ignoring the picture. Compare against the same system before adaptation so improvements in style are not mistaken for improvements in visual evidence use.

### 04 / How others use it

LLaVA's original paper and project describe visual instruction data and a simple projection-based interface. BLIP-2's paper describes learned queries that compress image features before a projection feeds the language model. Later systems with similar names can change these details, so this comparison is explicitly about the original papers. The formula below isolates connector adaptation with a toy squared-error objective; both papers use richer language and multimodal objectives, not this toy objective.

### 05 / The formula, unpacked

```text
h = Wz
E = ½ ‖h − r‖₂²
W′ = W − η(h − r)zᵀ
```

z is a fixed visual feature column with dᵥ entries. W is a trainable dₗ × dᵥ connector, and h is its dₗ-dimensional output in an illustrative language-side space. The target vector r has the same dimension as h. E is half the squared Euclidean error, ‖·‖₂ denotes Euclidean length, and η is a positive learning rate. Transpose T makes zᵀ a row, so (h − r)zᵀ has W's shape. W′ is the updated connector. This single-example gradient step assumes z and r are fixed and omits a bias term.

### 06 / Work through the numbers

Let z = (2, −1)ᵀ, let W be the two-dimensional identity matrix, and choose target r = (1, 1)ᵀ. Initially h = (2, −1)ᵀ and the error vector is (1, −2)ᵀ, so E = (1² + (−2)²)/2 = 2.5. The connector gradient is the outer product [[2, −1], [−4, 2]]. With η = 0.1, the updated matrix becomes [[0.8, 0.1], [0.4, 0.8]]. Multiplying this by the unchanged z gives h′ = (1.5, 0)ᵀ. The new error is (0.5, −1)ᵀ and the loss is (0.25 + 1)/2 = 0.625. Adaptation improved the connector without changing the visual feature. This illustrates what freezing permits, but it neither predicts instruction-following performance nor represents a full LLaVA or BLIP-2 training step.

**Where the analogy stops:** Sora's specialists sound like independent people, but neural modules exchange dense learned representations and can rely on fragile correlations. Freezing weights does not eliminate activation memory or all backward computation. Instruction tuning can teach a convincing response style without fixing perception, and this historical comparison should not be generalized to every later LLaVA or BLIP variant.

**Keep this idea:** Separate the connector, training data, and update policy: original LLaVA and BLIP-2 combine these ingredients differently, with different adaptation goals.

### Sources for this topic

- [arXiv: Visual Instruction Tuning](https://arxiv.org/html/2304.08485)

- [LLaVA research team: LLaVA: original visual instruction tuning project](https://llava-vl.github.io/)

- [Salesforce Research / arXiv: BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models](https://arxiv.org/html/2301.12597)

<a id="audio-text-alignment"></a>

## Audio and text: hearing words is one of several tasks

### 01 / The story

Radio producer Emil searched an old recording library for a scene with rain outside and a door closing indoors. A transcription system returned no useful words because the clips contained almost no speech. Emil realized that the request described acoustic events, not a sentence someone had spoken. He created short descriptions of verified recordings and searched by audio–text similarity. The first result contained heavy rain but no door, while the next included both requested sounds. He listened to the originals before selecting the second clip. Later, a colleague needed the spoken station announcement from the same collection, so Emil used transcription for that separate job. Both tools accepted audio and related it to language, but they answered different questions. His successful edit depended on matching the model's learning objective to the requested evidence, rather than treating all audio–language systems as interchangeable listeners.

### 02 / The concept

Audio begins as samples over time, often transformed into spectral features before encoding. Sample rate specifies how many samples represent one second; changing a rate label without resampling changes the interpreted timing and pitch. Audio–text alignment can associate a sound with a descriptive sentence, enabling retrieval or classification by text. Speech recognition instead estimates the words spoken, often through conditional sequence generation. A recording can contain speech, environmental sounds, music, and silence simultaneously. The supervision and objective determine which aspects the representation preserves, so transcription accuracy does not measure general acoustic understanding.

### 03 / Put the concept to work

Choose transcription when the desired evidence is spoken wording; choose a suitable audio–text retrieval model when the query describes a sound event. Preserve duration, channel handling, and the required sample rate throughout preprocessing. Evaluate overlapping sounds separately from clean single-source clips. If an event occupies only a brief part of a long recording, compare segment-level retrieval with one global embedding so a dominant background does not conceal it.

### 04 / How others use it

Whisper's original research and repository describe an encoder–decoder trained for speech tasks, including recognition and translation. The CLAP research used here trains audio and text encoders contrastively and evaluates text-to-audio retrieval and audio classification. These documented objectives support Emil's choice of different tools. Neither source establishes that a transcript preserves all non-speech events, and the retrieval example below is an invented vector calculation rather than a measured CLAP result.

### 05 / The formula, unpacked

```text
n = fₛD
s(a, b) = (a · b) / (‖a‖₂ ‖b‖₂)
```

n is the number of samples in one audio channel, fₛ is the sample rate in samples per second, and D is duration in seconds. The first equation assumes an exact whole-number sample count; real boundaries may need rounding. Nonzero vectors a and b are the audio and text embeddings in the same learned space. Their dot product is divided by their Euclidean lengths, denoted by ‖·‖₂, to obtain cosine similarity s. Sample count describes the waveform, whereas embedding dimension describes the representation; the two are not interchangeable quantities.

### 06 / Work through the numbers

A four-second mono recording sampled at 48,000 samples per second contains 192,000 samples. Properly resampling it to 16,000 samples per second gives 64,000 samples while preserving its four-second duration. Merely relabeling the original samples as 16,000 would instead imply twelve seconds, so that shortcut changes the signal's interpretation. Now suppose a retrieval encoder produces the unit audio vector (0.8, 0.6). A candidate description has unit vector (0.6, 0.8), giving similarity 0.48 + 0.48 = 0.96. Another has vector (0, 1), giving 0.6. The first ranks higher in this two-candidate comparison. Its high score does not locate either sound within the clip, identify spoken words, or prove that every event in the description occurred; those conclusions require additional evidence or task-specific outputs.

**Where the analogy stops:** Emil can listen again and separate the requested events, while a global embedding can merge simultaneous sources or discard their order. A semantic match does not imply a faithful transcript, speaker identity, or precise timing. The simple sample-count equation also omits stereo channels, compression, windowing, and the spectral processing used by particular encoders.

**Keep this idea:** Match the audio objective to the question: retrieving a described sound, transcribing speech, and locating an event require different evidence and evaluation.

### Sources for this topic

- [OpenAI / arXiv: Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356)

- [OpenAI: OpenAI Whisper: official architecture and usage documentation](https://github.com/openai/whisper)

- [arXiv: Large-scale Contrastive Language-Audio Pretraining with Feature Fusion and Keyword-to-Caption Augmentation](https://arxiv.org/abs/2211.06687)

<a id="video-temporal-grounding"></a>

## Video: what happened, and when did it happen?

### 01 / The story

Rina edited a twelve-second demonstration of a folding chair. Her client wanted the moment when the safety latch clicked into place. A contact sheet sampled every two seconds showed the chair closed, partly open, and fully open, but none of the sampled frames showed the brief latch movement. Rina returned to the original clip and inspected the uncertain interval more densely. She marked a short segment containing the movement and checked that it happened before the demonstrator sat down. The final edit included both the latch action and enough neighboring footage to make the sequence understandable. A single attractive frame would not have solved the request. Rina's workflow separates three decisions that video models also face: which observations to keep, how to represent their order, and how to connect a language query to an interval rather than merely to the whole video.

### 02 / The concept

Video adds time to visual representation. Sampling converts a continuous or densely recorded stream into a tractable set of frames or clips, but omitted events cannot be recovered from those samples alone. Temporal modeling represents ordering and change; averaging frame embeddings can lose both. Temporal grounding takes a language query and predicts one or more relevant intervals. This differs from assigning an activity label to the entire video. Evaluation must therefore consider boundary accuracy and retrieval quality, while checking that train and test clips do not share the same underlying recording.

### 03 / Put the concept to work

Set a sampling policy according to the duration of events the application must detect, then test short events near sampling boundaries. Store timestamps alongside features so retrieved evidence can be played back. For a long demonstration, a coarse retrieval pass can identify candidate regions for denser inspection. Evaluate before-and-after queries separately from object-presence questions: a system can recognize a chair while misunderstanding the order of assembly steps.

### 04 / How others use it

The QVHighlights research formulates natural-language moment retrieval and highlight detection; its Moment-DETR model jointly predicts relevant temporal spans and saliency. The paper's input features are extracted every two seconds, a documented design choice rather than a universal sampling rule. Hugging Face's video-classification guide shows another task with clip sampling. Comparing these sources helps separate video preprocessing from the particular question, output, and evaluation being modeled.

### 05 / The formula, unpacked

```text
tₖ = kΔ,  0 ≤ k < D/Δ
I = max(0, min(pₑ, gₑ) − max(pₛ, gₛ))
U = (pₑ − pₛ) + (gₑ − gₛ) − I
tIoU = I / U
```

D is the video duration in seconds and Δ is a positive sampling interval. Integer k starts at zero, and tₖ is a sampled timestamp strictly before D. This rule samples instants, not complete clips. Predicted interval endpoints are pₛ and pₑ, while reference endpoints are gₛ and gₑ, all in seconds on the same timeline. Each end must exceed its start. I is intersection duration and U is union duration. The functions min, max, and the zero clamp prevent negative overlap; tIoU is temporal intersection over union, assuming U is positive.

### 06 / Work through the numbers

For D = 12 seconds and Δ = 2 seconds, the sampling rule keeps timestamps 0, 2, 4, 6, 8, and 10. An action occurring only from 5.2 to 5.7 seconds is absent from all six sampled instants; a model cannot inspect those missing frames through this representation. Now consider a separate, longer reference interval [4, 8] and a predicted interval [5, 9]. Their intersection lasts min(9, 8) − max(5, 4) = 3 seconds. Each interval lasts four seconds, so the union lasts 4 + 4 − 3 = 5 seconds. Temporal IoU is 3/5 = 0.6. This score quantifies boundary overlap, but does not establish that the prediction described the correct action or that the chosen sampling captured a shorter event inside the interval.

**Where the analogy stops:** Rina can revisit the original recording, while a model given only cached sparse frames cannot recover discarded visual evidence. Temporal overlap also treats seconds geometrically: two intervals can overlap well yet refer to different events. The example ignores audio cues and motion inside clips, both of which can materially change what observations are available.

**Keep this idea:** Video understanding depends on retained evidence and temporal order; locating an interval requires different outputs and checks from labeling an entire clip.

### Sources for this topic

- [arXiv: QVHighlights: Detecting Moments and Highlights in Videos via Natural Language Queries](https://arxiv.org/html/2107.09609)

- [QVHighlights research authors: Moment-DETR: official code and QVHighlights data documentation](https://github.com/jayleicn/moment_detr)

- [Hugging Face: Hugging Face Transformers: video classification](https://huggingface.co/docs/transformers/tasks/video_classification)

<a id="evaluation-hallucination"></a>

## Evaluation: fluent claims still need observable support

### 01 / The story

A local archive asked reviewer Bea to approve automatically written descriptions of street photographs. One caption mentioned a bicycle beside a bus stop, although the image contained only the bus stop. The sentence sounded natural because bicycles often appeared in similar photographs. Bea stopped scoring descriptions only by their resemblance to reference prose. She counted unsupported object mentions, checked the proportion of affected captions, and recorded correct visual facts separately. A revised system became more cautious and reduced invented objects, but also omitted useful details from several images. Bea therefore added a measure of retained correct information and reviewed the uncertain cases with another annotator. The team selected a setting that balanced useful coverage with fewer unsupported claims. Its report included both outcomes and examples of remaining mistakes. The lesson was practical: reliability becomes visible only when evaluation separates what is stated, what is supported, and what is silently left out.

### 02 / The concept

A hallucinated visual claim asserts content unsupported by the image or video supplied to the system. It can arise when language regularities outweigh perceptual evidence. Evaluation should distinguish task success, factual grounding, calibration, and useful coverage. Object hallucination metrics address a specific subset of errors; they do not cover every incorrect relation, count, action, or explanation. Reference captions can omit real objects, so annotation protocols must specify how visual presence is established. A system that says almost nothing may avoid some unsupported claims while failing the user's information need.

### 03 / Put the concept to work

Keep a review table linking each important claim to the image region, timestamp, or explicit absence of supporting evidence. Combine automatic metrics with a defined annotation protocol and a checked sample of disagreements. Report performance separately for counting, relations, small objects, and misleading prompts. Compare output coverage alongside unsupported-claim rates so a shorter response is not automatically credited as a more capable visual assistant.

### 04 / How others use it

The CHAIR research introduced object-hallucination measures for image captions and examined why sentence similarity can miss visual errors. POPE evaluates object hallucination with questions about object presence, providing a different measurement setup. These sources motivate complementary checks, not a universal trust score. The calculation uses CHAIR's instance-level and sentence-level forms under an explicitly simplified annotation scheme; it does not reproduce either paper's benchmark results.

### 05 / The formula, unpacked

```text
CHAIRᵢ = H / M
CHAIRₛ = Cₕ / C
R = K / G
```

H is the number of hallucinated object mentions and M is the total number of object mentions under one fixed matching protocol. Cₕ is the number of captions containing at least one hallucinated object, and C is the total number of captions. Subscripts i and s indicate instance-level and sentence-level CHAIR. For a separate illustrative coverage measure, K counts correctly mentioned target objects and G counts all annotated target objects. R is that coverage ratio, not an additional CHAIR definition. Assume positive denominators, consistent synonym handling, and one counted mention per object within each caption.

### 06 / Work through the numbers

Suppose ten captions contain forty counted object mentions. Reviewers identify six unsupported mentions distributed across four captions. Instance-level CHAIR is 6/40 = 0.15, while sentence-level CHAIR is 4/10 = 0.40. The two values answer different questions: how many mentions are wrong, and how often a caption contains any such error. Suppose there are fifty annotated target objects and the remaining thirty-four mentions are distinct correct targets. Coverage is then 34/50 = 0.68. A shorter revision contains twenty mentions, only one unsupported, in one of ten captions. Its CHAIR values improve to 0.05 and 0.10, but coverage drops to 19/50 = 0.38. That tradeoff is visible only because all three quantities are reported. These arithmetic results describe the invented audit, not an expected outcome for a particular model.

**Where the analogy stops:** Bea's audit assumes reviewers can determine object presence reliably, which becomes difficult with occlusion, small regions, and incomplete annotations. A low object-hallucination rate does not verify relations, identity, or reasoning. Coverage depends on the chosen target inventory, and the simplified counting rules here must not be mistaken for a complete implementation of the published evaluation protocols.

**Keep this idea:** Evaluate both unsupported claims and retained useful evidence; reliable multimodal output must be grounded, informative, and honest about what the observations cannot establish.

### Sources for this topic

- [arXiv: Object Hallucination in Image Captioning](https://arxiv.org/html/1809.02156)

- [arXiv: Evaluating Object Hallucination in Large Vision-Language Models](https://arxiv.org/abs/2305.10355)

## The reference desk

### [Representation is a learned agreement](#modalities-alignment)

Equal dimensions make vectors compatible in shape; paired supervision makes their similarities useful. Keep original observations available to verify retrieved matches.

### [Contrastive scores are relative](#clip-contrastive)

CLIP compares both retrieval directions. Candidate descriptions, temperature, and false negatives affect the result; a softmax score is not a universal correctness probability.

### [Fusion changes with the query](#cross-attention-fusion)

Cross-attention combines values according to query–key compatibility. It supports detailed interaction, but an attention map alone does not establish causal explanation or grounding.

### [Generation and correctness are separate](#conditional-generation)

Captioning and generative VQA condition token predictions on visual context. High sequence likelihood can still favor an incorrect answer, so inspect the image evidence.

### [Name the trainable components](#visual-instruction-tuning)

Original LLaVA updates its connector and language model during instruction tuning; BLIP-2's pretraining uses a Q-Former with frozen vision and language backbones.

### [Audio tasks preserve different evidence](#audio-text-alignment)

Whisper's speech-to-text objectives and CLAP's contrastive audio–text objective serve different needs. Correct resampling preserves duration; semantic retrieval does not supply timestamps automatically.

### [Missing frames mean missing evidence](#video-temporal-grounding)

Sampling determines which events remain observable. Temporal grounding predicts intervals, and temporal IoU measures boundary overlap without independently verifying the action's identity.

### [Count omissions as well as inventions](#evaluation-hallucination)

Object hallucination rates and correct-information coverage reveal different failures. Report both, define the annotation protocol, and inspect remaining errors beyond object presence.

## Official tutorials & original research

Original stories, explanations and examples by Guoliang. The linked tutorials and research belong to their respective authors; these independent companions are not official translations or endorsed courses.

- [Hugging Face Transformers: CLIP model documentation](https://huggingface.co/docs/transformers/model_doc/clip) — Hugging Face

- [Learning Transferable Visual Models From Natural Language Supervision](https://arxiv.org/html/2103.00020) — OpenAI / arXiv

- [OpenAI CLIP: official repository and usage examples](https://github.com/openai/CLIP) — OpenAI

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — arXiv

- [Hugging Face Transformers: image captioning](https://huggingface.co/docs/transformers/tasks/image_captioning) — Hugging Face

- [Hugging Face Transformers: visual question answering](https://huggingface.co/docs/transformers/tasks/visual_question_answering) — Hugging Face

- [BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models](https://arxiv.org/html/2301.12597) — Salesforce Research / arXiv

- [Visual Instruction Tuning](https://arxiv.org/html/2304.08485) — arXiv

- [LLaVA: original visual instruction tuning project](https://llava-vl.github.io/) — LLaVA research team

- [Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356) — OpenAI / arXiv

- [OpenAI Whisper: official architecture and usage documentation](https://github.com/openai/whisper) — OpenAI

- [Large-scale Contrastive Language-Audio Pretraining with Feature Fusion and Keyword-to-Caption Augmentation](https://arxiv.org/abs/2211.06687) — arXiv

- [QVHighlights: Detecting Moments and Highlights in Videos via Natural Language Queries](https://arxiv.org/html/2107.09609) — arXiv

- [Moment-DETR: official code and QVHighlights data documentation](https://github.com/jayleicn/moment_detr) — QVHighlights research authors

- [Hugging Face Transformers: video classification](https://huggingface.co/docs/transformers/tasks/video_classification) — Hugging Face

- [Object Hallucination in Image Captioning](https://arxiv.org/html/1809.02156) — arXiv

- [Evaluating Object Hallucination in Large Vision-Language Models](https://arxiv.org/abs/2305.10355) — arXiv
