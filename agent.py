import os
from agents import Agent
import prompts
from model import model
from dotenv import load_dotenv, find_dotenv
from tools import search # Import the search tool

load_dotenv(find_dotenv())


# --- Agent Definitions ---
# Directly defining agents as per SDK examples

trend_spotter_agent = Agent(
    name="TrendSpotter",
    model=model,
    instructions=prompts.FIRST_PROMPT_TEMPLATE,
    tools=[search],
)

trend_selector_agent = Agent(
    name="TrendSelector",
    model=model,
    instructions=prompts.TREND_SELECTOR_PROMPT_TEMPLATE,
)

trend_analyzer_agent = Agent(
    name="TrendAnalyzer",
    model=model,
    instructions=prompts.TREND_ANALYZER_PROMPT_TEMPLATE,
    tools=[search],
)

question_asker_agent = Agent(
    name="QuestionAsker",
    model=model,
    instructions=prompts.USER_QUESTIONS_PROMPT_TEMPLATE,
)

brief_writer_agent = Agent(
    name="BriefWriter",
    model=model,
    instructions=prompts.BRIEF_WRITER_PROMPT_TEMPLATE,
)

linkedin_post_generator_agent = Agent(
    name="LinkedInPostGenerator",
    model=model,
    instructions=prompts.LINKEDIN_POST_GENERATOR_PROMPT_TEMPLATE,
)


# --- Helper functions to format instructions (can be moved to prompts.py or utils.py if preferred) ---
# These are kept here for now if agents need dynamic instruction formatting before run time,
# otherwise, the templates can be formatted directly in main.py when calling Runner.run_sync

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
