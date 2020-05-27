# Veracode Usage Script

A simple example of usage of the Veracode API signing library provided on the [Veracode Help Center](https://help.veracode.com/reader/LMv_dtSHyb7iIxAQznC~9w/cCoBmgWWxUM4hOY54dTqgA) to return account data related to license use and user roles.

## Setup

Save Veracode API credentials in your home folder `~/.veracode/credentials`
An example of how to create the Credentials file is also provided on the [Veracode Help Center](https://help.veracode.com/reader/LMv_dtSHyb7iIxAQznC~9w/zm4hbaPkrXi02YmacwH3wQ)

Add multiple crednentials, one for each account to be queried.
The bracketed name will become the account name. The credentials must map to either a human user with Admin and Security Lead roles or an API User with AdminAPI and ResultsAPI roles for each Account you wish to check entitlements for. The script will skip the [default] credentials. Example for retieving data for two agencies:

    [default]
    veracode_api_key_id = <YOUR_API_KEY_ID>
    veracode_api_key_secret = <YOUR_API_KEY_SECRET>

    [Account1]
    veracode_api_key_id = <API_KEY_ID_FOR_Account1>
    veracode_api_key_secret = <API_KEY_SECRET_FOR_Account1>

    [Account2]
    veracode_api_key_id = <API_KEY_ID_FOR_Account2>
    veracode_api_key_secret = <API_KEY_SECRET_FOR_Account2>

Install dependencies:

    cd veracode-usage-script
    pip install -r requirements.txt


## Run

Run by calling in a Terminal or cmd window:

    python account-usage.py
    
Results will be printed onscreen and saved to a csv file in the present working directory.

