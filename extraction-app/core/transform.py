import json
import csv
import os
from datetime import datetime
from core.kafka import create_kafka_producer, send_to_kafka

def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_csv(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def transform_to_csv(json_data):
    users = json_data['users']
    csv_data = []
    
    headers = [
        "id", "firstName", "lastName", "age", "gender", "email", "phone", 
        "username", "birthDate", "height", "weight", "eyeColor", 
        "hairColor", "hairType", "address", "city", "state", "postalCode", "country"
    ]
    csv_data.append(headers)
    
    for user in users:
        row = [
            user.get('id', ''),
            user.get('firstName', ''),
            user.get('lastName', ''),
            user.get('age', ''),
            user.get('gender', ''),
            user.get('email', ''),
            user.get('phone', ''),
            user.get('username', ''),
            user.get('birthDate', ''),
            user.get('height', ''),
            user.get('weight', ''),
            user.get('eyeColor', ''),
            user['hair'].get('color', ''),
            user['hair'].get('type', ''),
            user['address'].get('address', ''),
            user['address'].get('city', ''),
            user['address'].get('state', ''),
            user['address'].get('postalCode', ''),
            user['address'].get('country', '')
        ]
        csv_data.append(row)
    
    return csv_data

def create_summary(json_data):
    users = json_data['users']
    total_users = len(users)
    
    gender_count = {"male": 0, "female": 0, "other": 0}
    age_groups = {
        "00-10": [0, 0, 0], "11-20": [0, 0, 0], "21-30": [0, 0, 0],
        "31-40": [0, 0, 0], "41-50": [0, 0, 0], "51-60": [0, 0, 0],
        "61-70": [0, 0, 0], "71-80": [0, 0, 0], "81-90": [0, 0, 0],
        "91+": [0, 0, 0]
    }
    city_count = {}
    os_count = {"Windows": 0, "Apple": 0, "Linux": 0}
    
    for user in users:
        gender = user.get('gender', 'other')
        gender_count[gender] += 1
        
        age = user.get('age', 0)
        if age <= 10:
            age_groups["00-10"][gender_to_index(gender)] += 1
        elif age <= 20:
            age_groups["11-20"][gender_to_index(gender)] += 1
        elif age <= 30:
            age_groups["21-30"][gender_to_index(gender)] += 1
        elif age <= 40:
            age_groups["31-40"][gender_to_index(gender)] += 1
        elif age <= 50:
            age_groups["41-50"][gender_to_index(gender)] += 1
        elif age <= 60:
            age_groups["51-60"][gender_to_index(gender)] += 1
        elif age <= 70:
            age_groups["61-70"][gender_to_index(gender)] += 1
        elif age <= 80:
            age_groups["71-80"][gender_to_index(gender)] += 1
        elif age <= 90:
            age_groups["81-90"][gender_to_index(gender)] += 1
        else:
            age_groups["91+"][gender_to_index(gender)] += 1
        
        city = user['address'].get('city', 'Unknown')
        if city not in city_count:
            city_count[city] = {"male": 0, "female": 0, "other": 0}
        city_count[city][gender] += 1
        
        os = user.get('userAgent', '')
        if 'Windows' in os:
            os_count["Windows"] += 1
        elif 'Mac' in os or 'Apple' in os:
            os_count["Apple"] += 1
        elif 'Linux' in os:
            os_count["Linux"] += 1
    
    summary_data = [
        ["register", total_users],
        [],
        ["gender", "total"],
        ["male", gender_count["male"]],
        ["female", gender_count["female"]],
        ["other", gender_count["other"]],
        [],
        ["age", "male", "female", "other"],
    ]
    
    for age_group, counts in age_groups.items():
        summary_data.append([age_group, *counts])
    
    summary_data.append([])
    summary_data.append(["City", "male", "female", "other"])
    for city, counts in city_count.items():
        summary_data.append([city, counts["male"], counts["female"], counts["other"]])
    
    summary_data.append([])
    summary_data.append(["OS", "total"])
    summary_data.append(["Windows", os_count["Windows"]])
    summary_data.append(["Apple", os_count["Apple"]])
    summary_data.append(["Linux", os_count["Linux"]])
    
    return summary_data

def gender_to_index(gender):
    if gender == 'male':
        return 0
    elif gender == 'female':
        return 1
    else:
        return 2

def main():
    today = datetime.today().strftime('%Y%m%d')
    
    json_file_path = f'files/data_{today}.json'
    json_data = load_json(json_file_path)
    
    csv_data = transform_to_csv(json_data)
    etl_csv_file_path = f'files/ETL_{today}.csv'
    save_csv(csv_data, etl_csv_file_path)
    
    summary_data = create_summary(json_data)
    summary_csv_file_path = f'files/summary_{today}.csv'
    save_csv(summary_data, summary_csv_file_path)

if __name__ == "__main__":
    main()
