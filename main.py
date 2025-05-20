from agents import Runner, set_trace_processors, trace
import agent
from langsmith.wrappers import OpenAIAgentsTracingProcessor



def run_trend_to_post_pipeline():
    print("--- Trend to LinkedIn Post Agent Pipeline ---")

    # 1. Get initial inputs from user
    current_date = input("Enter the current date (e.g., YYYY-MM-DD): ")
    niche = input("Enter the niche for trend spotting: ")
    
    print("\n--- Step 1: Trend Spotting ---")
    trend_spotter_agent = agent.create_trend_spotter_agent(current_date, niche)
    # The input string for run_sync can be a general instruction if the main task is in agent.instructions
    trend_spotter_result = Runner.run_sync(starting_agent=trend_spotter_agent, input="Identify current trends based on your instructions.")
    
    if not trend_spotter_result or not trend_spotter_result.final_output:
        print("TrendSpotterAgent failed to return output. Exiting.")
        return
    
    print(f"TrendSpotter Output:\n{trend_spotter_result.final_output}")
    potential_trends_str = trend_spotter_result.final_output
    
    print("\n--- Step 2: Trend Refinement & Analysis ---")
    trend_refiner_agent = agent.create_trend_refiner_agent(potential_trends_str)
    trend_refiner_result = Runner.run_sync(starting_agent=trend_refiner_agent, input="Select the most promising trend and provide a detailed analysis.")
    
    if not trend_refiner_result or not trend_refiner_result.final_output:
        print("TrendRefinerAgent failed to return output. Exiting.")
        return

    detailed_analysis = trend_refiner_result.final_output
    print(f"TrendRefiner Output (Detailed Analysis):\n{detailed_analysis}")

    print("\n--- Step 3: Formulating User Questions ---")
    question_asker_agent = agent.create_question_asker_agent(detailed_analysis)
    question_asker_result = Runner.run_sync(starting_agent=question_asker_agent, input="Present the analysis and formulate questions for the user.")
    
    if not question_asker_result or not question_asker_result.final_output:
        print("QuestionAskerAgent failed to return output. Exiting.")
        return

    print(f"QuestionAsker Output:\n{question_asker_result.final_output}")
    
    # 4. Get user input based on questions presented
    questions_map = {
        "1": "How can this post relate to me personally?",
        "2": "How can this post relate to my business?",
        "3": "What is a controversial take you have on this?",
        "4": "How can this post play on a psychological effect from 'Made to Stick'?"
    }
    
    # Allow the user to select one or more questions by number (e.g., '1,3')
    valid_choices = set(questions_map.keys())
    selected_nums = []
    while not selected_nums:
        choice_input = input("Enter the numbers of the questions you want to answer (e.g., '1,3'): ").strip()
        selected_nums = [num.strip() for num in choice_input.split(',') if num.strip()]
        invalid = [num for num in selected_nums if num not in valid_choices]
        if invalid or not selected_nums:
            print("Invalid selection. Please choose one or more numbers between 1 and 4, separated by commas (e.g., '1,3').")
            selected_nums = []
    # Prompt user for each selected question
    user_answers_map = {}
    print("\nPlease provide your answers to the selected questions one by one.")
    for i, num in enumerate(selected_nums):
        q_text = questions_map[num]
        answer_prompt = f"\n--- Answering Question {num} ---\nQuestion: '{q_text}'\nYour answer: "
        answer = input(answer_prompt)
        user_answers_map[num] = answer
        print(f"Answer for question {num} received.")
    
    # Combine selected questions and answers for the brief writer
    user_chosen_question_text = "; ".join([questions_map[num] for num in selected_nums])
    user_answer = "\n".join([f"{questions_map[num]}: {user_answers_map[num]}" for num in selected_nums])

    print("\n--- Step 5: Brief Writing ---")
    brief_writer_agent = agent.create_brief_writer_agent(detailed_analysis, user_chosen_question_text, user_answer)
    brief_writer_result = Runner.run_sync(starting_agent=brief_writer_agent, input="Generate a brief based on the analysis and user input.")

    if not brief_writer_result or not brief_writer_result.final_output:
        print("BriefWriterAgent failed to return output. Exiting.")
        return
        
    brief = brief_writer_result.final_output
    print(f"BriefWriter Output (Brief):\n{brief}")

    print("\n--- Step 6: LinkedIn Post Generation ---")
    linkedin_post_generator_agent = agent.create_linkedin_post_generator_agent(brief)
    linkedin_post_result = Runner.run_sync(starting_agent=linkedin_post_generator_agent, input="Generate the LinkedIn post from the brief.")

    if not linkedin_post_result or not linkedin_post_result.final_output:
        print("LinkedInPostGeneratorAgent failed to return output. Exiting.")
        return

    final_post = linkedin_post_result.final_output
    print(f"\n--- Generated LinkedIn Post ---:\n{final_post}")


if __name__ == "__main__":
    # Before running, ensure:
    # 1. You have created a virtual environment and activated it.
    #    python -m venv .venv
    #    source .venv/bin/activate  (Linux/macOS)
    #    .\.venv\Scripts\activate (Windows)
    # 2. You have installed the openai-agents SDK:
    #    pip install openai-agents
    # 3. Your OpenAI API key is set as an environment variable:
    #    export OPENAI_API_KEY='sk-...' (Linux/macOS)
    #    set OPENAI_API_KEY=sk-... (Windows CMD)
    #    $env:OPENAI_API_KEY="sk-..." (Windows PowerShell)
    
    # Note: A functional web_search_tool is required for TrendSpotterAgent.
    # This is now referenced in agents_def.py. You'd need to implement
    # or integrate such a tool for the first step to work effectively.
    set_trace_processors([OpenAIAgentsTracingProcessor()])
    # Wrap all agent runs under a single root trace
    with trace("Trend to LinkedIn Post Pipeline"):
        run_trend_to_post_pipeline()
