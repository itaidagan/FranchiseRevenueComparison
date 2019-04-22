# Franchise Comparison

Franchise Comparison looks at the daily gross from ticket sales of film franchises and charts them in an animated plot based on matplotlib. It also takes into account inflation data taken from the United States Department of Labor.


## Installation

Install matplotlib using pip:

```
pip install matplotlib
```

In order to save the animation to an mp4 file install [FFmpeg](https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg), make sure it's added to path.


## Usage
Simply run FranchiseAnimation.py.
You can change how things are shown in the animation by changing the animation_config.py file.
* SHOW_FILM_NAMES - Choose if film names are on the graph or not.
* UPDATE_TEXT_BOX_LOC - Choose whether film names appear for the premiere date and remain stationary or float continiously with the graph as it updates.
* SHORTEN_FILM_NAMES - The graph can get quite crowded if film names are long and many films are shown, check this option and add strings to DISPOSABLE_STRINGS to shorten film names.
* READ_PARTIAL_DB - Mostly for debugging and when you wish to check the rendering and design.
* HIGH_RES - Choose whether to generate the graph in high or low resolution.
* EXPIRE_FILM_NAMES - Causes film to fade gradually once enough time has elapsed since their last location update.
* SLIDING_WINDOW - Choose whether to limit x limits of the graph to a fixed with, slowly moving ahead during the animantion. Choose window width in years using WINDOW_WIDTH.
* ADD_ZOOM_OUT - Add the zooming out animation at the end of the animation.
* ADD_END_DELAY - Add several seconds of static image at the end of the animation.
* SHOW_LEADERBOARD - A misnomer, just shows the date counter.
* TRACK_FRANCHISES - Track the accumulated revenue for each franchise on the right side of the graph.
* FRANCHISE_NAME_DICT - Shortens the names of franchises



## Sources

  - [The Numbers](https://www.the-numbers.com/)
  - [CPI Inflation Calculator](https://data.bls.gov/cgi-bin/cpicalc.pl)


License
----

MIT