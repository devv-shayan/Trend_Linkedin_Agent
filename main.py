from agents import Runner, set_trace_processors, trace
# Import agent objects directly
from agent import (
    trend_spotter_agent,
    trend_selector_agent,
    trend_analyzer_agent,
    question_asker_agent,
    brief_writer_agent,
    linkedin_post_generator_agent,
    get_trend_spotter_instructions, # Keep for now, or format directly
    get_trend_selector_instructions,
    get_trend_analyzer_instructions,
    get_question_asker_instructions,
    get_brief_writer_instructions,
    get_linkedin_post_generator_instructions,
)
from langsmith.wrappers import OpenAIAgentsTracingProcessor


def _get_initial_user_inputs():
    """Gets the current date and niche from the user."""
    current_date = input("Enter the current date (e.g., YYYY-MM-DD): ")
    niche = input("Enter the niche for trend spotting: ")
    return current_date, niche


def run_trend_to_post_pipeline():
    print("--- Trend to LinkedIn Post Agent Pipeline ---")

    # 1. Get initial inputs from user
    current_date, niche = _get_initial_user_inputs()

    print("\n--- Step 1: Trend Spotting ---")
    # Format instructions at runtime
    trend_spotter_agent.instructions = get_trend_spotter_instructions(current_date, niche)
    trend_spotter_result = Runner.run_sync(
        starting_agent=trend_spotter_agent,
        input="Identify current trends based on your instructions.", # Input can be minimal if instructions are comprehensive
    )

    if not trend_spotter_result or not trend_spotter_result.final_output:
        print("TrendSpotterAgent failed to return output. Exiting.")
        return

    print(f"TrendSpotter Output:\n{trend_spotter_result.final_output}")
    potential_trends_str = trend_spotter_result.final_output

    print("\n--- Step 2a: Trend Selection ---")
    trend_selector_agent.instructions = get_trend_selector_instructions(potential_trends_str)
    trend_selector_result = Runner.run_sync(
        starting_agent=trend_selector_agent, input="Select the most promising trend based on the provided list."
    )

    if not trend_selector_result or not trend_selector_result.final_output:
        print("TrendSelectorAgent failed to return output. Exiting.")
        return

    selected_trend = (
        trend_selector_result.final_output.strip()
    )
    print(f"TrendSelector Output (Selected Trend):\n{selected_trend}")

    print("\n--- Step 2b: Trend Analysis ---")
    if not selected_trend:
        print("No trend was selected by TrendSelectorAgent. Exiting.")
        return

    trend_analyzer_agent.instructions = get_trend_analyzer_instructions(selected_trend)
    trend_analyzer_result = Runner.run_sync(
        starting_agent=trend_analyzer_agent,
        input=f"Provide a detailed analysis for the trend: {selected_trend}", # Input can reiterate if needed
    )

    if not trend_analyzer_result or not trend_analyzer_result.final_output:
        print("TrendAnalyzerAgent failed to return output. Exiting.")
        return

    detailed_analysis = trend_analyzer_result.final_output
    print(f"TrendAnalyzer Output (Detailed Analysis):\n{detailed_analysis}")

    print("\n--- Step 3: Formulating User Questions ---")
    question_asker_agent.instructions = get_question_asker_instructions(detailed_analysis)
    question_asker_result = Runner.run_sync(
        starting_agent=question_asker_agent,
        input="Present the analysis and formulate questions for the user based on your instructions.",
    )

    if not question_asker_result or not question_asker_result.final_output:
        print("QuestionAskerAgent failed to return output. Exiting.")
        return

    print(f"QuestionAsker Output:\n{question_asker_result.final_output}")

    # 4. Get user input based on questions presented
    questions_map = {
        "1": "How can this post relate to me personally?",
        "2": "How can this post relate to my business?",
        "3": "What is a controversial take you have on this?",
        "4": "How can this post play on a psychological effect from 'Made to Stick'?",
    }

    valid_choices = set(questions_map.keys())
    selected_nums = []
    while not selected_nums:
        choice_input = input(
            "Enter the numbers of the questions you want to answer (e.g., '1,3'): "
        ).strip()
        selected_nums = [num.strip() for num in choice_input.split(",") if num.strip()]
        invalid = [num for num in selected_nums if num not in valid_choices]
        if invalid or not selected_nums:
            print(
                "Invalid selection. Please choose one or more numbers between 1 and 4, separated by commas (e.g., '1,3')."
            )
            selected_nums = []

    user_answers_map = {}
    print("\nPlease provide your answers to the selected questions one by one.")
    for i, num in enumerate(selected_nums):
        q_text = questions_map[num]
        answer_prompt = (
            f"\n--- Answering Question {num} ---\nQuestion: '{q_text}'\nYour answer: "
        )
        answer = input(answer_prompt)
        user_answers_map[num] = answer
        print(f"Answer for question {num} received.")

    user_chosen_question_text = "; ".join([questions_map[num] for num in selected_nums])
    user_answer = "\n".join(
        [f"{questions_map[num]}: {user_answers_map[num]}" for num in selected_nums]
    )

    print("\n--- Step 5: Brief Writing ---")
    brief_writer_agent.instructions = get_brief_writer_instructions(
        detailed_analysis, user_chosen_question_text, user_answer
    )
    brief_writer_result = Runner.run_sync(
        starting_agent=brief_writer_agent,
        input="Generate a brief based on the analysis and user input, following your instructions.",
    )

    if not brief_writer_result or not brief_writer_result.final_output:
        print("BriefWriterAgent failed to return output. Exiting.")
        return

    brief = brief_writer_result.final_output
    print(f"BriefWriter Output (Brief):\n{brief}")

    print("\n--- Step 6: LinkedIn Post Generation ---")
    linkedin_post_generator_agent.instructions = get_linkedin_post_generator_instructions(brief)
    linkedin_post_result = Runner.run_sync(
        starting_agent=linkedin_post_generator_agent,
        input="Generate the LinkedIn post from the brief, adhering to your specific instructions.",
    )

    if not linkedin_post_result or not linkedin_post_result.final_output:
        print("LinkedInPostGeneratorAgent failed to return output. Exiting.")
        return

    final_post = linkedin_post_result.final_output
    print(f"\n--- Generated LinkedIn Post ---:\n{final_post}")


if __name__ == "__main__":
    set_trace_processors([OpenAIAgentsTracingProcessor()])
    with trace("Trend to LinkedIn Post Pipeline"):
        run_trend_to_post_pipeline()
