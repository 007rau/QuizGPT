import json

import streamlit as st
from quiz import get_quiz_questions

# Initialize session state variables if they don't exist yet
if "questions" not in st.session_state:
    st.session_state["answers"] = {}
    st.session_state["current_question"] = 0
    st.session_state["questions"] = []
    st.session_state["right_answers"] = 0
    st.session_state["wrong_answers"] = 0
    st.session_state["difficultyLevel"] = 5
    st.session_state["score"] = 0


# Define a function to display the current question and options
def display_question():
    # Handle first case
    if len(st.session_state.questions) == 0:
        first_question = get_quiz_questions(st.session_state.difficultyLevel)
        for i in 0, 1, 2, 3, 4:
            st.session_state.questions.append(first_question[i])

    # Disable the submit button if the user has already answered this question
    submit_button_disabled = st.session_state.current_question in st.session_state.answers

    # Get the current question from the questions list
    question = st.session_state.questions[st.session_state.current_question]

    # Display the question prompt
    st.write(f"{st.session_state.current_question + 1}. {question['question']}")

    # Use an empty placeholder to display the radio button options
    options = st.empty()

    # Display the radio button options and wait for the user to select an answer
    user_answer = options.radio("Options:", question["options"], key=st.session_state.current_question)

    # Display the submit button and disable it if necessary
    submit_button = st.button("Submit", disabled=submit_button_disabled)

    # If the user has already answered this question, display their previous answer
    if st.session_state.current_question in st.session_state.answers:
        index = st.session_state.answers[st.session_state.current_question]
        options.radio(
            "Your answer:",
            question["options"],
            key=float(st.session_state.current_question),
            index=index,
        )

    # If the user clicks the submit button, check their answer and show the explanation
    if submit_button:
        # Record the user's answer in the session state
        st.session_state.answers[st.session_state.current_question] = question["options"].index(user_answer)

        # Check if the user's answer is correct and update the score
        if user_answer == question["answer"]:
            st.write("Correct!")
            st.session_state.right_answers += 1
            st.session_state.score += 1
        else:
            st.write(f"Sorry, the correct answer was {question['answer']}.")
            st.session_state.wrong_answers += 1

        # Show an expander with the explanation of the correct answer
        with st.expander("Explanation"):
            st.write(question["explanation"])

    # Display the current score and difficulty level
    st.sidebar.write(f"Score: {st.session_state.score}")
    st.sidebar.write(f"Difficulty: {st.session_state.difficultyLevel}")    

# Define a function to go to the next question
def next_question():
    # Move to the next question in the questions list
    st.session_state.current_question += 1

    # If we've reached the end of the questions list, get a new questions list with a updated difficulty level
    if st.session_state.current_question > len(st.session_state.questions) - 1:
        st.session_state.difficultyLevel = min(10, max(1, st.session_state.difficultyLevel + st.session_state.right_answers - st.session_state.wrong_answers))
        st.session_state.right_answers = 0
        st.session_state.wrong_answers = 0
        next_question = get_quiz_questions(st.session_state.difficultyLevel)
        for i in 0, 1, 2, 3, 4:
            st.session_state.questions.append(next_question[i])

# Define a function to go to the previous question
def prev_question():
    # Move to the previous question in the questions list
    if st.session_state.current_question > 0:
        st.session_state.current_question -= 1
        st.session_state.explanation = None


# Create a 3-column layout for the Prev/Next buttons and the question display
col1, col2, col3 = st.columns([1, 6, 1])

# Add a Prev button to the left column that goes to the previous question
with col1:
    if col1.button("Prev"):
        prev_question()

# Add a Next button to the right column that goes to the next question
with col3:
    if col3.button("Next"):
        next_question()
    
# Display the actual quiz question
with col2:
    display_question()