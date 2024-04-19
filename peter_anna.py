import matplotlib.pyplot as plt
from pymongo import MongoClient

# Connect to the MongoDB server (assuming localhost and default MongoDB port 27017)
client = MongoClient('mongodb+srv://plin11:2968peter@cluster0.jwnt1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['test']  # Access the 'test' database
collection = db['database']  # Access the 'database' collection

# Define the MongoDB aggregation pipeline
pipeline = [
    {
        "$match": {
            "$or": [
                {"user_description": {"$regex": "democrat|liberal", "$options": "i"}},
                {"user_location": {"$in": ["WA", "OR", "NV", "CA", "AZ", "NM", "CO", "MN", "WI", "IL", "MI", "GA", "PA", "VA", "DC", "MD", "DE", "NJ", "CT", "NY", "RI", "MA", "NH", "ME", "VT"]}},
                {"user_description": {"$regex": "republican|conservative", "$options": "i"}},
                {"user_location": {"$in": ["ID", "MT", "WY", "ND", "SD", "UT", "NE", "KS", "OK", "TX", "IA", "MO", "AR", "LA", "IN", "OH", "KY", "WV", "TN", "MS", "AL", "FL", "SC", "NC"]}}
            ]
        }
    },
    {
        "$project": {
            "_id": 0,
            "user_id": 1,
            "description": "$user_description",
            "location": "$user_location",
            "is_democrat": {
                "$cond": {
                    "if": {
                        "$or": [
                            {"$regexMatch": {"input": {"$toString": "$user_description"}, "regex": "democrat|liberal", "options": "i"}},
                            {"$in": ["$user_location", ["WA", "OR", "NV", "CA", "AZ", "NM", "CO", "MN", "WI", "IL", "MI", "GA", "PA", "VA", "DC", "MD", "DE", "NJ", "CT", "NY", "RI", "MA", "NH", "ME", "VT"]]}
                        ]
                    },
                    "then": 1,
                    "else": 0
                }
            },
            "is_republican": {
                "$cond": {
                    "if": {
                        "$or": [
                            {"$regexMatch": {"input": {"$toString": "$user_description"}, "regex": "republican|conservative", "options": "i"}},
                            {"$in": ["$user_location", ["ID", "MT", "WY", "ND", "SD", "UT", "NE", "KS", "OK", "TX", "IA", "MO", "AR", "LA", "IN", "OH", "KY", "WV", "TN", "MS", "AL", "FL", "SC", "NC"]]}
                        ]
                    },
                    "then": 1,
                    "else": 0
                }
            }
        }
    },
    {
        "$group": {
            "_id": None,
            "democrat_count": {"$sum": "$is_democrat"},
            "republican_count": {"$sum": "$is_republican"}
        }
    }
]

# Execute the aggregation pipeline
results = list(collection.aggregate(pipeline))

# Check results and print to console
if results and results[0]:
    counts = results[0]
    print(f"Number of Republican users: {counts.get('republican_count', 0)}")
    print(f"Number of Democratic users: {counts.get('democrat_count', 0)}")

    # Data for plotting
    labels = ['Republican', 'Democratic']
    sizes = [counts.get('republican_count', 0), counts.get('democrat_count', 0)]
    colors = ['#FF9999', '#9999FF']  # Colors for the pie chart
    explode = (0.1, 0)  # "explode" the 1st slice (Republican)

    # Plotting the pie chart
    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Political Affiliation of Users')
    plt.show()

else:
    print("No data found.")
