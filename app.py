# Libraries
import base64
import sqlite3

import streamlit as st
from openai import OpenAI

max_requests = 10


# Function to initialize the database only if it doesn't exist
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        uses_available INTEGER DEFAULT 10,
        active INTEGER DEFAULT 1
    )
    """)

    # Insert initial users if they do not exist
    initial_users = [
        ("demo1", st.secrets.demo_credentials.demo1, max_requests, 1),
        ("demo2", st.secrets.demo_credentials.demo2, max_requests, 1),
        ("demo3", st.secrets.demo_credentials.demo3, max_requests, 1),
        ("demo4", st.secrets.demo_credentials.demo4, max_requests, 1),
        ("demo5", st.secrets.demo_credentials.demo5, max_requests, 1),
        ("demo6", st.secrets.demo_credentials.demo6, max_requests, 1),
        ("demo7", st.secrets.demo_credentials.demo7, max_requests, 1),
        ("demo8", st.secrets.demo_credentials.demo8, max_requests, 1),
        ("demo9", st.secrets.demo_credentials.demo9, max_requests, 1),
        ("demo10", st.secrets.demo_credentials.demo10, max_requests, 1),
        ("demo11", st.secrets.demo_credentials.demo11, max_requests, 1),
        ("demo12", st.secrets.demo_credentials.demo12, max_requests, 1),
        ("demo13", st.secrets.demo_credentials.demo13, max_requests, 1),
        ("demo14", st.secrets.demo_credentials.demo14, max_requests, 1),
        ("demo15", st.secrets.demo_credentials.demo15, max_requests, 1),
        ("demo16", st.secrets.demo_credentials.demo16, max_requests, 1),
        ("demo17", st.secrets.demo_credentials.demo17, max_requests, 1),
        ("demo18", st.secrets.demo_credentials.demo18, max_requests, 1),
        ("demo19", st.secrets.demo_credentials.demo19, max_requests, 1),
        ("demo20", st.secrets.demo_credentials.demo20, max_requests, 1),
    ]

    for user in initial_users:
        cursor.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?)", user)

    conn.commit()
    conn.close()


# Call the init_db function once when the script starts
init_db()


# Load secrets and client configurations
client = OpenAI(api_key=st.secrets.openai_credentials.OPENAI_API_KEY)
fine_tuned_model_id = st.secrets.openai_credentials.ID_MODEL_OPENAI


system_message = """
You are an advanced assistant specialized in analyzing and detecting emotions in short text. 
Your role is to identify the underlying emotion conveyed in each input and provide the most accurate emotional classification between: shame, sadness, joy, guilt, fear, disgust and anger"
"""


# Function to create the user message (prompt) for emotion detection
def create_user_message(input_text: str) -> str:
    """
    Creates a formatted user prompt for emotion detection.

    Args:
        input_text (str): The text input from the user.

    Returns:
        str: A formatted string prompt for the model.
    """
    if not isinstance(input_text, str):
        raise TypeError("input_text must be a string.")
    return f"Text: {input_text}\n\nWhat is the emotion expressed in this text?"


def detect_emotion(
    input_text: str, system_message: str, fine_tuned_model_id: str
) -> str:
    """
    Detects the emotion expressed in the given text using a fine-tuned model.

    Args:
        input_text (str): The text input from the user.
        system_message (str): The system message providing context for the model.
        fine_tuned_model_id (str): The ID of the fine-tuned model to use.

    Returns:
        str: The detected emotion.

    Raises:
        TypeError: If any of the inputs are not strings.
    """
    # Input type checking
    if not all(
        isinstance(arg, str)
        for arg in [input_text, system_message, fine_tuned_model_id]
    ):
        raise TypeError("All inputs must be strings.")

    # Prepare messages for the model
    input_message = []
    input_message.append({"role": "system", "content": system_message})
    user_input_text = create_user_message(input_text)
    input_message.append({"role": "user", "content": user_input_text})

    # Call the OpenAI API to get the response
    response = client.chat.completions.create(
        model=fine_tuned_model_id, messages=input_message, temperature=0, max_tokens=4
    )

    # Extract the emotion from the response
    emotion = response.choices[0].message.content.strip()

    # Output type checking
    if not isinstance(emotion, str):
        raise TypeError("The response from the model is not a string.")

    return emotion


emotion_emojis = {
    "joy": "😊",
    "fear": "😨",
    "disgust": "🤢",
    "guilt": "😔",
    "shame": "😳",
    "sadness": "😢",
    "anger": "😡",
}


# Login function
def login():
    logo_url = "logo/DELTA-WITS-LOGO-WHITE.png"
    try:
        with open(logo_url, "rb") as image_file:
            logo_base64 = base64.b64encode(image_file.read()).decode("utf-8")
        # Responsive styling for the title and logo
        st.markdown(
            f"""
            <style>
                /* Responsive styling for mobile */
                @media (max-width: 600px) {{
                    .title-logo-container h1 {{
                        font-size: 1.5em; /* Smaller font size for mobile */
                        text-align: center; /* Center-align title */
                    }}
                    .title-logo-container img {{
                        width: 150px; /* Reduce logo size */
                        margin-top: 10px;
                    }}
                    .title-logo-container {{
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                    }}
                }}

                /* Default styling for larger screens */
                .title-logo-container {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    max-width: 700px;
                    margin: auto;
                    padding-top: 18px;
                }}
                .title-logo-container h1 {{
                    margin: 0;
                    font-size: 2.5em;
                    font-weight: bold;
                    color: white;
                }}
                .title-logo-container img {{
                    width: 200px;
                }}
            </style>

            <div class="title-logo-container">
                <h1>Login</h1>
                <a href="https://www.deltawits.com" target="_blank">
                    <img src="data:image/png;base64,{logo_base64}" alt="Logo"/>
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )
    except FileNotFoundError:
        st.error("Logo image not found. Please check the file path.")

    st.write("Please enter your credentials to access the demo.")

    with st.form("login_form", clear_on_submit=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")

    if login_button:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT password, uses_available, active FROM users WHERE username = ?",
            (username,),
        )
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            db_password, uses_available, active = user_data
            if password == db_password and active == 1:
                st.session_state["authenticated"] = True
                st.session_state["remaining_queries"] = uses_available
                st.session_state["username"] = username
                st.success(f"Welcome, {username}!")
                st.rerun()  # Automatically go to the demo page
            elif active == 0:
                st.error("You have no remaining uses in this accout.")
            else:
                st.error("Invalid username or password.")
        else:
            st.error("Invalid username or password.")


# Main function
def main():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        login()
    else:
        logo_url = "logo/DELTA-WITS-LOGO-WHITE.png"
        try:
            with open(logo_url, "rb") as image_file:
                logo_base64 = base64.b64encode(image_file.read()).decode("utf-8")
        except FileNotFoundError:
            st.error("Logo image not found. Please check the file path.")
            return

        st.markdown(
            f"""
            <style>
                /* Responsive styling for mobile */
                @media (max-width: 600px) {{
                    .title-logo-container h1 {{
                        font-size: 1.5em;
                        text-align: center;
                    }}
                    .title-logo-container img {{
                        width: 150px;
                        margin-top: 10px;
                    }}
                    .title-logo-container {{
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                    }}
                }}

                /* Default styling for larger screens */
                .title-logo-container {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    max-width: 700px;
                    margin: auto;
                    padding-top: 10px;
                }}
                .title-logo-container h1 {{
                    margin: 0;
                    font-size: 2.5em;
                    font-weight: bold;
                    color: white;
                }}
                .title-logo-container img {{
                    width: 200px;
                }}
            </style>

            <div class="title-logo-container">
                <h1>Janus</h1>
                <a href="https://www.deltawits.com" target="_blank">
                    <img src="data:image/png;base64,{logo_base64}" alt="Logo"/>
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style="max-width: 700px; margin: auto; color: white; font-size: 1.1em; margin-bottom: 15px;">
                Experience the power of AI with our LLM based demo app! Efficiently identify emotions in texts through seven distinct emotions: joy, fear, disgust, guilt, shame, sadness, and anger.
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.session_state["remaining_queries"] > 0:
            with st.container():
                with st.form(key="emotion_form"):
                    # Text area for user input
                    user_input = st.text_area(
                        "Enter your text here:", placeholder="Insert text in English"
                    )

                    # Display remaining requests count inside the form
                    remaining_requests_placeholder = st.empty()
                    remaining_requests_placeholder.markdown(
                        f"""
                        <div style="text-align: right; color: gray; font-size: 0.9em;">
                            Remaining requests: {st.session_state["remaining_queries"]}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # Submit button
                    submit_button = st.form_submit_button(label="Analyze")

                if submit_button and user_input:
                    st.session_state["remaining_queries"] -= 1
                    conn = sqlite3.connect("users.db")
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE users SET uses_available = ?, active = ? WHERE username = ?",
                        (
                            st.session_state["remaining_queries"],
                            1 if st.session_state["remaining_queries"] > 0 else 0,
                            st.session_state["username"],
                        ),
                    )
                    conn.commit()
                    conn.close()

                    with st.spinner("Analyzing text..."):
                        try:
                            response = detect_emotion(
                                user_input, system_message, fine_tuned_model_id
                            )
                            emoji = emotion_emojis.get(response.lower(), "🔍")
                            st.markdown("### Emotion Detected:")
                            st.markdown(
                                f"<div style='background-color: #333333; padding: 10px; border-radius: 10px; color: white; font-size: 20px; text-align: center;'>{emoji} {response.capitalize()}</div>",
                                unsafe_allow_html=True,
                            )

                            # Update the remaining requests count inside the form after displaying the answer
                            remaining_requests_placeholder.markdown(
                                f"""
                                <div style="text-align: right; color: gray; font-size: 0.9em; padding-right: 10px;">
                                    Remaining requests: {st.session_state["remaining_queries"]}
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                        except Exception as e:
                            st.error(f"An error occurred: {e}")

        else:
            st.warning(
                "You have reached the maximum number of queries for this account."
            )


if __name__ == "__main__":
    main()
