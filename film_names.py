class Franchise:
    def __init__(self, franchise_name, film_array):
        self.franchise_name = franchise_name
        self.film_array = film_array


MCU_films = [
    "Iron Man",
    "The Incredible Hulk",
    "Iron Man 2",
    "Thor",
    "Captain America: The First Avenger",
    "Marvel's The Avengers",
    "Iron Man 3",
    "Thor: The Dark World",
    "Captain America: The Winter Soldier",
    "Guardians of the Galaxy",
    "Avengers: Age of Ultron",
    "Ant-Man",
    "Captain America: Civil War",
    "Doctor Strange",
    "Guardians of the Galaxy Vol. 2",
    "Spider-Man: Homecoming",
    "Thor: Ragnarok",
    "Black Panther",
    "Avengers: Infinity War",
    "Ant-Man and the Wasp",
    "Captain Marvel"]

HP_films = [
    "Harry Potter and the Sorcerer's Stone",
    "Harry Potter and the Chamber of Secrets",
    "Harry Potter and the Prisoner of Azkaban",
    "Harry Potter and the Goblet of Fire",
    "Harry Potter and the Order of the Phoenix",
    "Harry Potter and the Half-Blood Prince",
    "Harry Potter and the Deathly Hallows Part 1",
    "Harry Potter and the Deathly Hallows Part 2",
    "Fantastic Beasts and Where To Find Them",
    "Fantastic Beasts: The Crimes of Grindelwald"
]

LOTR_films = [
    "The Lord of the Rings: The Fellowship of the Ring",
    "The Lord of the Rings: The Two Towers",
    "The Lord of the Rings: The Return of the King",
    "The Hobbit: An Unexpected Journey",
    "The Hobbit: The Desolation of Smaug",
    "The Hobbit: The Battle of the Five Armies"
]

X_Men_films = [
    "X-Men",
    "X2: X-Men United",
    "X-Men: The Last Stand",
    "X-Men Origins: Wolverine",
    "X-Men: First Class",
    "The Wolverine",
    "X-Men: Days of Future Past",
    "Deadpool",
    "X-Men: Apocalypse",
    "Logan (2017)",
    "Deadpool 2"
]

Star_Wars_films = [
    "Star Wars: Episode I - The Phantom Menace",
    "Star Wars: Episode II - Attack of the Clones",
    "Attack of the Clones: The IMAX Experience (IMAX)",
    "Star Wars: Episode III - Revenge of the Sith",
    "Star Wars: The Clone Wars",
    "Star Wars: The Force Awakens",
    "Rogue One: A Star Wars Story",
    "Star Wars: The Last Jedi",
    "Solo: A Star Wars Story"
]

DCEU_films = [
    "Man of Steel",
    "Batman v Superman: Dawn of Justice",
    "Suicide Squad",
    "Wonder Woman",
    "Justice League",
    "Aquaman"
]

FF_films = [
    "The Fast and the Furious",
    "2 Fast 2 Furious",
    "The Fast and the Furious: Tokyo Drift",
    "Fast and Furious",
    "Fast Five",
    "Fast & Furious 6",
    "Furious 7",
    "The Fate of the Furious"
]

Pirates_films = [
    "Pirates of the Caribbean: The Curse of the Black Pearl",
    "Pirates of the Caribbean: Dead Man's Chest",
    "Pirates of the Caribbean: At World's End",
    "Pirates of the Caribbean: On Stranger Tides",
    "Pirates of the Caribbean: Dead Men Tell No Tales"
]

MCU_franchise           = Franchise("Marvel Cinematic Universe", MCU_films)
HP_franchise            = Franchise("Wizarding World", HP_films)
LOTR_franchise          = Franchise("Middle Earth", LOTR_films)
X_Men_franchise         = Franchise("X-Men", X_Men_films)
Star_Wars_franchise     = Franchise("Star Wars", Star_Wars_films)
DCEU_franchise          = Franchise("DC Extended Universe", DCEU_films)
FF_franchise            = Franchise("The Fast and the Furious", FF_films)
Pirates_franchise       = Franchise("Pirates of the Caribbean", Pirates_films)

franchise_array = [MCU_franchise,
                   HP_franchise,
                   LOTR_franchise,
                   X_Men_franchise,
                   Star_Wars_franchise,
                   DCEU_franchise,
                   FF_franchise,
                   Pirates_franchise]
