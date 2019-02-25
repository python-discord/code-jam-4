# Annoying Weather

## What we want to achieve

A really bad user experience

## User stories

User opens GUI \[ ,needs to press `I` or `i` to enter `INSERT MODE` \] and enters a location.

The following stuff can happen then (multiple of them can happen too):

   1. User gets to see the weather in a nice gui
   
   2. User gets so see the weather but with randomly selected units (mixed up imperial, SI and metric units)
  
   3. If multiple of these locations exists request show the weather for the least relevant one.
      (E.g if the user searches for Berlin and does not get the result for the capital of germany but another place on the
      world. See [here](https://www.openstreetmap.org/search?query=Berlin#map=14/49.8650/22.1921))
      
      Instead of showing the results in the order
      
      1. today
      2. tomorrow
      3. bla bla bla
      
      The order is shuffled randomly
   
   4. User opens GUI and needs to press I to enter `INSERT MODE` and enters a location
   
