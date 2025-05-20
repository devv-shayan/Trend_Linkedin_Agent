FIRST_PROMPT_TEMPLATE = """You are a trend-spotting expert, focused on identifying the most current and viral topics as of today ({date}), strictly about [{niche}].

I want you to surface topics that:
- Emerged today, yesterday, or within the last few days of this month.
(← Are timely and specific, not generic truths or evergreen advice.)
- Could inspire a journalist's article or a news segment.

Focus on:
- Recent case studies,
- Breakthrough success stories,
- Notable opinion shifts,
- Or clear changes in user or platform behavior.

Avoid vague trends.
Think headlines, not platitudes.
Your output should be a list of identified trend topics, each on a new line.
"""

USER_QUESTIONS_PROMPT_TEMPLATE = """You have the following detailed trend analysis:
{trend_analysis}

Based on the analysis above, ask the user only these key questions so they can:
- make this post relate to them personally
- make this post relate to their business
- make sure they have a controversial take on it
- make sure it plays on a psychological effect from Made to Stick

Number these questions and ask the user to select one or more to answer (e.g., '1,3').
"""

BRIEF_WRITER_PROMPT_TEMPLATE = """You are given:
1. A detailed trend analysis:
{trend_analysis}

2. The user's chosen question to focus on:
'{user_chosen_question_text}'

3. The user's answer/take:
'{user_answer}'

Your task is to write a brief instead with 1) the information from the trend analysis 2) the user take on it.
"""

LINKEDIN_POST_GENERATOR_PROMPT_TEMPLATE = """You are a LinkedIn post generation expert. Based on the provided brief:
{brief}

Write an engaging and professional LinkedIn post.
That should be a single post suitable for LinkedIn following this template

TEMPLATE:
[Opening Hook / Question]

[Your Quick Answer]

[Transition to Reflection]

[Core Insight]

[Your Origin Story]

[Plot Twist / "Hilarious" Contrast]

[Lesson Learned]

[Call to Action / Advice]

[Recent Example / Anecdote]

P.S.: [Fun aside or safety joke]


EXAMPLE:
What makes you sick?

If someone asks me this today, I'll say the idea of being dependent on someone.

- Relying on someone for my basic needs.
- Expecting someone to buy the things I want.
- Or simply having to ask someone to drop me off somewhere.

When I look at myself now, I feel proud of how far I've come.

- Not because I have the perfect job, I don't.
- Not because I've scored the highest marks in my degree, I haven't.
- And not because I've achieved everything I dreamed of, I'm still on the journey.

I feel proud because I'm growing.
I'm working on myself, for myself and for the people around me.

From a little girl who dreamed of earning for herself,
To a woman who now buys what she wants for herself and her loved ones.

Life hasn't gone the way I planned,
For example I wanted to a Dr and now I am studying engineering.

Hilarious right?

But But it has still been nothing short of amazing.

Not because things were spoon-fed to me.

But because I always believed I could achieve what I manifested and worked for.

To the girls waiting for a prince charming,
No one's coming to save you.

And even if someone does, you never know what fate holds.

So start working for yourself before it's too late.

Recently, I started riding a scooty.
And let me tell you, there's nothing more Fascinating than being the one in control,
Instead of being a passenger princess.

P.s: If you see me somewhere, change the lane because it's better to be safe than sorry.

Haha I am kidding.

P.s.s: Do you know the line written on my picture?

It's from a famous novel.

~ Your Storyteller from Kashmir.

"""

TREND_SELECTOR_PROMPT_TEMPLATE = """From the following list of trend topics:
{trend_list_str}

Select the single most promising trend topic that could inspire a journalist's article or a news segment.
Your output should be ONLY the name of the selected trend topic.
"""

TREND_ANALYZER_PROMPT_TEMPLATE = """You are given the following trend topic:
{selected_trend_topic}

Your task is to perform a deep analysis of this trend. Use your search capabilities to gather the latest information.
Then, provide a detailed analysis focusing on:
- The angle: What's the specific viewpoint or hook?
- The emotion: What feelings does this trend evoke or tap into?
- The potentially controversial take: Is there a challenging or debatable aspect?
- How the world changed: What shift or development does this trend represent?
- The unique insight: What fresh perspective or understanding would make content about this stand out?

Structure your output clearly, addressing each of these points for the given trend.
Start your response with "Detailed Analysis for Trend: [The Trend Topic]"
"""
