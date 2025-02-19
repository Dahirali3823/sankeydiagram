import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import plotly.graph_objects as go

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def authenticate(account_number=1):
    """Shows basic usage of the Gmail API. Lists the user's Gmail labels."""
    creds = None
    creds_filename = f"google_account{account_number}.json"

    # Load credentials if available
    creds = None

    if os.path.exists(creds_filename):
        creds = Credentials.from_authorized_user_file(creds_filename, SCOPES)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    elif not creds:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)

    # Print the email address for this account
    service = build("gmail", "v1", credentials=creds)
    profile = service.users().getProfile(userId="me").execute()
    email = profile.get("emailAddress", "Unknown")
    print(f"Authenticated account {account_number}: {email}")

    # Save credentials for future use
    with open(creds_filename, "w") as google:
        google.write(creds.to_json())

    return creds


def labels(my_email, account_number=1):
    """Retrieve labels for the specified account."""

    try:
        creds = authenticate(account_number)
        service = build("gmail", "v1", credentials=creds)
        results = service.users().labels().list(userId="me").execute()
        label_list = results.get("labels", [])

        if not label_list:
            print(f"No labels found for account {account_number}.")
            return {}

        label_dict = {}

        for label in label_list:
            label_name = label["name"]

            if label_name.startswith("Applications/") and label_name != "Applications/Received" and label_name != "Applications/test":
                # Get list of messages for this label
                messages = service.users().messages().list(
                    userId="me", labelIds=[label["id"]]
                ).execute().get("messages", [])

                unique_threads = set()  # Track unique threads

                for msg in messages:
                    msg_data = service.users().messages().get(
                        userId="me", id=msg["id"]
                    ).execute()

                    thread_id = msg_data.get("threadId")
                    if thread_id:
                        # Add only unique thread IDs
                        unique_threads.add(thread_id)

                # Store the unique thread count
                label_dict[label_name] = len(unique_threads)

            elif label_name == "Applications/Received":
                # Get total messages normally for Applications/test
                label_details = service.users().labels().get(
                    userId="me", id=label["id"]
                ).execute()
                label_dict[label_name] = label_details.get("messagesTotal", 0)

        if label_dict:
            print(
                f"Labels and Message Count for account {account_number}: {label_dict}")
        else:
            print(f"No matching labels found for account {account_number}.")

        return label_dict  # Ensure return statement is correctly placed

    except HttpError as error:
        print(
            f"An error occurred while processing account {account_number}: {error}")
        return {}  # Return empty dictionary in case of an error


def format():
    sankey = []

    # Fetch labels from both accounts and combine them
    label_account1 = labels("da23ali83@gmail.com", 1)
    label_account2 = labels("ali00378@umn.edu", 2)
   

    # Merge label counts from both accounts
    applications_received = label_account2.get('Applications/Received', 0) + label_account1.get('Applications/Received', 0)
    applications_rejected = label_account2.get('Applications/Rejected', 0) + label_account1.get('Applications/Rejected', 0)
    applications_interview = label_account2.get('Applications/Interview/1st Round', label_account2.get('Applications/Interview', 0)) + label_account1.get('Applications/Interview/1st Round', label_account1.get('Applications/Interview', 0))
    second_round = label_account2.get('Applications/Interview/2nd Round', 0) + label_account1.get('Applications/Interview/2nd Round', 0)
    third_round = label_account2.get('Applications/Interview/3rd Round', 0) + label_account1.get('Applications/Interview/3rd Round', 0)
    offers = label_account2.get('Applications/Offer', 0) + label_account1.get('Applications/Offer', 0)
    accepted_offers = label_account2.get('Applications/Accepted', 0) + label_account1.get('Applications/Offer', 0)

    # Rejections for interview rounds
    firstrejection = max(applications_interview - second_round, 0)
    secondrejection = max(second_round - third_round, 0)
    thirdrejection = max(third_round - offers, 0)

    declined_offers = max(offers - accepted_offers, 0)

    # Ensure non-negative
    no_answer = max(applications_received - applications_rejected - applications_interview, 0)

    # Build the Sankey flow structure
    sankey = [
        f"Applications [{applications_interview}] 1st Interviews",
        f"1st Interviews [{firstrejection}] Rejected",
        f"1st Interviews [{second_round}] 2nd Interviews",
        f"1st Interviews [{offers}] Offers",
        f"Applications [{applications_rejected}] Rejected",
        f"Applications [{no_answer}] No answer",
        f"2nd Interviews [{secondrejection}] Rejected",
        f"2nd Interviews [{third_round}] 3rd Interviews",
        f"3rd Interviews [{thirdrejection}] Rejected",
        f"Offers [{accepted_offers}] Accepted",
        f"Offers [{declined_offers}] Declined"
    ]

    # Return the Sankey flow structure as a single string
   
    return "\n".join(sankey)

if __name__ == "__main__":
    print(format())
