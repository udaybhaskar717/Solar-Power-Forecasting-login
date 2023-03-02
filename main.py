import streamlit as st
from github import Github
import json

# Set up GitHub credentials
ACCESS_TOKEN = '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'
g = Github(ACCESS_TOKEN)

# Define functions for creating and retrieving data from repository
def create_repo(username, repo_name):
    user = g.get_user(username)
    user.create_repo(repo_name)
    
def get_data(username, repo_name, filename):
    repo = g.get_user(username).get_repo(repo_name)
    contents = repo.get_contents(filename)
    data = json.loads(contents.decoded_content)
    return data

def save_data(username, repo_name, filename, data):
    repo = g.get_user(username).get_repo(repo_name)
    repo.create_file(filename, "signup data", json.dumps(data))

# Define Streamlit app
def app():
    st.title("Sign-up and Forecast App")
    
    # Sign-up form
    st.subheader("Sign-up")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Sign up"):
        # Create repository if it doesn't exist
        try:
            create_repo("your_github_username", "signup-data")
        except:
            pass
        
        # Save sign-up data to repository
        data = {"name": name, "email": email, "password": password}
        save_data("your_github_username", "signup-data", "signup.json", data)
        
        st.success("Sign-up successful! Please log in.")
    
    # Log-in form
    st.subheader("Log in")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Log in"):
        # Retrieve sign-up data from repository
        try:
            data = get_data("your_github_username", "signup-data", "signup.json")
        except:
            st.error("Log-in failed. Please sign up first.")
            return
        
        # Authenticate user
        if data["email"] == email and data["password"] == password:
            st.success("Log-in successful!")
            
            # Forecast page
            st.subheader("Forecast")
            # Add code for forecasting here
            
        else:
            st.error("Log-in failed. Please check your email and password.")
if __name__ == '__main__':
    app()

