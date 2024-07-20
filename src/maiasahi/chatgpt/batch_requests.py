MODEL = "gpt-4o-mini-2024-07-18"


def create_batch_request(
    id: str,
    system: str | None = None,
    user: str | None = None,
    temperature: float = 0.2,
) -> dict:
    """Create an OpenAI prompt with system and user messages."""
    if not system and not user:
        raise ValueError("At least one of system or user messages must be provided.")

    messages = []

    if system:
        messages.append({"role": "system", "content": system})
    if user:
        messages.append({"role": "user", "content": user})

    return {
        "custom_id": id,
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": MODEL,
            "messages": messages,
            "temperature": temperature,
        },
    }


def create_paragraph_annotation_request(id: str, paragraph: str) -> dict:
    """Generates one batch request for annotating a paragraph."""
    system = """You are an app that annotates furigana using <ruby> and <rt> tags. For example, if the paragraph is <p>ビートルズの「最後の曲」とされる「ナウ・アンド・ゼン」が日本時間2日午後11時にデジタル配信で発売された。</p>

    Then the response should be <p><ruby>ビートルズ<rt>びーとるず</rt></ruby>の「<ruby>最後<rt>さいご</rt></ruby>の<ruby>曲<rt>きょく</rt></ruby>」とされる「<ruby>ナウ・アンド・ゼン<rt>なう・あんど・ぜん</rt></ruby>」が<ruby>日本<rt>にほん</rt></ruby><ruby>時間<rt>じかん</rt></ruby>2<ruby>日<rt>にち</rt></ruby><ruby>午後<rt>ごご</rt></ruby>11<ruby>時<rt>じ</rt></ruby>に<ruby>デジタル<rt>でじたる</rt></ruby><ruby>配信<rt>はいしん</rt></ruby>で<ruby>発売<rt>はつばい</rt></ruby>された。</p>
    """

    prompt = f"Now annotate this paragraph: <p>{paragraph}</p>. Your response should be HTML with matching <ruby> and <rt> tags for all words and phrases."

    return create_batch_request(id, system, prompt, temperature=0.2)


def create_article_annotation_request(article: str) -> list[dict]:
    """Annotate an article with ChatGPT by paragraph."""
    paragraphs = [p.strip() for p in article.split("\n\n")]
    paragraph_annotation_requests = [
        create_paragraph_annotation_request(f"annotate-p{idx}", paragraph)
        for idx, paragraph in enumerate(paragraphs)
    ]

    return paragraph_annotation_requests


def create_title_annotation_request(title: str) -> dict:
    """Create a batch request to annotate a title with ChatGPT."""
    system = "You are an app that helps intermediate and advanced Japanese learners learn intermediate and advanced level vocabulary."
    prompt = f"""{title}
    
    Translate the above sentence from Japanese into English.
    """

    return create_batch_request("title", system, prompt)


def create_vocabulary_request(article: str) -> dict:
    """Create a batch request to find a list of vocabulary in the article with ChatGPT."""
    system = "You are an app that helps intermediate and advanced Japanese learners learn intermediate and advanced level vocabulary."
    prompt = f"""From the article below, find 30 intermediate and advanced words that are at JLPT N1, N2, and N3 levels.  Focus on verbs, adjectives, and adverbs. Make sure to combine all results in one markdown table with the following columns:

    1. Word: write each word in dictionary form with furigana in parentheses next to it
    2. JLPT Level: whether they are JLPT N5, N4, N3, N2, or N1 words
    3. Part of speech: for adjectives, be specific about whether they are い-adjectives or な-adjectives. For verbs, be specific about whether they are ichidan, godan, or irregular verbs
    4. Meaning: write in lower case.

    <article>
    {article}
    </article>

    Your response should be the markdown only. Do not put it in a code block.
    """

    return create_batch_request("vocabulary", system, prompt)


def create_grammar_request(article: str) -> dict:
    """Create a batch request to find a list of grammar in the article with ChatGPT."""
    system = "You are an app that helps intermediate and advanced Japanese learners learn intermediate and advanced level grammar."
    prompt = f"""
    {article}

    In the above article, select 3 sentences that are difficult to understand. For each sentence, do the following:

    1. explain grammatical points
    2. explain the structure of the sentence

    Your response should be the markdown only. Do not put it in a code block.
    """

    return create_batch_request("grammar", system, prompt)


def create_quiz_request(article: str) -> dict:
    """Create a batch request to generate a quiz with ChatGPT."""
    system = "You are a Japanese tutoring app teaching intermediate level adult students. You are designing a quiz to test reading comprehension of Japanese articles. Do not format your answer in Markdown."
    prompt = f"""The quiz has 5 questions based on an article below. The questions should test the comprehension of the article. Each question should have one correct answer and three incorrect answers. The incorrect answers cannot be too obviously wrong, and the order of the options should be random. One good examples for the question is:  この記事で語られている事件の詳細は何ですか？ However, you cannot use the same question in the example. 

    Here's the article:

    {article}

    I want the quiz as an array of JSON objects with the following field: 
    1. question: the question itself,
    2. options: an array of 4 options,
    3. answer: the index of the correct answer in the options array
    4. explanation, which is an explanation of the correct answer.

    Your response should be nothing but the array. Do not format your answer in Markdown.
    """

    return create_batch_request("quiz", system, prompt)


def create_all_requests(title, article) -> list[dict]:
    """Create all batch requests for a title and article."""

    batch_requests = create_article_annotation_request(article)

    batch_requests.append(create_title_annotation_request(title))
    batch_requests.append(create_vocabulary_request(article))
    batch_requests.append(create_grammar_request(article))
    batch_requests.append(create_quiz_request(article))

    return batch_requests
