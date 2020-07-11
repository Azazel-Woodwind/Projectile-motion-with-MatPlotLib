# Projectile-motion-with-MatPlotLib
Python script that calculates optimal angle and time to hit a target given speed, horizontal and vertical displacement.

The question is as follows:

"That’s all very well, but you can’t just fly towards the goal in Quidditch, you’ll get a bludger in the face!"
"I agree, so you’ll need a backup plan. Imagine that instead of shooting, you need to dodge a bludger and weave around one of the opposing team’s chasers."

You are now only 20m from the goal and have come to a complete stop, exactly level in height with the goal.
At what angle must you throw the ball in order to still hit the target?                                      (Projection speed still = 15ms-1)

“But there isn’t just one goal in Quidditch, there are three, and there’s a keeper in the way trying to stop you scoring.”
“Good point, so we need to think about which shot would be the most effective.”

The chaser now notices there are 3 goals vertically aligned with 5m between them (the original goal is the middle of the 3). 
They can choose to score in any of the 3 goals but wish to do so in the quickest possible time to beat the keeper. 
Which goal should they aim for in order to have the shortest time of flight (and beat the reaction times of the keeper)?
(Range = 20m, Projection speed = 15m/s)

This is a python script that uses matplotlib and basic SUVAT maths to make a brute force algorithm that tests every possible angle between minimum and maximum values 
(step of 0.02 degrees). It then finds the angle with the least distance from the target, given the projections speed of course.

N.B: TO RUN THE PROGRAMME, SIMPLY DOWNLOAD tkinterUI.py AND projmotion.py TO THE SAME FOLDER AND RUN tkinterUI.py
