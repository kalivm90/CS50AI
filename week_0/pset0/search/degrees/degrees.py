import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}
# {'kevin bacon': {'102'}, 'tom cruise': {'129'}, 'cary elwes': {'144'}, 'tom hanks': {'158'}, 
#  'mandy patinkin': {'1597'}, 'dustin hoffman': {'163'}, 'chris sarandon': {'1697'}, 
#  'demi moore': {'193'}, 'jack nicholson': {'197'}, 'bill paxton': {'200'}, 
#  'sally field': {'398'}, 'valeria golino': {'420'}, 'gerald r. molen': {'596520'}, 
#  'gary sinise': {'641'}, 'robin wright': {'705'}, 'emma watson': {'914612'}}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}
# {'102': {'name': 'Kevin Bacon', 'birth': '1958', 'movies': {'104257', '112384'}}, '129': {'name': 'Tom Cruise', 'birth': '1962', 'movies': {'95953', '104257'}}, 
#  '144': {'name': 'Cary Elwes', 'birth': '1962', 'movies': {'93779'}}, '158': {'name': 'Tom Hanks', 'birth': '1956', 'movies': {'112384', '109830'}}, 
#  '1597': {'name': 'Mandy Patinkin', 'birth': '1952', 'movies': {'93779'}}, '163': {'name': 'Dustin Hoffman', 'birth': '1937', 'movies': {'95953'}}, 
#  '1697': {'name': 'Chris Sarandon', 'birth': '1942', 'movies': {'93779'}}, '193': {'name': 'Demi Moore', 'birth': '1962', 'movies': {'104257'}}, 
#  '197': {'name': 'Jack Nicholson', 'birth': '1937', 'movies': {'104257'}}, '200': {'name': 'Bill Paxton', 'birth': '1955', 'movies': {'112384'}}, 
#  '398': {'name': 'Sally Field', 'birth': '1946', 'movies': {'109830'}}, '420': {'name': 'Valeria Golino', 'birth': '1965', 'movies': {'95953'}}, 
#  '596520': {'name': 'Gerald R. Molen', 'birth': '1935', 'movies': {'95953'}}, '641': {'name': 'Gary Sinise', 'birth': '1955', 'movies': {'112384', '109830'}}, 
#  '705': {'name': 'Robin Wright', 'birth': '1966', 'movies': {'93779', '109830'}}, '914612': {'name': 'Emma Watson', 'birth': '1990', 'movies': set()}}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}
# {'112384': {'title': 'Apollo 13', 'year': '1995', 'stars': {'200', '158', '102', '641'}}, 
#  '104257': {'title': 'A Few Good Men', 'year': '1992', 'stars': {'193', '197', '102', '129'}}, 
#  '109830': {'title': 'Forrest Gump', 'year': '1994', 'stars': {'158', '705', '398', '641'}}, 
#  '93779': {'title': 'The Princess Bride', 'year': '1987', 'stars': {'1597', '144', '1697', '705'}}, 
#  '95953': {'title': 'Rain Man', 'year': '1988', 'stars': {'596520', '163', '129', '420'}}}

def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name("tom cruise")
    # source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    # target = person_id_for_name(input("Name: "))
    target = person_id_for_name("tom hanks")
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    root = Node(people[source], None, [])
    q = QueueFrontier()
    q.add(root)
    visited = StackFrontier()

    while not q.empty():
        current = q.remove()
        if not visited.contains_state(current):
            visited.add(root)
            print(current)
            for i in neighbors_for_person(person_id_for_name(current.state["name"])):
                q.add(Node(people[i[1]], current.state, [i] + current.action))
            
            print(q.frontier)

        if current.state == people[target]:
            return current.action



    # TODO
    # raise NotImplementedError


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    # print(movie_ids)
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
