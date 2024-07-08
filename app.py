from flask import Flask, request, render_template, send_file
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import os
import emailscrape as s  # Assuming emailscrape has the scrape_mail_from_mca function

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Function to scrape data from Falconebiz
def scrape_company_data(company_name, cin):
    company_name_formatted = company_name.replace(" ", "-")
    url = f"https://www.falconebiz.com/company/{company_name_formatted}-{cin}"

    response = requests.get(url)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    script_tag = soup.find("script", type="application/ld+json")
    if not script_tag:
        return None

    json_data = json.loads(script_tag.string)
    org_data = json_data["@graph"][0]

    directors = ", ".join(director["name"] for director in org_data.get("founders", []))
    address = org_data["address"]["streetAddress"]
    activity = org_data["naics"]

    return {
        "Directors": directors,
        "Address": address,
        "Activity": activity,
    }


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename.endswith(".xlsx"):
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            # Load the Excel file, skipping the first row
            sheet_name = "Indian Companies"
            df = pd.read_excel(
                filepath, sheet_name=sheet_name, header=0
            )  # Skip first row

            # Clean the column names
            df.columns = df.columns.str.strip()

            # Debug: Print out the actual column names
            print("Actual columns:", df.columns.tolist())

            # Attempt to dynamically find the CIN column
            cin_column = next((col for col in df.columns if "CIN" in col.upper()), None)
            if not cin_column:
                return "CIN column not found in the uploaded file."

            # Filter rows where CIN has 'TN' at 7th and 8th positions
            df_filtered = df[df[cin_column].str[6:8] == "TN"]

            directors_list = []
            address_list = []
            activity_list = []
            email_list = []  # New list for email addresses

            for _, row in df_filtered.iterrows():
                company_name = row["Company Name"]
                cin = row[cin_column]

                data = scrape_company_data(company_name, cin)
                if data:
                    directors_list.append(data["Directors"])
                    address_list.append(data["Address"])
                    activity_list.append(data["Activity"])
                else:
                    directors_list.append(None)
                    address_list.append(None)
                    activity_list.append(None)

                # Call email scraping function
                result = None
                while not result:
                    result = s.scrape_mail_from_mca(cin)
                    if result:
                        email_list.append(result)
                        break
                else:
                    email_list.append(None)

            df_filtered["Directors"] = directors_list
            df_filtered["Address"] = address_list
            df_filtered["Activity"] = activity_list
            df_filtered["Email"] = email_list  # Add email column

            output_filepath = os.path.join(
                app.config["UPLOAD_FOLDER"], "filtered_companies.xlsx"
            )
            df_filtered.to_excel(output_filepath, index=False)

            return send_file(output_filepath, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
