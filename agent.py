import os
from pyexpat import model
from agents import Agent, function_tool
import prompts
from model import model
from linkup import LinkupClient
from dotenv import load_dotenv, find_dotenv



load_dotenv(find_dotenv())


# --- Agent Instruction Helper Functions ---
def get_trend_spotter_instructions(date: str, niche: str) -> str:
    return prompts.FIRST_PROMPT_TEMPLATE.format(date=date, niche=niche)


def get_trend_selector_instructions(trend_list_str: str) -> str:
    return prompts.TREND_SELECTOR_PROMPT_TEMPLATE.format(trend_list_str=trend_list_str)


def get_trend_analyzer_instructions(selected_trend_topic: str) -> str:
    return prompts.TREND_ANALYZER_PROMPT_TEMPLATE.format(
        selected_trend_topic=selected_trend_topic
    )


def get_question_asker_instructions(trend_analysis: str) -> str:
    return prompts.USER_QUESTIONS_PROMPT_TEMPLATE.format(trend_analysis=trend_analysis)


def get_brief_writer_instructions(
    trend_analysis: str, user_chosen_question_text: str, user_answer: str
) -> str:
    return prompts.BRIEF_WRITER_PROMPT_TEMPLATE.format(
        trend_analysis=trend_analysis,
        user_chosen_question_text=user_chosen_question_text,
        user_answer=user_answer,
    )


def get_linkedin_post_generator_instructions(brief: str) -> str:
    return prompts.LINKEDIN_POST_GENERATOR_PROMPT_TEMPLATE.format(brief=brief)


# --- Agent Definitions ---
@function_tool
def search(query: str) -> str:
    """
    Search for information using the Tavily API.

    This function performs a web search using Tavily's search API to find relevant information
    based on the provided query."""

    client = LinkupClient(api_key=os.getenv("LINKUP_API_KEY"))
    response = client.search(
        query=query,
        depth="standard",
        output_type="sourcedAnswer",
        include_images=False,
    )
    return f"Here is the search result for {query}: {response}"


def create_trend_spotter_agent(date: str, niche: str) -> Agent:
    """
    Creates an agent responsible for spotting trends based on the given date and niche.
    It uses a search tool to find current and viral topics.
    """
    return Agent(
        name="TrendSpotter",
        model=model,
        instructions=get_trend_spotter_instructions(date, niche),
        tools=[search],
    )


def create_trend_selector_agent(trend_list_str: str) -> Agent:
    return Agent(
        name="TrendSelector",
        model=model,
        instructions=get_trend_selector_instructions(trend_list_str),
    )


def create_trend_analyzer_agent(selected_trend_topic: str) -> Agent:
    return Agent(
        name="TrendAnalyzer",
        model=model,
        instructions=get_trend_analyzer_instructions(selected_trend_topic),
        tools=[search],
    )


def create_question_asker_agent(detailed_analysis: str) -> Agent:
    return Agent(
        name="QuestionAsker",
        model=model,
        instructions=get_question_asker_instructions(detailed_analysis),
    )


def create_brief_writer_agent(
    detailed_analysis: str, user_chosen_question_text: str, user_answer: str
) -> Agent:
    return Agent(
        name="BriefWriter",
        model=model,
        instructions=get_brief_writer_instructions(
            detailed_analysis, user_chosen_question_text, user_answer
        ),
    )


def create_linkedin_post_generator_agent(brief: str) -> Agent:
    return Agent(
        name="LinkedInPostGenerator",
        model=model,
        instructions=get_linkedin_post_generator_instructions(brief),
    )
