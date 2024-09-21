
import streamlit as st
import pandas as pd
import numpy as np
import firebase_admin
from firebase_admin import credentials, firestore

import matplotlib.pyplot as plt
import uuid

# # Check if the user is logged in
# if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
#     st.error("You need to log in to access this page.")
#     st.stop()

# # If logged in, proceed to the dashboard
# st.title("Admin Dashboard")
# st.write(f"Welcome, {st.session_state['email']}!")








st.set_page_config(
    page_title="Admin Dashboard",  # Optional title for the page
    layout="wide",  # Ensures the layout is optimized for wider screens
    initial_sidebar_state="expanded"  # Ensure the sidebar is always expanded
)

# Sidebar
st.sidebar.image("/Users/apple/Downloads/logo.png", use_column_width=True)
option = st.sidebar.selectbox("Select a section", ["clients", "Technicians", "Request", "analytics"])


#Clients



# Firebase Initialization
# if 'firebase_initialized' not in st.session_state:
#     cred = credentials.Certificate("/Users/apple/Downloads/hackathonwinnerstelehack-firebase-adminsdk-xxff5-deb1c144f1.json")  # Replace with your Firebase service account key path
#     firebase_admin.initialize_app(cred)
#     st.session_state['firebase_initialized'] = True

# db = firestore.client()

if not firebase_admin._apps:  # Check if Firebase app is already initialized
    cred = credentials.Certificate("/Users/apple/Downloads/hackathonwinnerstelehack-firebase-adminsdk-xxff5-deb1c144f1.json")  # Replace with your Firebase service account key path
    firebase_admin.initialize_app(cred)

db = firestore.client()


# Retrieve users (clients) data from Firestore
def get_users():
    users_ref = db.collection('users').where('role', '==', 'client')  # Filter users by role  
    docs = users_ref.stream()
    users = []
    for doc in docs:
        users.append(doc.to_dict())
    return users

# Add new user to Firestore with role set to 'client'
def add_user(display_name, email, phone_number):
    user_id = str(uuid.uuid4())  # Generate a unique ID using uuid
    db.collection('users').add({
        'displayName': display_name,
        'email': email,
        'phoneNumber': phone_number,
        'role': 'client',  # Set role as 'client'
        'id': user_id  # Use the generated uuid as the ID
    })

# Delete user from Firestore
def delete_user(user_email):
    users_ref = db.collection('users')
    docs = users_ref.where('email', '==', user_email).stream()
    for doc in docs:
        db.collection('users').document(doc.id).delete()

# User (Client) Dashboard Section
if option == "clients":  # Assuming 'clients' is the selected dashboard option
    st.header("Clients Management")


    # "Add User" button that opens the form
    if 'show_form' not in st.session_state:
        st.session_state['show_form'] = False

    if st.button("Add Client"):
        st.session_state['show_form'] = True

    # Conditional form to add user details
    if st.session_state['show_form']:
        st.write("### Add New Client")
        with st.form("add_user_form"):
            display_name = st.text_input("Display Name")
            email = st.text_input("Email")
            phone_number = st.text_input("Phone Number")
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Submit")
            with col2:
                if st.form_submit_button("Close"):
                    st.session_state['show_form'] = False

            # Submit the form to add the user and close the form
            if submitted:
                add_user(display_name, email, phone_number)
                st.session_state['show_form'] = False
                st.success("Client added successfully!")

    # Display the user table
    users = get_users()
    if users:
        st.subheader("Clients List")
        users_df = pd.DataFrame(users)

        # Display users in a table with delete buttons
        st.dataframe(users_df)

        # # Add "Delete" buttons in a separate section
        # for index, user in enumerate(users):
        #     col1, col2 = st.columns([8, 1])
        #     with col2:
        #         if st.button(f"Delete", key=user['email']):
        #             delete_user(user['email'])
        #             # st.experimental_rerun()  # Refresh the page after deletion
    else:
        st.write("No users available.")






#Technicians

# Retrieve users (Technicians) data from Firestore
def get_users():
    users_ref = db.collection('users').where('role', '==', 'technician')  # Filter users by role  
    docs = users_ref.stream()
    users = []
    for doc in docs:
        users.append(doc.to_dict())
    return users


# Add new Technicians to Firestore with role set to 'Technician'
def add_user(display_name, email, phone_number):
    user_id = str(uuid.uuid4())  # Generate a unique ID using uuid
    db.collection('users').add({
        'displayName': display_name,
        'email': email,
        'phoneNumber': phone_number,
        'role': 'technician',  # Set role as 'client'
        'id': user_id  # Use the generated uuid as the ID
    })

# Delete Technicians from Firestore
def delete_user(user_email):
    users_ref = db.collection('users')
    docs = users_ref.where('email', '==', user_email).stream()
    for doc in docs:
        db.collection('users').document(doc.id).delete()

if option == "Technicians":
    st.header("Technicians Management")

    # "Add User" button that opens the form
    if 'show_form' not in st.session_state:
        st.session_state['show_form'] = False

    if st.button("Add Technician"):
        st.session_state['show_form'] = True

    # Conditional form to add user details
    if st.session_state['show_form']:
        st.write("### Add New User")
        with st.form("add_user_form"):
            display_name = st.text_input("Display Name")
            email = st.text_input("Email")
            phone_number = st.text_input("Phone Number")
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Submit")
            with col2:
                if st.form_submit_button("Close"):
                    st.session_state['show_form'] = False

            # Submit the form to add the user and close the form
            if submitted:
                add_user(display_name, email, phone_number)
                st.session_state['show_form'] = False
                st.success("Technician added successfully!")

    # Display  table
    users = get_users()
    if users:
        st.subheader("Technicians List")
        users_df = pd.DataFrame(users)

        # Display users in a table with delete buttons
        st.dataframe(users_df)

        # # Add "Delete" buttons in a separate section
        # for index, user in enumerate(users):
        #     col1, col2 = st.columns([3, 1])
        #     with col2:
        #         if st.button(f"Delete", key=user['email']):
        #             delete_user(user['email'])
        #             # st.experimental_rerun()  # Refresh the page after deletion
    else:
        st.write("No Technicians available.")




if option == "analytics":
    st.header("Sample Charts")
    
    # Line Chart
    st.subheader("Line Chart")
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['A', 'B', 'C']
    )
    st.line_chart(chart_data)
    
    # Bar Chart
    st.subheader("Bar Chart")
    st.bar_chart(chart_data)



# Add new Technicians to Firestore with role set to 'Technician'
def add_request(display_name, email):
    user_id = str(uuid.uuid4())  # Generate a unique ID using uuid
    db.collection('requests').add({
        'attachments': display_name,
        'status': email,
       
    })
def get_r():
    users_ref = db.collection('requests') # Filter users by role  
    docs = users_ref.stream()
    users = []
    for doc in docs:
        users.append(doc.to_dict())
    return users
    
    
if option == "Request":
    st.header("Request")

    

    # "Add User" button that opens the form
    if 'show_form' not in st.session_state:
        st.session_state['show_form'] = False

    # if st.button("Add Request"):
    #     st.session_state['show_form'] = True

    # Conditional form to add user details
    if st.session_state['show_form']:
        st.write("### Add New User")
        with st.form("add_user_form"):
            display_name = st.text_input("URL")
            email = st.text_input("end-point")
           
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Submit")
            with col2:
                if st.form_submit_button("Close"):
                    st.session_state['show_form'] = False

            # Submit the form to add the user and close the form
            if submitted:
                add_user(display_name, email)
                st.session_state['show_form'] = False
                st.success("Request added successfully!")

    # Display  table
    r = get_r()
    if r:
        st.subheader("Requeest List")
        users_df = pd.DataFrame(r)

        # Display users in a table with delete buttons
        st.dataframe(users_df)

        # # Add "Delete" buttons in a separate section
        # for index, user in enumerate(users):
        #     col1, col2 = st.columns([3, 1])
        #     with col2:
        #         if st.button(f"Delete", key=user['email']):
        #             delete_user(user['email'])
        #             # st.experimental_rerun()  # Refresh the page after deletion
    else:
        st.write("No Technicians available.")






