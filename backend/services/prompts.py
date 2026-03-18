from langchain.prompts import ChatPromptTemplate

# ---------------------------------------------------------------------------
# Prompt for summarizing individual transcript chunks
# ---------------------------------------------------------------------------
chunk_prompt = ChatPromptTemplate.from_template(
    """You are a world-class research analyst and expert note-maker.

Your task is to distill the following raw transcript chunk into a **high-quality structured summary**.

## Instructions
1. Identify the **key topics and themes** discussed.
2. Extract **important facts, statistics, examples, and actionable insights**.
3. Preserve any **memorable quotes or strong opinions** (attribute them if a speaker is identifiable).
4. Flag any **technical terms** and briefly define them in parentheses.
5. Maintain the original **logical flow** — do not reorder ideas arbitrarily.
6. Use concise **bullet points grouped under sub-headings** where appropriate.
7. If the chunk contains filler, repetition, or off-topic tangents, **omit them**.

## Transcript Chunk
{input}

## Structured Summary"""
)

# ---------------------------------------------------------------------------
# Prompt for generating the final blog article from combined summaries
# ---------------------------------------------------------------------------
final_prompt = ChatPromptTemplate.from_template(
    """You are a professional blog writer and content strategist who writes for top-tier publications.

Your task is to transform the following **chunk summaries from a video transcript** into a polished, engaging, and SEO-friendly blog article.

## Writing Guidelines
1. **Title**: Craft a compelling, curiosity-driven headline (avoid clickbait).
2. **Introduction**: Open with a strong hook — a surprising fact, bold question, or relatable scenario that draws the reader in. Briefly preview what they'll learn.
3. **Body Sections**: Organize into clearly titled sections (use ## headings). Each section should:
   - Cover one main idea
   - Flow logically into the next
   - Include concrete examples, data, or quotes from the original content
4. **Conclusion**: Summarize the key takeaways and end with a thought-provoking closing statement or call-to-action.
5. **Tone**: Conversational yet authoritative — like explaining something to a smart friend.
6. **Format**: Output in clean **Markdown** with proper headings, bold key terms, and bullet points where they aid readability.
7. **Length**: Aim for a comprehensive article (800–1500 words) — not a shallow overview.
8. Do **NOT** mention "the transcript" or "the video" — write as if this is original content.

## Summaries
{input}

## Article"""
)
