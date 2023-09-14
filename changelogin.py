import yaml
from getpass import getpass
import bcrypt
import streamlit as st
import streamlit_authenticator as stauth
import time
from mojafunkcja import st_style

st_style()


def change_password(username, old_password, new_password):

    # Load existing YAML data from file
    with open("config.yaml", "r") as file:
        data = yaml.safe_load(file)
    if username not in data["credentials"]["usernames"]:
        return False
    # Get the user's hashed password from the YAML data
    hashed_password = data["credentials"]["usernames"][username]["password"]

    # Verify the old password
    if bcrypt.checkpw(old_password.encode(), hashed_password.encode()):
        # Generate hashed password for the new password
        salt = bcrypt.gensalt()
        new_hashed_password = bcrypt.hashpw(
            new_password.encode(), salt).decode()

        # Update the user's hashed password in the YAML data
        data["credentials"]["usernames"][username]["password"] = new_hashed_password

        # Write updated YAML data to file
        with open("config.yaml", "w") as file:
            yaml.dump(data, file, default_flow_style=False)

        return True
    else:
        return False


def main():

    st.subheader('Change Password')
    placeholder = st.empty()
    st.session_state['question'] = ''

    with placeholder.form(key='my_form', clear_on_submit=True):

        # Prompt user for change password
        username = st.text_input("Enter username: ")
        old_password = st.text_input("Enter old password: ", type="password")
        new_password = st.text_input("Enter new password: ", type="password")
        change_password_button = st.form_submit_button(label='Change Password')

        if change_password_button:
            # Prompt user for username and old/new passwords
            if new_password:

                # Attempt to change the password
                password_changed = change_password(
                    username, old_password, new_password)

                # Display success/error message
                if password_changed:
                    alert = st.success("Password changed successfully.")
                    time.sleep(2)
                    alert.empty()
                else:
                    st.error(
                        "Failed to change password. Please check your username and old password.")


if __name__ == "__main__":
    main()


