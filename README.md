This program is designed to create and update contacts in a Freshdesk account using data from a GitHub account. The program works by first prompting the user to 
input their GitHub username and their Freshdesk subdomain. It then uses the GitHub API to retrieve information about the user, including their name, bio and email address.
This information is then used to create a new contact in Freshdesk or update an existing one, if the email address already exists.

To create or update a contact in Freshdesk, the program sends a POST or PUT request to the Freshdesk API with the appropriate data in the request body. 
The program also includes authentication credentials in the headers of the request to verify that the request is coming from a valid source.
It uses environment variables (FRESHDESK_TOKEN and GITHUB_TOKEN) from the local device to accessthe apis of freshdesk and github respectively.

To run the program, you'll need to follow these steps:

Make sure you have Python 3.x installed on your computer.
Clone the repository containing the program to your local machine.
Open a terminal or command prompt and navigate to the directory where the program is located.
Install the necessary packages by running the command: pip install -r requirements.txt
Run the program by executing the command: python main.py
Follow the prompts to enter your GitHub username and Freshdesk subdomain.
The program will then retrieve your GitHub data and attempt to create or update a contact in Freshdesk based on your email address.
The program will output the status code and response message from the API request, indicating whether the operation was successful or not.
That's it! If you encounter any errors while running the program, make sure to double-check that you've entered the correct GitHub username and Freshdesk subdomain,
and that your API credentials are valid.
