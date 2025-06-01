import click
import os
import webbrowser
import time
import json
from github import Github, BadCredentialsException, UnknownObjectException
import shutil

# --- Constants ---
TOKEN_DIR = "Github_token_cc_SynapseKit"
TOKEN_FILE = os.path.join(TOKEN_DIR, "github_token.json")
COMMIT_MESSAGE = "Committed from SynapseKit, github.com/giuse1106/SynapseKit"
GITHUB_REPO_URL = "https://github.com/giuse1106/SynapseKit" # Your toolbox's GitHub repo

# --- Title Display Function (as defined before, now in English) ---
def display_toolbox_title():
    """
    Prints the ASCII art title for the toolbox, centered and colored.
    """
    title_art = """
.▄▄ ·  ▄· ▄▌ ▐ ▄  ▄▄▄·  ▄▄▄·.▄▄ · ▄▄▄ .▄ •▄ ▪  ▄▄▄▄▄
▐█ ▀. ▐█▪██▌•█▌▐█▐█ ▀█ ▐█ ▄█▐█ ▀. ▀▄.▀·█▌▄▌▪██ •██  
▄▀▀▀█▄▐█▌▐█▪▐█▐▐▌▄█▀▀█  ██▀·▄▀▀▀█▄▐▀▀▪▄▐▀▀▄·▐█· ▐█.▪
▐█▄▪▐█ ▐█▀·.██▐█▌▐█ ▪▐▌▐█▪·•▐█▄▪▐█▐█▄▄▌▐█.█▌▐█▌ ▐█▌·
 ▀▀▀▀   ▀ • ▀▀ █▪ ▀  ▀ .▀    ▀▀▀▀  ▀▀▀ ·▀  ▀▀▀▀ ▀▀▀ 
    """
    
    lines = title_art.strip().split('\n')
    terminal_width = os.get_terminal_size().columns if hasattr(os, 'get_terminal_size') else 80
    max_line_length = max(len(line) for line in lines)
    padding = max(0, (terminal_width - max_line_length) // 2)
    
    for line in lines:
        click.echo(click.style(" " * padding + line, fg='cyan'))
    
    subtitle = "Your Super Python Toolbox! Automation & More"
    subtitle_padding = max(0, (terminal_width - len(subtitle)) // 2)
    click.echo(click.style("\n" + " " * subtitle_padding + subtitle, fg='white', bold=True))
    
    separator = "-" * (terminal_width - 2)
    click.echo(click.style(separator + "\n", fg='white'))

# --- Utility Function: Clear Screen ---
def clear_screen():
    """Clears the console."""
    os.system('cls' if os.name == 'nt' else 'clear')

# --- Token Management Utilities ---
def get_github_token():
    """Retrieves the GitHub token from the stored JSON file."""
    if not os.path.exists(TOKEN_FILE):
        return None
    try:
        with open(TOKEN_FILE, 'r') as f:
            data = json.load(f)
            return data.get('token')
    except (json.JSONDecodeError, KeyError):
        return None

def validate_github_token(token):
    """
    Validates a GitHub token by attempting to get the authenticated user.
    Returns:
        0: Token does not exist.
        1: Token exists and is functional.
        2: Token exists but is not functional (bad credentials or missing scopes).
    """
    if not token:
        return 0 # Token doesn't exist (or couldn't be read)

    try:
        g = Github(token)
        g.get_user().login # Try to access a property to validate token
        return 1 # Token is functional
    except BadCredentialsException:
        return 2 # Token exists but is bad/expired
    except Exception as e:
        # Catch other potential issues like missing scopes (e.g., if it's a fine-grained token)
        click.echo(f"Debug: Token validation error: {e}", err=True)
        return 2 # Token exists but has other issues (e.g., insufficient permissions)

# --- Main Menu Display and Navigation ---
@click.command()
def cli():
    """
    SynapseKit - Your super Python Toolbox!
    """
    while True:
        clear_screen()
        display_toolbox_title() # Show the title at the top

        click.echo(click.style("--- Main Menu ---", fg='yellow', bold=True))
        click.echo(click.style("Select an option:\n", fg='white'))
        
        click.echo(click.style("01. ", fg='cyan', bold=True) + click.style("GitHub Utils", fg='white'))
        click.echo(click.style("02. ", fg='cyan', bold=True) + click.style("Another Module 1 (Placeholder)", fg='white'))
        click.echo(click.style("03. ", fg='cyan', bold=True) + click.style("Another Module 2 (Placeholder)", fg='white'))
        
        click.echo(click.style("98. ", fg='cyan', bold=True) + click.style("Contacts", fg='white'))
        click.echo(click.style("99. ", fg='cyan', bold=True) + click.style("Quit Toolkit", fg='white'))

        choice = click.prompt(click.style("\nEnter option number", fg='green'))

        if choice == '01':
            show_github_utils_page()
        elif choice == '02':
            click.echo("You selected 'Another Module 1'. Implement its logic here!")
            time.sleep(2)
        elif choice == '03':
            click.echo("You selected 'Another Module 2'. Implement its logic here!")
            time.sleep(2)
        elif choice == '98':
            show_contacts_page()
        elif choice == '99':
            click.echo(click.style("\nThanks for using SynapseKit! Goodbye.", fg='yellow'))
            time.sleep(1)
            clear_screen()
            break
        else:
            click.echo(click.style("Invalid option. Please try again.", fg='red'))
            time.sleep(1)

# --- GitHub Utils Menu ---
def show_github_utils_page():
    """
    Displays and manages the GitHub Utilities page.
    """
    while True:
        clear_screen()
        display_toolbox_title()

        current_token = get_github_token()
        token_status = validate_github_token(current_token)

        # Determine token status text and color
        if token_status == 1:
            token_status_text = click.style("(Already Functional)", fg='green')
            show_advanced_github_options = True
        elif token_status == 2:
            token_status_text = click.style("(Exists but not functional)", fg='red')
            show_advanced_github_options = False # Don't show fork/upload if token is bad
        else: # token_status == 0
            token_status_text = click.style("(Not Set Up)", fg='yellow')
            show_advanced_github_options = False # Don't show fork/upload if no token

        click.echo(click.style("--- GitHub Utilities ---", fg='yellow', bold=True))
        click.echo(click.style("Select an option:\n", fg='white'))

        # Add Token option always available
        click.echo(click.style("01. ", fg='cyan', bold=True) + click.style(f"Add GitHub Token {token_status_text}", fg='white'))

        # Other options conditional on token functionality
        if show_advanced_github_options:
            click.echo(click.style("02. ", fg='cyan', bold=True) + click.style("Fork a Repository", fg='white'))
            click.echo(click.style("03. ", fg='cyan', bold=True) + click.style("Upload Files to a Repository", fg='white'))
        else:
            click.echo(click.style("02. ", fg='black', bold=True) + click.style("Fork a Repository (Token Required)", fg='bright_black')) # Grayed out
            click.echo(click.style("03. ", fg='black', bold=True) + click.style("Upload Files to a Repository (Token Required)", fg='bright_black')) # Grayed out

        click.echo(click.style("98. ", fg='cyan', bold=True) + click.style("Close Menu", fg='white'))
        click.echo(click.style("99. ", fg='cyan', bold=True) + click.style("Quit Toolkit", fg='white'))

        choice = click.prompt(click.style("\nEnter option number", fg='green'))

        if choice == '01':
            add_github_token()
        elif choice == '02' and show_advanced_github_options:
            fork_github_repo(current_token)
        elif choice == '03' and show_advanced_github_options:
            upload_files_to_repo(current_token)
        elif choice == '98':
            click.echo("Returning to Main Menu...")
            time.sleep(1)
            clear_screen()
            break
        elif choice == '99':
            click.echo(click.style("\nThanks for using SynapseKit! Goodbye.", fg='yellow'))
            time.sleep(1)
            clear_screen()
            exit() # Exit directly from here if Quit is chosen in sub-menu
        else:
            click.echo(click.style("Invalid option or token not functional. Please try again.", fg='red'))
            time.sleep(1)

# --- GitHub Functionality Implementations ---
def add_github_token():
    """
    Prompts user for a GitHub token and stores it.
    Validates the token immediately after storing.
    """
    clear_screen()
    display_toolbox_title()
    click.echo(click.style("--- Add GitHub Token ---", fg='yellow', bold=True))
    click.echo("Please enter your GitHub Personal Access Token.")
    click.echo("This token will be stored in 'Github_token_cc_SynapseKit/github_token.json'.")
    click.echo("Make sure it has necessary permissions (e.g., 'repo' scope for full access).")
    
    new_token = click.prompt(click.style("Enter your token", fg='green'), hide_input=True)

    try:
        os.makedirs(TOKEN_DIR, exist_ok=True)
        with open(TOKEN_FILE, 'w') as f:
            json.dump({'token': new_token}, f)
        
        status = validate_github_token(new_token)
        if status == 1:
            click.echo(click.style("Token saved and is functional!", fg='green'))
        else:
            click.echo(click.style("Token saved, but it appears to be NOT FUNCTIONAL. Please check permissions or validity.", fg='red'))
        
    except Exception as e:
        click.echo(click.style(f"Error saving token: {e}", fg='red'))
    
    time.sleep(2)

def fork_github_repo(token):
    """
    Forks a specified GitHub repository using the provided token.
    """
    clear_screen()
    display_toolbox_title()
    click.echo(click.style("--- Fork a Repository ---", fg='yellow', bold=True))
    
    repo_input = click.prompt(click.style("Enter repository URL or 'user/repo' (e.g., 'github.com/octocat/Spoon-Knife')", fg='green'))
    
    # Normalize input: remove http(s)://github.com/ if present
    if repo_input.startswith("https://github.com/"):
        repo_input = repo_input[len("https://github.com/"):]
    elif repo_input.startswith("http://github.com/"):
        repo_input = repo_input[len("http://github.com/"):]
    elif repo_input.startswith("github.com/"):
        repo_input = repo_input[len("github.com/"):]
    
    if '/' not in repo_input:
        click.echo(click.style("Invalid repository format. Please use 'user/repo'.", fg='red'))
        time.sleep(2)
        return

    try:
        g = Github(token)
        target_repo = g.get_repo(repo_input)
        
        click.echo(f"Attempting to fork '{target_repo.full_name}'...")
        forked_repo = target_repo.create_fork()
        
        click.echo(click.style(f"Successfully forked '{target_repo.full_name}' to '{forked_repo.full_name}'!", fg='green'))
        click.echo(f"You can view it at: {forked_repo.html_url}")

    except UnknownObjectException:
        click.echo(click.style(f"Error: Repository '{repo_input}' not found. Check the spelling.", fg='red'))
    except BadCredentialsException:
        click.echo(click.style("Error: Bad credentials. Your token might be invalid or expired.", fg='red'))
    except Exception as e:
        click.echo(click.style(f"An unexpected error occurred: {e}", fg='red'))
    
    time.sleep(3)


def upload_files_to_repo(token):
    """
    Uploads specified files from a local folder to a user's GitHub repository.
    """
    clear_screen()
    display_toolbox_title()
    click.echo(click.style("--- Upload Files to Repository ---", fg='yellow', bold=True))
    
    local_folder = click.prompt(click.style("Enter the path to the local folder with files to upload", fg='green'))
    if not os.path.isdir(local_folder):
        click.echo(click.style(f"Error: Local folder '{local_folder}' not found.", fg='red'))
        time.sleep(2)
        return

    target_repo_name = click.prompt(click.style("Enter the name of YOUR target GitHub repository (e.g., 'my-awesome-repo')", fg='green'))

    # Confirm before proceeding
    confirm = click.confirm(click.style(f"Confirm uploading files from '{local_folder}' to your repo '{target_repo_name}'?", fg='yellow'), default=True)
    if not confirm:
        click.echo("Upload cancelled.")
        time.sleep(1)
        return

    try:
        g = Github(token)
        user = g.get_user()
        target_repo = user.get_repo(target_repo_name)

        click.echo(f"Uploading files to '{target_repo.full_name}'...")
        
        # Iterate over files in the local folder
        for root, _, files in os.walk(local_folder):
            for file_name in files:
                local_path = os.path.join(root, file_name)
                # Determine the path within the GitHub repo (relative to local_folder)
                repo_path = os.path.relpath(local_path, local_folder).replace(os.sep, '/') # Use forward slashes for GitHub paths

                try:
                    with open(local_path, 'rb') as f:
                        content = f.read()

                    # Check if file exists to update or create
                    try:
                        # Get SHA of existing file if it exists
                        file_in_repo = target_repo.get_contents(repo_path, ref=target_repo.default_branch)
                        target_repo.update_file(file_in_repo.path, COMMIT_MESSAGE, content, file_in_repo.sha, branch=target_repo.default_branch)
                        click.echo(f"Updated: {repo_path}")
                    except UnknownObjectException:
                        # File does not exist, create it
                        target_repo.create_file(repo_path, COMMIT_MESSAGE, content, branch=target_repo.default_branch)
                        click.echo(f"Created: {repo_path}")
                except Exception as file_error:
                    click.echo(click.style(f"Failed to upload '{file_name}': {file_error}", fg='red'))

        click.echo(click.style("File upload process completed!", fg='green'))

    except UnknownObjectException:
        click.echo(click.style(f"Error: Your repository '{target_repo_name}' not found. Please ensure it exists and you own it.", fg='red'))
    except BadCredentialsException:
        click.echo(click.style("Error: Bad credentials. Your token might be invalid or expired, or lacks 'repo' scope.", fg='red'))
    except Exception as e:
        click.echo(click.style(f"An unexpected error occurred during upload: {e}", fg='red'))
    
    time.sleep(3)


# --- Contacts Menu ---
def show_contacts_page():
    """
    Displays the contacts information page.
    """
    while True:
        clear_screen()
        display_toolbox_title()

        click.echo(click.style("--- Contacts ---", fg='yellow', bold=True))
        click.echo(click.style("Select an option:\n", fg='white'))

        click.echo(click.style("01. ", fg='cyan', bold=True) + click.style("Contact on Whatsapp", fg='white'))
        click.echo(click.style("02. ", fg='cyan', bold=True) + click.style("Contact on TikTok", fg='white'))
        click.echo(click.style("03. ", fg='cyan', bold=True) + click.style("Contact on Instagram", fg='white'))
        click.echo(click.style("04. ", fg='cyan', bold=True) + click.style(f"SynapseKit GitHub Repository", fg='white'))

        click.echo(click.style("98. ", fg='cyan', bold=True) + click.style("Close Menu", fg='white'))
        click.echo(click.style("99. ", fg='cyan', bold=True) + click.style("Quit Toolkit", fg='white'))

        choice = click.prompt(click.style("\nEnter option number", fg='green'))

        if choice == '01':
            click.echo("Opening Whatsapp...")
            webbrowser.open("https://wa.me/393445461546")
            time.sleep(2)
        elif choice == '02':
            click.echo("Opening TikTok...")
            webbrowser.open("https://tiktok.com/@giu.rochevivo")
            time.sleep(2)
        elif choice == '03':
            click.echo("Opening Instagram...")
            webbrowser.open("https://instagram.com/giu.rochevivo")
            time.sleep(2)
        elif choice == '04':
            click.echo("Opening SynapseKit GitHub Repository...")
            webbrowser.open(GITHUB_REPO_URL)
            time.sleep(2)
        elif choice == '98':
            click.echo("Returning to Main Menu...")
            time.sleep(1)
            clear_screen()
            break
        elif choice == '99':
            click.echo(click.style("\nThanks for using SynapseKit! Goodbye.", fg='yellow'))
            time.sleep(1)
            clear_screen()
            exit() # Exit directly from here if Quit is chosen in sub-menu
        else:
            click.echo(click.style("Invalid option. Please try again.", fg='red'))
            time.sleep(1)

# --- Entry Point ---
if __name__ == '__main__':
    cli() # Executes the 'cli' command which is our main menu