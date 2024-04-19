/* global use, db */
// MongoDB Playground
// To disable this template go to Settings | MongoDB | Use Default Template For Playground.
// Make sure you are connected to enable completions and to be able to run a playground.
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.
// The result of the last command run in a playground is shown on the results panel.
// By default the first 20 documents will be returned with a cursor.
// Use 'console.log()' to print to the debug output.
// For more documentation on playgrounds please refer to
// https://www.mongodb.com/docs/mongodb-vscode/playgrounds/

// drop existing tables before a live demo

// Select the database to use and get collections
use('test');
db.getCollection('database');

// const candidates = ['Trump', 'Biden']
// policyWords = ['covid', 'mask', 'vaccine', 'climate', 'tax', 'Obamacare', 'China', 'tariff', 'racism']

// Example of sample SQL to create collections for each policy and each candidate respectively
/* 
WITH covid AS (
  SELECT tweet_id, "covid" AS policy
  FROM (
      SELECT tweet_id, SPLIT_STRING(tweet, ' ') AS policyWord
      FROM database
      WHERE  policyWord LIKE '%covid%'
          OR policyWord LIKE '%corona%'
          OR policyWord LIKE '%virus%'
  )
)
*/

db.database.aggregate([
  {
    $project: {
      tweet_id: 1,
      policyWords: {
        $split: ["$tweet", " "]
      }
    }
  },
  { $unwind: "$policyWords" },
  {
    $match: {
      $or: [
        { policyWords: /covid/i },
        { policyWords: /corona/i },
        { policyWords: /virus/i }
      ]
    }
  },
  {
    $group: {
      _id: "$tweet_id",
      policy: { $first: "covid" }
    }
  },
  {
    $project: {
      _id: 0,
      tweet_id: "$_id",
      policy: 1
    }
  },
    {$sort: { tweet_id: 1 } },
    { $out: "covid" }
]);

db.database.aggregate([
  {
    $project: {
      tweet_id: 1,
      policyWords: {
        $split: ["$tweet", " "]
      }
    }
  },
  { $unwind: "$policyWords" },
  {
      $match: {
        policyWords: /mask/i
      }
  },
  {
    $group: {
      _id: "$tweet_id",
      policy: { $first: "mask" }
    }
  },
  {
    $project: {
      _id: 0,
      tweet_id: "$_id",
      policy: 1
    }
  },
    {$sort: { tweet_id: 1 } },
    { $out: "mask" }
]);

db.database.aggregate([
  {
    $project: {
      tweet_id: 1,
      policyWords: {
        $split: ["$tweet", " "]
      }
    }
  },
  { $unwind: "$policyWords" },
  {
      $match: {
        policyWords: /vaccine/i
      }
  },
  {
    $group: {
      _id: "$tweet_id",
      policy: { $first: "vaccine" }
    }
  },
  {
    $project: {
      _id: 0,
      tweet_id: "$_id",
      policy: 1
    }
  },
    {$sort: { tweet_id: 1 } },
    { $out: "vaccine" }
]);

db.database.aggregate([
  {
    $project: {
      tweet_id: 1,
      policyWords: {
        $split: ["$tweet", " "]
      }
    }
  },
  { $unwind: "$policyWords" },
  {
      $match: {
        policyWords: /climate/i
      }
  },
  {
    $group: {
      _id: "$tweet_id",
      policy: { $first: "climate" }
    }
  },
  {
    $project: {
      _id: 0,
      tweet_id: "$_id",
      policy: 1
    }
  },
    {$sort: { tweet_id: 1 } },
    { $out: "climate" }
]);

db.database.aggregate([
  {
    $project: {
      tweet_id: 1,
      policyWords: {
        $split: ["$tweet", " "]
      }
    }
  },
  { $unwind: "$policyWords" },
  {
      $match: {
        policyWords: /tax/i
      }
  },
  {
    $group: {
      _id: "$tweet_id",
      policy: { $first: "tax" }
    }
  },
  {
    $project: {
      _id: 0,
      tweet_id: "$_id",
      policy: 1
    }
  },
    {$sort: { tweet_id: 1 } },
    { $out: "tax" }
]);

db.database.aggregate([
  {
    $project: {
      tweet_id: 1,
      policyWords: {
        $split: ["$tweet", " "]
      }
    }
  },
  { $unwind: "$policyWords" },
  {
      $match: {
        policyWords: /Obamacare/i
      }
  },
  {
    $group: {
      _id: "$tweet_id",
      policy: { $first: "Obamacare" }
    }
  },
  {
    $project: {
      _id: 0,
      tweet_id: "$_id",
      policy: 1
    }
  },
    {$sort: { tweet_id: 1 } },
    { $out: "Obamacare" }
]);

db.database.aggregate([
  {
    $project: {
      tweet_id: 1,
      policyWords: {
        $split: ["$tweet", " "]
      }
    }
  },
  { $unwind: "$policyWords" },
  {
      $match: {
        policyWords: /China/i
      }
  },
  {
    $group: {
      _id: "$tweet_id",
      policy: { $first: "China" }
    }
  },
  {
    $project: {
      _id: 0,
      tweet_id: "$_id",
      policy: 1
    }
  },
    {$sort: { tweet_id: 1 } },
    { $out: "China" }
]);

db.database.aggregate([
  {
    $project: {
      tweet_id: 1,
      policyWords: {
        $split: ["$tweet", " "]
      }
    }
  },
  { $unwind: "$policyWords" },
  {
      $match: {
        policyWords: /tariff/i
      }
  },
  {
    $group: {
      _id: "$tweet_id",
      policy: { $first: "tariff" }
    }
  },
  {
    $project: {
      _id: 0,
      tweet_id: "$_id",
      policy: 1
    }
  },
    {$sort: { tweet_id: 1 } },
    { $out: "tariff" }
]);

db.database.aggregate([
  {
    $project: {
      tweet_id: 1,
      policyWords: {
        $split: ["$tweet", " "]
      }
    }
  },
  { $unwind: "$policyWords" },
  {
      $match: {
        policyWords: /racism/i
      }
  },
  {
    $group: {
      _id: "$tweet_id",
      policy: { $first: "racism" }
    }
  },
  {
    $project: {
      _id: 0,
      tweet_id: "$_id",
      policy: 1
    }
  },
    {$sort: { tweet_id: 1 } },
    { $out: "racism" }
]);

db.database.aggregate([
  {
    $project: {
      tweet_id: 1,
      policyWords: {
        $split: ["$tweet", " "]
      }
    }
  },
  { $unwind: "$policyWords" },
  {
      $match: {
        policyWords: /Trump/i
      }
  },
  {
    $group: {
      _id: "$tweet_id",
      policy: { $first: "Trump" }
    }
  },
  {
    $project: {
      _id: 0,
      tweet_id: "$_id",
      policy: 1
    }
  },
    {$sort: { tweet_id: 1 } },
    { $out: "Trump" }
]);

db.database.aggregate([
  {
    $project: {
      tweet_id: 1,
      policyWords: {
        $split: ["$tweet", " "]
      }
    }
  },
  { $unwind: "$policyWords" },
  {
      $match: {
        policyWords: /Biden/i
      }
  },
  {
    $group: {
      _id: "$tweet_id",
      policy: { $first: "Biden" }
    }
  },
  {
    $project: {
      _id: 0,
      tweet_id: "$_id",
      policy: 1
    }
  },
    {$sort: { tweet_id: 1 } },
    {$out: "Biden" }
]);

// Computed the number of tweets mentioning the policy keywords
var num_covid = db.covid.countDocuments();
print("Number of tweets mentioning covid policy: " + num_covid);
var num_mask = db.mask.countDocuments();
print("Number of tweets mentioning mask policy: " + num_mask);
var num_vaccine = db.vaccine.countDocuments();
print("Number of tweets mentioning vaccine policy: " + num_vaccine);
var num_climate = db.climate.countDocuments();
print("Number of tweets mentioning climate policy: " + num_climate);
var num_tax = db.tax.countDocuments();
print("Number of tweets mentioning tax policy: " + num_tax);
var num_Obamacare = db.Obamacare.countDocuments();
print("Number of tweets mentioning Obamacare policy: " + num_Obamacare);
var num_China = db.China.countDocuments();
print("Number of tweets mentioning China policy: " + num_China);
var num_tariff = db.tariff.countDocuments();
print("Number of tweets mentioning tariff policy: " + num_tariff);
var num_racism = db.racism.countDocuments();
print("Number of tweets mentioning racism policy: " + num_racism);

// Manually implemented Chi-Square test to find the correlation between a candidate and a policy

const total_num_tweet = db.database.countDocuments();

// Compute number of tweets mentioning/not mentioning Trump
var num_tweet_Trump = db.Trump.countDocuments();
print("Number of tweets mentioning Trump: " + num_tweet_Trump);
var num_tweet_not_Trump = total_num_tweet - num_tweet_Trump; 
print("Number of tweets not mentioning Trump: " + num_tweet_not_Trump);

// Compute number of tweets mentioning/not mentioning Biden
const num_tweet_Biden = db.Biden.countDocuments();
print("Number of tweets mentioning Biden: " + num_tweet_Biden);
var num_tweet_not_Biden = total_num_tweet - num_tweet_Biden; 
print("Number of tweets not mentioning Biden: " + num_tweet_not_Biden);

// Compute number of tweets mentioning both Trump and covid policy
db.database.aggregate([
  {
      $match: {
          tweet: {
              $regex: 'TRUMP',
              $options: 'i' 
          }
      }
  },
  {
      $match: {
          tweet: {
              $regex: 'covid',
              $options: 'i'
          }
      }
  },
  {
      $project: {
          tweet_id: 1,
          policyWord: { $split: ["$tweet", " "] }
      }
  },
  {$sort: { tweet_id: 1 } },
  {$out: "Trump_and_covid" }
]);
var num_tweet_Trump_AND_covid = db.Trump_and_covid.countDocuments();
print("Number of tweets mentioning Trump and covid policy: " + num_tweet_Trump_AND_covid);

// Compute number of tweets mentioning both Biden and covid policy
db.database.aggregate([
  {
      $match: {
          tweet: {
              $regex: 'Biden',
              $options: 'i' 
          }
      }
  },
  {
      $match: {
          tweet: {
              $regex: 'covid',
              $options: 'i'
          }
      }
  },
  {
      $project: {
          tweet_id: 1,
          policyWord: { $split: ["$tweet", " "] }
      }
  },
  {$sort: { tweet_id: 1 } },
  {$out: "Biden_and_covid" }
]);
const num_tweet_Biden_AND_covid = db.Biden_and_covid.countDocuments();
print("Number of tweets mentioning Biden and covid policy: " + num_tweet_Biden_AND_covid);