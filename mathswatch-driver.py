from selenium import webdriver
import openai

# Prompt the user for their OpenAI API key
api_key = input("Enter your OpenAI API key: ")

# Set the OpenAI API key
openai.api_key = api_key

# Prompt the user for their login credentials
username = input("Enter your Mathswatch username: ")
password = input("Enter your Mathswatch password: ")

# Create a webdriver
driver = webdriver.Firefox()

# Navigate to the Mathswatch login page
driver.get("https://vle.mathswatch.com/login")

# Enter the login credentials
driver.find_element_by_id("Username").send_keys(username)
driver.find_element_by_id("Password").send_keys(password)

# Submit the login form
driver.find_element_by_id("loginButton").click()

# Wait for the page to load
driver.implicitly_wait(10)

# Navigate to the assignment page
driver.get("https://vle.mathswatch.com/student-assignments")

# Wait for the page to load
driver.implicitly_wait(10)

# Get a list of assignments
assignments = driver.find_elements_by_css_selector(".assignment-item")

# Iterate over the assignments
for assignment in assignments:
    # Click on the assignment
    assignment.click()

    # Wait for the page to load
    driver.implicitly_wait(10)

    # Get a list of questions
    questions = driver.find_elements_by_css_selector(".question")

    # Iterate over the questions
    for question in questions:
        # Find the question text
        question_text = question.find_element_by_css_selector(".question-text").text

        # Use the OpenAI API to generate an answer
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"{question_text}\n\n",
            max_tokens=1024,
            temperature=0.5,
        )

        # Enter the answer
        question.find_element_by_css_selector(".question-input").send_keys(response["choices"][0]["text"])

# Submit the assignment
driver.find_element_by_css_selector(".submit-button").click()

# Close the webdriver
driver.close()
