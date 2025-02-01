import shiny
from shiny import ui, render_ui, Inputs, session

# Simulating a simple user database (you can use a real DB or dictionary)
users_db = {'user1': 'password1', 'user2': 'password2'}

# User interface
app_ui = ui.page_fluid(
    ui.input_text("username", "Username:"),
    ui.input_password("password", "Password:"),
    ui.input_action_button("login_btn", "Login"),
    ui.output_ui("login_message"),
    ui.output_ui("logout_btn")
)

# Server logic
def server(input, output, session):
    
    # To store login status
    logged_in = shiny.reactive.Value(False)
    
    # Rendering login message based on login status
    @render_ui
    def login_message():
        if logged_in():
            return ui.h3(f"Welcome {input.username()}")
        return ui.h3("Please enter your credentials")
    
    # Rendering logout button if logged in
    @render_ui
    def logout_btn():
        if logged_in():
            return ui.input_action_button("logout_btn", "Logout")
        return None
    
    # Handle login button click event
    @shiny.observe_event(input.login_btn, "click")
    def handle_login():
        # Check if the username and password match
        if users_db.get(input.username(), None) == input.password():
            logged_in(True)
        else:
            logged_in(False)
    
    # Handle logout button click event
    @shiny.observe_event(input.logout_btn, "click")
    def handle_logout():
        logged_in(False)

# Run the app
app = shiny.App(app_ui, server)
app.run()
