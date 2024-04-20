import matplotlib.pyplot as plt
from pymongo import MongoClient

client = MongoClient('mongodb+srv://plin11:2968peter@cluster0.jwnt1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['test']
collection = db['database']

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

# Execute
results = list(collection.aggregate(pipeline))

# Check results
if results and results[0]:
    counts = results[0]
    print(f"Number of Republican users: {counts.get('republican_count', 0)}")
    print(f"Number of Democratic users: {counts.get('democrat_count', 0)}")

    # Data
    labels = ['Republican', 'Democratic']
    sizes = [counts.get('republican_count', 0), counts.get('democrat_count', 0)]
    colors = ['#FF9999', '#9999FF']
    explode = (0.1, 0)  

    # Plot
    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    ax.axis('equal')
    plt.title('Political Affiliation of Users')
    plt.show()

else:
    print("No data found.")
