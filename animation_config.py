SHOW_FILM_NAMES = True
# SHOW_FILM_NAMES = False

# UPDATE_TEXT_BOX_LOC = False
UPDATE_TEXT_BOX_LOC = True

SHORTEN_FILM_NAMES = True

# READ_PARTIAL_DB = True
READ_PARTIAL_DB = False

# HIGH_RES = False
HIGH_RES = True

EXPIRE_FILM_NAMES = True
# EXPIRE_FILM_NAMES = False

#SLIDING_WINDOW = False
SLIDING_WINDOW = True
WINDOW_WIDTH = 5  # in years
ADD_ZOOM_OUT = True
ADD_END_DELAY = True

W_HIGH_RES = 1920
H_HIGH_RES = 1080
FONT_SIZE_H_RES = 3

W_LOW_RES = 1080
H_LOW_RES = 720
FONT_SIZE_L_RES = 7

# SHOW_LEADERBOARD = False
SHOW_LEADERBOARD = True

TRACK_FRANCHISES = True
# TRACK_FRANCHISES = False

DISPOSABLE_STRINGS = [
    "Captain America: ",
    "Thor: ",
    "Avengers: ",
    "Spider-Man: ",
    "Harry Potter and the ",
    "Fantastic Beasts: ",
    "Star Wars: ",
    "The IMAX Experience ",
    ": A Star Wars Story",
    "The Lord of the Rings: ",
    "The Hobbit: ",
    "X-Men: ",
    "X-Men Origins: ",
    " (2017)",
    "The Fast and the Furious: ",
    "Pirates of the Caribbean: ",
    ": Dawn of Justice"
]

FRANCHISE_NAME_DICT = {
    'Marvel Cinematic Universe': 'MCU',
    'The Fast and the Furious': 'Fast and Furious',
    'Pirates of the Caribbean': 'Pirates',
    'DC Extended Universe': 'DCEU'
}