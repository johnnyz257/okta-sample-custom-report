# Okta Partner Registraion Workflow Example

This project was built using Python 2.7

This is a demo where partners can register, and go through an approval workflow using Okta as the Identity Provider.  Partners will have access to different Okta apps based on their partner portal selection.

## Requirements
* Python 3.4 or higher
* Okta domain
* Okta API Token

## Dependencies
You can run all the dependencies via the requirements.txt
`pip3 install -r requirements.txt`

## How to Run

NOTE: You may need to configure ports to listen to for serviing up the site
Besure to set these environment variables first

`OKTA_ORG_URL` Your Okta Org URL formatted like this "https://<my okta org>.okta.com"

`OKTA_API_TOKEN` The APi Token you created in your Okta org

Run the app

`python3 app.py`

## Okta Org Requirements
In order to see results, please create two or more unique groups in Okta with a naming convention that starts with "Office 365" like
"Office 365 - E1 Users"
"Office 365 - E5 Users"
etc...
and please besure to have tst users in each group

to test the application simply navigate to your base pp host i.e. "https://okta-sample-custom-report-recinto.c9users.io/"
and you will be prompted to download a CSV file with the resulting report