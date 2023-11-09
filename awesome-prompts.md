# Awesome ChatGPT Prompts for Language Learning

Below are some great ChatGPT prompts for learning a foreign language. They are grouped by levels of proficiency in prompt engineering. I am using Japanese as an Example. Most of this applies to other languages as well.

Note that depending on the volume of training data, ChatGPT might perform better/worse for some languages.

Other great general-purpose ChatGPT prompts and resources can be found at [prompts.chat](https://prompts.chat).

I have also made a [Japanese News Every Day website](https://digicosmos86.github.io/maiasahi), which is hosted in this repo, to help myself learn Japanese from the latest news every day.

## Level 1: Generic (and sometimes naïve) prompts.

You can probably find these prompts somewhere else on the Internet.

### Vocabulary

```
I am an Anime/Manga fan. Can you recommend 25 words and sentences that often appear in Anime/Manga?
```

```
I am at JLPT N4 level. I want to take JLPT N3 in three months. Make me a list of JLPT N3 vocabulary to learn in the first month.
```

```
I am traveling to Japan in a week. What are some of the expressions that might be helpful?
```

```
Create a Japanese–English vocabulary list on the theme of cooking.
```

![Waku waku](https://media.tenor.com/jiRSjXlEuF0AAAAd/waku-waku-excited.gif | width=200)

```
List words in Japanese like "ワクワク".
```

```
Can you show me antonym pairs such as 大きい and 小さい？
```

### Grammar / Comprehension

```
How to use the te-form in Japanese?
```

```
What are the differences between the conditional forms と、ば、たら、なら in Japanese?
```

```
How to conjugate Japanese verbs from their dictionary form to passive form?
```

```
Are there any grammatical errors in the following paragraph?
```

Below I asked ChatGPT to explain part of the lyrics from an Anime song.

```
Explain this sentence 沈むように溶けてゆくように
```

ChatGPT's response:

The sentence "沈むように溶けてゆくように" in Japanese can be translated as "as if sinking and melting away." It's a poetic expression that could be used to describe a state of slowly disappearing or dissipating, much like how an object might slowly sink into water and seem to melt away into nothingness. This phrase can be used metaphorically to describe a variety of situations, such as the fading of memories, the softening of emotions, or even the setting of the sun. It evokes a sense of gentle transition from one state to another.

## Level 2. Add some prompt engineering.

Some tips in prompt engineering:

### 1. Be very specific about what you want from ChatGPT

```
Can you explain the vocabulary, structure, and grammatical points in this sentence:

炭治郎からは泣きたくなるような優しい音がする。今まで聞いたこともないくらい優しい音だ。
```

ChatGPT's response:

Certainly! Let's break down the Japanese sentence:

1. 炭治郎からは泣きたくなるような優しい音がする。

**Vocabulary and Structure:**

- 炭治郎 (Tanjiro): This is a character's name, likely from the popular anime/manga series "Demon Slayer" (Kimetsu no Yaiba).
- から (kara): This is a particle that means "from" or "out of."
- は (wa): This is a topic marker, indicating that what follows is the topic of the sentence.
- 泣きたくなる (nakitaku naru): This is a phrase that means "to want to cry" or "to feel like crying."
- ような (yōna): This is a grammar construct used to compare or describe something that resembles another thing. In this context, it's used to describe the sound that is so gentle that it makes you want to cry.
- 優しい (yasashii): This means "gentle" or "kind."
- 音 (oto): This means "sound."
- が (ga): This is a subject marker, indicating that what precedes it is the subject of the sentence.
- する (suru): This is a verb meaning "to do" or "to make." In this context, it means "to produce" or "to emit."
  **Translation:** "From Tanjiro, a sound that makes you want to cry can be heard."

2. 今まで聞いたこともないくらい優しい音だ。

**Vocabulary and Structure:**

- 今まで (ima made): This means "until now" or "up to this point."
  聞いたこともない (kiita koto mo nai): This phrase means "have never heard."
- くらい (kurai): This is used to indicate the extent or degree of something. In this context, it means "to the extent."
- 優しい (yasashii): As mentioned earlier, this means "gentle" or "kind."
- 音 (oto): Again, this means "sound."
- だ (da): This is the copula, which is used to assert or describe something.
  **Translation:** "It's a sound that is so gentle that I've never heard up to this point."

So, the overall sentence means, "From Tanjiro, a sound that makes you want to cry can be heard. It's a sound that is so gentle that I've never heard up to this point." This sentence likely describes a very soothing or touching sound associated with the character Tanjiro in the context of the "Demon Slayer" series.

### 2. You can format ChatGPT's output

You can also specify the form of ChatGPT's output. ChatGPT understands HTML, markdown, and JSON very well.

```
I am at JLPT N4 level. I want to take JLPT N3 in three months. Make me a list of JLPT N3 vocabulary to learn in the first month.

Format your response with a Markdown table.
```

Combining the two tips, you can be very specific about what you want ChatGPT to output:

```
I am at JLPT N4 level. I want to take JLPT N3 in three months. Make me a list of JLPT N3 vocabulary to learn in the first month.

Format your response with a Markdown table with the following 3 columns:

1. Word (with furigana annotations in parentheses next to it)
2. Part of speech
3. Meaning (in lower case)
```

ChatGPT likes bullet points a lot. Make sure you use bullet points to make your prompt as specific as possible.

### 3. Context is very important

Context is very important in prompt engineering. Sometimes letting the LLM know the role that they are playing can change the output of model entirely. It is helpful to provide this information at the beginning of each prompt.

```
You are a Japanese tutor that teaches intermediate to advanced level Japanese learners who are native English speakers.

I am at JLPT N4 level. I want to take JLPT N3 in three months. Make me a list of JLPT N3 vocabulary to learn in the first month.

Format your response with a Markdown table with the following 3 columns:

1. Word (with furigana annotations in parentheses next to it)
2. Part of speech
3. Meaning (in lower case)
```

Try changing ChatGPT's output to HTML tables or JSON.

## Level Ninja: Provide more context to ChatGPT

Context also grounds ChatGPT: it encourages ChatGPT to take information from the context, which reduces its tendency to hallucinate. We can take advantage of this and provide texts in the language that we want to learn to ChatGPT, and ask it to provide us information based on the text.

For this section, let's use this article about the risks of Generative AI in Japanese.

```
岸田文雄首相の声と画像を使ってひわいな発言をしたように見せかけた偽動画が、日本テレビのニュース番組のロゴを使って編集され、X（旧ツイッター）などSNS上で拡散されている。日テレは動画について「フェイク動画」だとして注意を呼びかけている。

偽動画は生成AIを利用して作られたものと見られ、スーツ姿の岸田氏が、カメラに向かって語りかけている様子が収められている。さらに、日テレの「日テレNEWS24」のロゴを使い、ニュース番組で中継されているように装っている。同社は番組を通じて「放送、番組ロゴをフェイク動画に悪用されたことは到底許すことはできない」と注意を呼びかけた。

現在、生成AIを巡っては、主要7カ国（G7）の国際ルール作りを目指す「広島AIプロセス」の年内の策定に向けて議論が進んでいる。10月30日には、生成AIの開発者を対象にした「行動規範」をG7で合意。生成AIのリスクを特定し、適切な対応を実施することが盛り込まれており、リスクとして偽情報の助長やプライバシー侵害などがあげられている。（明楽麻子）
```

### 1. Pronunciation annotation

You can use ChatGPT to annotate the pronunciation of words in the article.

```
Can you annotate the furigana of the kanji words and phrases in the following paragraph?

岸田文雄首相の声と画像を使ってひわいな発言をしたように見せかけた偽動画が、日本テレビのニュース番組のロゴを使って編集され、X（旧ツイッター）などSNS上で拡散されている。日テレは動画について「フェイク動画」だとして注意を呼びかけている。
```

Here's the magic of ChatGPT. You can ask ChatGPT to annotate pronunciation with `<ruby>` tags instead of parenthesis. For example:

```html
<ruby>インターネット<rt>Internet</rt></ruby>
```

becomes

<ruby>インターネット<rt>Internet</rt></ruby>

Using this, we can ask ChatGPT to generate pronunciation annotation in `<ruby>` tags:

```
You are an app that annotates pronunciation of kanjis for Japanese learners. Enclose all words and phrases in <ruby> tags with their furigana annotation in <rt> tags.

<p>
岸田文雄首相の声と画像を使ってひわいな発言をしたように見せかけた偽動画が、日本テレビのニュース番組のロゴを使って編集され、X（旧ツイッター）などSNS上で拡散されている。日テレは動画について「フェイク動画」だとして注意を呼びかけている。
</p>
```

Note that I put the paragraph itself in a set of `<p>` tags. This has two benefits. First, since ChatGPT understands HTML (and code in general) really well, this separates the actual paragraph from instructions. Also, since the results are also HTML, this actually gives ChatGPT a hint of what it is supposed to do.

Here's the ChatGPT output. Magic, isn't it?

<p>
<ruby>岸田文雄<rt>きしだ ふみお</rt></ruby><ruby>首相<rt>しゅしょう</rt></ruby>の<ruby>声<rt>こえ</rt></ruby>と<ruby>画像<rt>がぞう</rt></ruby>を<ruby>使<rt>つか</rt></ruby>ってひわいな<ruby>発言<rt>はつげん</rt></ruby>をしたように<ruby>見<rt>み</rt></ruby>せかけた<ruby>偽<rt>にせ</rt></ruby><ruby>動画<rt>どうが</rt></ruby>が、<ruby>日本<rt>にほん</rt></ruby><ruby>テレビ<rt>てれび</rt></ruby>の<ruby>ニュース<rt>にゅーす</rt></ruby><ruby>番組<rt>ばんぐみ</rt></ruby>のロゴを<ruby>使<rt>つか</rt></ruby>って<ruby>編集<rt>へんしゅう</rt></ruby>され、X（<ruby>旧<rt>きゅう</rt></ruby><ruby>ツイッター<rt>ついったー</rt></ruby>）などSNS上で<ruby>拡散<rt>かくさん</rt></ruby>されている。<ruby>日<rt>にっ</rt></ruby><ruby>テレ<rt>てれ</rt></ruby>は<ruby>動画<rt>どうが</rt></ruby>について「<ruby>フェイク<rt>ふぇいく</rt></ruby><ruby>動画<rt>どうが</rt></ruby>」だとして<ruby>注意<rt>ちゅうい</rt></ruby>を<ruby>呼<rt>よ</rt></ruby>びかけている。
</p>

To see this on your computer, either paste the HTML in an app that supports Markdown (such as [Obsidian](https://obsidian.md/)) or [JSBin](https://jsbin.com) and paste the HTML between the `<body>` tags.

Try this with LLMs. This shows how ChatGPT is much better than any other LLM in this aspect.

### 2. Reading comprehension quizzes

You can also ask ChatGPT to develop a quiz that tests your comprehension of the text. You can even do the quiz interactively with ChatGPT:

```
You are Japanese tutor teaching intermediate level adult students. You are designing a quiz to test my reading comprehension of Japanese articles. The quiz has 5 questions based on an article below. The questions should test the comprehension of the article. Each question should have 1 correct answer and 3 incorrect answers. The incorrect answers cannot be too obviously wrong. One good examples for the question are:  この記事で語られている事件の詳細は何ですか ?However, you cannot use the same question in the example.

Now, ask me these questions, one after another. Prompt me to answer the question. After I answer, tell me whether I did right or wrong and why, and move on to the next question.

Here's the article:
岸田文雄首相の声と画像を使ってひわいな発言をしたように見せかけた偽動画が、日本テレビのニュース番組のロゴを使って編集され、X（旧ツイッター）などSNS上で拡散されている。日テレは動画について「フェイク動画」だとして注意を呼びかけている。

偽動画は生成AIを利用して作られたものと見られ、スーツ姿の岸田氏が、カメラに向かって語りかけている様子が収められている。さらに、日テレの「日テレNEWS24」のロゴを使い、ニュース番組で中継されているように装っている。同社は番組を通じて「放送、番組ロゴをフェイク動画に悪用されたことは到底許すことはできない」と注意を呼びかけた。

現在、生成AIを巡っては、主要7カ国（G7）の国際ルール作りを目指す「広島AIプロセス」の年内の策定に向けて議論が進んでいる。10月30日には、生成AIの開発者を対象にした「行動規範」をG7で合意。生成AIのリスクを特定し、適切な対応を実施することが盛り込まれており、リスクとして偽情報の助長やプライバシー侵害などがあげられている。（明楽麻子）
```
