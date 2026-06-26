import random

RIDDLES = [

{
"question":"I have keys but no locks. I have space but no room. What am I?",
"answer":"keyboard",
"hint":"Computer"
},

{
"question":"What has hands but cannot clap?",
"answer":"clock",
"hint":"Shows time"
},

{
"question":"What has one eye but cannot see?",
"answer":"needle",
"hint":"Used in stitching"
},

{
"question":"What comes down but never goes up?",
"answer":"rain",
"hint":"Weather"
},

{
"question":"Which animal is known as the King of the Jungle?",
"answer":"lion",
"hint":"Big cat"
},

{
"question":"What has legs but cannot walk?",
"answer":"table",
"hint":"Furniture"
},

{
"question":"What gets wetter as it dries?",
"answer":"towel",
"hint":"Bathroom"
},

{
"question":"Which planet is called the Red Planet?",
"answer":"mars",
"hint":"Fourth planet"
},

{
"question":"How many days are there in one week?",
"answer":"7",
"hint":"Count Monday to Sunday"
}

]

def get_riddle():
    return random.choice(RIDDLES)
