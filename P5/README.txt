This was created by Alex Perrotti and Rogelio Molina-Marquez.

The search is a relatively basic A* based on the given P1 code from
P2. It prioritized where to search by timecost + heuristic.

The heuristic simply adds inf to any state which produces an
'unnecessary' item. Theoretically, if given a goal to make 100
benches, it would fail for this reason, so in order to make these
decisions reasonably, we disallowed any quantity of a reletively easy to
obtain item higher than the maximum amount that may be needed for any
of the given test cases in the grading criteria section.

The definition of an unnecessary quantity is as follows:
max = (max consumed in a rule - 1) + (min amount produced in a rule)

We also banned axes (i.e. gave +inf heuristic to states with axes),
as they were not included in any optimal solution
to the grading criteria problems. We could've gotten under to 30 second
mark allowing non-iron axes (iron is no better than stone), but because
the heuristic is already tailored to the idea that we're NOT making
100 planks, an amount of wood that would benefit from axes is already
impossible for our heuristic to produce. This conclusion was arrived at
by running our search on the given test cases with no time limit, and
seeing it return the proper cost and len given in the assignment
description, with no axes produced. The time saved from this is actually
extremely significant, as every axe increases the possibility space
being searched over by the number of possible 1-0 combinations of axes.
For example, 3 axes allowed to exist that may or may not mean 8 versions
of every other state can potentially exist for all the axe combinations.
We were able to get 1 cart and 20 rails from 28 seconds, to 11 seconds
by doing this.
