import sys
import streamlit as st

# Define a custom stream class that redirects to st.write()


class StreamlitRedirect:
    def write(self, text):
        st.write(text)


# Create an instance of the custom stream class
st_redirect = StreamlitRedirect()

# Save the original sys.stdout for later restoration
original_stdout = sys.stdout

# Redirect sys.stdout to the custom stream class
sys.stdout = st_redirect

# Now, print statements will be redirected to st.write()
print("This will be written using st.write()")

# Restore sys.stdout to its original value
sys.stdout = original_stdout


