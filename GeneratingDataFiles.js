//Creating data files that will be used to create scatter plots
const fs = require('fs');


var cursor = db.getSiblingDB("test").getCollection("database").find({}, { _id: 0, user_id: 1, user_description: 1, likes: 1, retweet_count: 1 }).limit(50000);


var allLikes = [];
var allRetweets = [];
var allDescriptionLengths = [];


cursor.forEach(function(doc) {
    allLikes = allLikes.concat(doc.likes);
    allRetweets = allRetweets.concat(doc.retweet_count);
    allDescriptionLengths.push(doc.user_description.length); 
});


var likesContent = "likes\n" + allLikes.join("\n");
var retweetsContent = "retweets\n" + allRetweets.join("\n");
var descriptionLengthsContent = "description_length\n" + allDescriptionLengths.join("\n");


try {
    fs.writeFileSync("all_users_likes.csv", likesContent);
    fs.writeFileSync("all_users_retweets.csv", retweetsContent);
    fs.writeFileSync("all_users_description_lengths.csv", descriptionLengthsContent);
    print("Files saved successfully.");
} catch (e) {
    print("Error writing files: " + e);
}
