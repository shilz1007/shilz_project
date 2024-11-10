import re
import json

def parse_car_showroom_data(text):
    showroom_data = {}
    current_showroom = None

    for line in text.splitlines():
        if "Store Name:" in line:
            current_showroom = re.search(r"Store Name: (.*)", line).group(1).strip()
            showroom_data[current_showroom] = {}
        elif "Phone Number:" in line:
            showroom_data[current_showroom]["phone_number"] = re.search(r"Phone Number: (.*)", line).group(1).strip()
        elif "Address:" in line:
            showroom_data[current_showroom]["address"] = re.search(r"Address: (.*)", line).group(1).strip()
        elif "Services available:" in line:
            showroom_data[current_showroom]["services"] = []
        elif "Reviews:" in line:
            showroom_data[current_showroom]["reviews"] = []
        elif "- " in line:
            if not line.startswith("- Review"):
                service_match = re.search(r"- (.*),", line)
            if service_match:
                service = service_match.group(1).strip()
                price_match = re.search(r"(\d+) INR",line) 
            if price_match:
                price = int(price_match.group(1))
                showroom_data[current_showroom]["services"].append({"service": service.strip(), "price": int(price)})
            else:
                review = re.search(r"- Review \d+: \"(.*)\"", line).group(1).strip()
                showroom_data[current_showroom]["reviews"].append(review)   


    return showroom_data

infile = ''#provide input folder path
outfile = ''#provide output folder path
# Example usage:
with open(infile, "r") as f:
    text_data = f.read()

showroom_data = parse_car_showroom_data(text_data)
with open(outfile, "w") as f:
    json.dump(showroom_data, f, indent=4)