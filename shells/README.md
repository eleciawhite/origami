Shell_t creates a generric shell-like object. This was an accidental find when it became clear that [the toroid bowl](../other/toroidbowl.svg) was not foldable. I cut it in half (the actual paper) and the two result made nice, somewhat generic shells.

The [chambered nautilus](curvedChamberedNautilus.svg) was a more directed effort. After trying to fold the Chambered Nautilus in [Origami Sea Life](https://www.amazon.com/dp/B01LXN1AGC/) and getting stuck (again!) on step 21: the unholy crimping, I looked at the pattern and wondered if I could re-create it with curves. I got out some log-log paper and estimated some curves (ok, then I did it a few more times, [this is version 8](LangBasedNautilus.svg)). The outer part of the fold is ok but the paper curls under and the underside is pretty unsightly. These are the nautilus shells in the [paper aquarium image](pics/paperAquarium.jpeg).

Note that usually, I usually see straight lines pairing curved lines for this sort of effect but I did curving lines with curving lines (the flatter curve to get the general shape, the wavy curve to get the raw edges to tuck under). The outside of the shell will be the direction that the double curved lines are mountain. I recommend folding the flatter lines first since they end up curving opposite to the expected.

I modified that [one to have a bit of translation](LangBasedNautilusT.svg) (nautilus are usually planispiral so the spiral is in one plane, curving over itself, snails are not planispiral because the whorls translate to one side or the other... oh, did you know that there are right and left handed snails... wait this is origami not snail facts). It is ok... I suspect it could be better, it is very tough to fold but you can see [the pic](pics/LangBasedNautilusT.jpeg).

I came across "Paper Nautili: A Model for Three Dimensional Planispiral Growth" by Arle Lommel in [Origami4](https://www.amazon.com/Origami-4-AK-Peters-ebook/dp/B00UVB3ROY/) (it is in the kindle preview). The method described there is for finding the ratios of the spiral an growth. I made a [python script](lommel_halfshellgen.py) to recreate the pattern in the paper and be able to modify it. However, the paper creates a disappointingly flat spiral. However, I modified the script to use Bezier curves so I could try out different curve methods. Note that the goal here is to create a half-shell, open so you can see the septa. While the script creates several options, only a few are committed as being good:
* [Original Lommel flat shell](shellgen_Lommel_r108_16.svg)
* 

Ideally, once I'm happier with the models, I can connect two half-shells to get a nautilus that is correct inside and out

Finally, you can fold these with prescored kami but something thicker is much, much easier.