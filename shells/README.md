Want to see [inside a nautilus](pics/nautilus_halfshell.jpeg)? This is a tough fold but not impossible. Score the inner lines on [nautilus_halfshell.svg](nautilus_halfshell.svg), cut the outer ones (the black ones). Fold up and down (the first mountain fold on the big end will be the outside of the shell). 

More tips: You'll need to curving the paper so you can create a crease where the score mark is. Because the curving will go one way and then the other, I recommend folding all the mountains (every other line) then all the valleys (remaining lines). Crease fiercely at the ends of the paper. When the creases are in place, start at the small end, folding the septa (the inner parts of the nautilus) along the creases you made. Don't worry about the spiraling of the paper, it probably starts looking like a staircase. At the end, put it all on one plane, and you get a nautilus half shell.

This works with light cardstock (easier) and kami (harder).

This was generated with the python script [lommel_shellgen.py](lommel_shellgen.py) so if you want to play with number of coils (N) or number of whorls per coil (r), have fun. 

There is also another shell generation script [fuse_shellgen](fuse_shellgen.py) that makes slightly easier to fold snail shells.

# Backstory #

[Shell_t.svg](shell_t.svg) creates a generic shell-like object. This was an accidental find when it became clear that [the toroid bowl](../other/toroidbowl.svg) was not foldable. I cut it in half (the actual paper) and the two result made nice, somewhat generic shells.

The [chambered nautilus](curvedChamberedNautilus.svg) was a more directed effort. After trying to fold the Chambered Nautilus in [Origami Sea Life](https://www.amazon.com/dp/B01LXN1AGC/) and getting stuck (again!) on step 21: the unholy crimping, I looked at the pattern and wondered if I could re-create it with curves. I got out some log-log paper and estimated some curves (ok, then I did it a few more times, [this is version 8](LangBasedNautilus.svg)). The outer part of the fold is ok but the paper curls under and the underside is pretty unsightly. These are the nautilus shells in the [paper aquarium image](pics/paperAquarium.jpeg).

Note that usually, I usually see straight lines pairing curved lines for this sort of effect but I did curving lines with curving lines (the flatter curve to get the general shape, the wavy curve to get the raw edges to tuck under). The outside of the shell will be the direction that the double curved lines are mountain. I recommend folding the flatter lines first since they end up curving opposite to the expected.

I modified that [one to have a bit of translation](LangBasedNautilusT.svg) (nautilus are usually planispiral so the spiral is in one plane, curving over itself, snails are not planispiral because the whorls translate to one side or the other... oh, did you know that there are right and left handed snails... wait this is origami not snail facts). It is ok... I suspect it could be better, it is very tough to fold but you can see [the pic](pics/LangBasedNautilusT.jpeg).

I came across "Paper Nautili: A Model for Three Dimensional Planispiral Growth" by Arle Lommel in [Origami4](https://www.amazon.com/Origami-4-AK-Peters-ebook/dp/B00UVB3ROY/) (it is in the kindle preview). The method described there is for finding the ratios of the spiral an growth. I made a [python script](lommel_halfshellgen.py) to recreate the pattern in the paper and be able to modify it. However, the paper creates a disappointingly flat spiral. However, I modified the script to use Bezier curves so I could try out different curve methods. Note that the goal here is to create a half-shell, open so you can see the septa (see above). 

You can use the double parameter and the offset function to create a pair of of shells that fit together (thereby folding them as a single shell). I'm still experimenting with them, the haven't been to my liking.

I received Tomoko Fuse's Spirals as a gift and decided to change it all. Her Navel Shells and Ammonites are very close to what I've been doing (but she works with straight lines which [produce curved outlines but pretty flat shells](pics/NavelShellsFromSpiralsBook.jpeg)). The Ammonite pattern given in the book has parameters (central angle which describes how fast the shell grows and an angle of spirality that describes how fast the whorls happen). While the python script will generate these, since it isn't my pattern, I'm not going to put an svg in the repo. 

I made a new python script using her methodology [fuse_shellgen](fuse_shellgen.py). Then I modified it to use Bezier curves. I'm mostly [happy with the results](pics/curvedCreaseAmonnites.jpeg) though the tiny tips need some work. There are three svgs available for prescoring (necessary with curves, even slight ones) and they make the three in the photo. Which is which? I wish I'd marked them as I intended but all three look pretty good, I just need to find the one easiest to fold (probably not fusesgen_bez195_ca30_sa15_N20.svg).
