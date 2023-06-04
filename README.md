# QuizGPT

This is a quiz application powered by ChatGPT. The goal of the application is to allow users to interact with the app though a series of questions and answers. QuizGPT has an adaptive difficulty with every 5 questions when user gets the pervious questions correct, difficulty increases and vice versa.

# Design Decisions

1. ChatGPT API is used as it is well documented and has a cummunity for resolving the errors encounted during development.
2. ChatGPT sends the question, options, correct option, and explaination of the correct option. I used the user answer to match with the correct option rather than sending it to ChatGPT as it was slow due to latency in the API calls.
3. Subject matter is general knowledge, which is relatively suitalbe for a general audience. 
4. Difficulty levels ranges from 1 to 10, easiest to hardest respectively. 
5. I used streamlit for easy and clean implementation of the UI and to host the app.


# Challenges

1. Understanding ChatGPT API from their documentation is not clear as they have few examples.
```
Approach: Read few blog post and also few ChatGPT code examples to understand various APIs and their parameters.
```
2. Latency in the question generation.
```
Approach: There is a noticable latency when we go to next question or load a question due to the API response. So, I load 5 questions if user clicks on next button or if it is start of the quiz.
```
3. ChatGPT RateError.
```
Approach: Reload the application as load/send the request again resolves the rate error issue as load reduces after few milliseconds.
```
4. Decoding Error with ChatGPT response.
```
Approach: Sometimes I encountered JSONDecodError when the question didn't follow the API response contract, I just dropped that question and continue with others.
```
4. Adaptive difficulty is not measurable from ChatGPT response. The same questions come in different difficulty levels in quiz.
5.  Loading questions asynchronous in the UI.