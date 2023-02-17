import requests

sheety_headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer ai9f034mfpslmf3f09j302"
}

sheety_users_url = "https://api.sheety.co/5081303fda5ac7c15023a7f07cf98314/flightDeals/users"

print("Welcome to Aaron's Flight Club!\nWe will find the best flight deals and email you.")
first_name = input("What is your first name?\n").title()
last_name = input("What is your last name?\n").title()
input_identical = False
while not input_identical:
    email_address = input("What is your email?\n").lower()
    confirm_email = input("Type your email again.\n").lower()
    if email_address == confirm_email:
        new_user = {
            "user": {
                "firstName": first_name,
                "lastName": last_name,
                "email": confirm_email
            }
        }
        requests.post(url=sheety_users_url, json=new_user, headers=sheety_headers)
        print("Success! Your email has been added! Look forward to sending you great flight deals!")
        input_identical = True