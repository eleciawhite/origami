I sort of made a seashell by accident and then I wanted a intentional seashell. After a mistake or hundred, I finally got some shells I'm pleased with. I also made a Python script to generate different shells with different coiling and whorl rates.

Let's start with easiest one to fold.

# Nautilus halfshell #

[<img src="pics/nautilus_halfshell.jpeg" alt="inside a nautilus origami" width="200"/>](pics/nautilus_halfshell.jpeg)

Want to see [inside a nautilus](pics/nautilus_halfshell.jpeg)? This is a tough fold but not impossible, see [nautilus_halfshell.svg](nautilus_halfshell.svg).

The SVG was generated with the python script [lommel_shellgen.py](lommel_shellgen.py) so if you want to play with number of coils (N) or number of whorls per coil (r), have fun. 


# Folding Method #
Score the inner lines on , cut the outer ones (the black ones). Fold up and down (the first mountain fold on the big end will be the outside of the shell). 

More tips: You'll need to curving the paper so you can create a crease where the score mark is. Because the curving will go one way and then the other, I recommend folding all the mountains (every other line) then all the valleys (remaining lines). Crease fiercely at the ends of the paper. When the creases are in place, start at the small end, folding the septa (the inner parts of the nautilus) along the creases you made. Don't worry about the spiraling of the paper, it probably starts looking like a staircase. At the end, put it all on one plane, and you get a nautilus half shell.

This works with light cardstock (easier) and kami (harder).

# Snail Shell #

I received Tomoko Fuse's Spirals as a gift and decided to change it all. Her Navel Shells and Ammonites are very close to what I've been doing (but she works with straight lines which [produce curved outlines but pretty flat shells](../spirals/pics/NavelShellsFromSpiralsBook.jpeg)). The Ammonite pattern given in the book has parameters (central angle which describes how fast the shell grows and an angle of spirality that describes how fast the whorls happen). 

In Fuse’s Spirals book but she has a central angle (~growth) and angle of spirality (~whorls). She gives these as numbers for master pattern and leaves the pattern generation to the user, suggesting protractors and templates. I made a new Python script using her methodology [spirals/ammonite.py](../spirals/ammonite.py). While the Python script will generate these flat-fold versions, since it isn't my pattern, I'm not going to put an svg in the repo. 

However, I modified it to use Bezier curves. I'm mostly [happy with the results](pics/curvedCreaseAmonnites.jpeg). If you want a pattern to try, look at [snailShell.svg](snailShell.svg) is available for your pre-scoring, cutting and folding pleasure. The outside is defined by the first mountain fold at the big end.

But there are a lot of parameters that cause different characteristics in the result (both for real shells and for origami shells). The two important ones are the rate the shell expands and the number of whorls per rotation. These can be made intentially off balance to give a turbinate or conispiral shell (like a snail) or a planispiral shell (like a nautilus). See the [snail trio picture](pics/snail_trio.jpeg). These are represented in the snails_*.svg files.

# Backstory #

Note, [Shell_t.svg](shell_t.svg) creates a generic shell-like object. This was an accidental find when it became clear that [the toroid bowl](../other/toroidbowl.svg) was not foldable. I cut it in half (the actual paper) and the two result made nice, somewhat generic shells.

The nautilus was a more directed effort. After trying to fold the Chambered Nautilus in [Origami Sea Life](https://www.amazon.com/dp/B01LXN1AGC/) and getting stuck (again!) on step 21: the unholy crimping, I looked at the pattern and wondered if I could re-create it with curves. I got out some log-log paper and estimated some curves (ok, then I did it a few more times). I used to have the pattern here but the Fuse-based version is much better, this was difficult to fold and while the outer part of the fold looked ok but the paper curls under and the underside is pretty unsightly. These are the nautilus shells in the [paper aquarium image](pics/paperAquarium.jpeg).

[<img src="pics/paperAquarium.jpeg" alt="paper aquarium" width="200"/>](pics/paperAquarium.jpeg)


I came across "Paper Nautili: A Model for Three Dimensional Planispiral Growth" by Arle Lommel in [Origami4](https://www.amazon.com/Origami-4-AK-Peters-ebook/dp/B00UVB3ROY/) (it is in the kindle preview). The method described there is for finding the ratios of the spiral an growth. I made a [python script](lommel_halfshellgen.py) to recreate the pattern in the paper and be able to modify it. However, the paper creates a disappointingly flat spiral. However, I modified the script to use Bezier curves so I could try out different curve methods. Note that the goal here is to create a half-shell, open so you can see the septa (see above). 

You can use the double parameter and the offset function to create a pair of of shells that fit together (thereby folding them as a single shell). I'm still experimenting with them, the haven't been to my liking.

Then I received Tomoko Fuse's Spirals and decided to change it all, including creating new python script using her methodology for [ammonites](../spirals/ammonite.py). 

As for real shells, they also obey parameters in a very interesting way, search for *Raup shell morphospace* or [read this overview](https://www.deepseanews.com/2015/07/digital-seashells-and-david-raup/).