// Step 1: Calculate average description length, likes, and retweets per user
var result = db.getSiblingDB("test").getCollection("database").aggregate([
  {
      $group: {
          _id: "$user_id",
          avg_description_length: { $avg: { $strLenCP: { $toString: "$user_description" } } },
          avg_likes: { $avg: "$likes" },
          avg_retweets: { $avg: "$retweet_count" }
      }
  },
  {
      $sort: { avg_description_length: -1 } // Sort by average description length in descending order
  }
]).toArray();

// Step 2: Calculate correlation coefficient for likes
var sumProductLikes = 0;
var sumProductRetweets = 0;
var sumDescriptionLengths = 0; // Define sumDescriptionLengths
var sumLikes = 0;
var sumRetweets = 0;
var sumSqrDescriptionLengths = 0; // Define sumSqrDescriptionLengths
var sumSqrLikes = 0;
var sumSqrRetweets = 0;
var n = result.length;

result.forEach(function(doc) {
  sumDescriptionLengths += doc.avg_description_length;
  sumLikes += doc.avg_likes;
  sumRetweets += doc.avg_retweets;
  sumSqrDescriptionLengths += Math.pow(doc.avg_description_length, 2); // Update sumSqrDescriptionLengths
  sumSqrLikes += Math.pow(doc.avg_likes, 2);
  sumSqrRetweets += Math.pow(doc.avg_retweets, 2);
  sumProductLikes += doc.avg_description_length * doc.avg_likes;
  sumProductRetweets += doc.avg_description_length * doc.avg_retweets;
});

var correlationLikes = (n * sumProductLikes - sumDescriptionLengths * sumLikes) /
                (Math.sqrt(n * sumSqrDescriptionLengths - Math.pow(sumDescriptionLengths, 2)) *
                 Math.sqrt(n * sumSqrLikes - Math.pow(sumLikes, 2)));

var correlationRetweets = (n * sumProductRetweets - sumDescriptionLengths * sumRetweets) /
                (Math.sqrt(n * sumSqrDescriptionLengths - Math.pow(sumDescriptionLengths, 2)) *
                 Math.sqrt(n * sumSqrRetweets - Math.pow(sumRetweets, 2)));

// Output the correlation coefficients
print("Correlation coefficient for likes:", correlationLikes);
print("Correlation coefficient for retweets:", correlationRetweets);
