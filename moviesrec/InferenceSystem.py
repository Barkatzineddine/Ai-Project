from .facts import *
from aima3.logic import *


def generateLogicConcept(data):
    expression_parts = []
    for key, value in data.items():
        if key in mapper:
            expression_parts.append(str(mapper[key](value)))
    expression = " & ".join(expression_parts) + " ==> Concept(x)"
    print(expression)
    return expression


def generateLogicMovie(data):
    expression_parts = []
    for key, value in data.items():
        if key in mapper:
            expression_parts.append(str(mapper[key](value)))
    expression = " & ".join(expression_parts) + " ==> Movie(y)"
    print(expression)
    return expression


mapper = {
    'language': lambda val: expr(f'Language({val})'),
    'type': lambda val: expr(f'Type({val})'),
    'time': lambda val: expr(f'Time({val})'),
    'genre': lambda val: expr(f'Genre({val})'),
    'principalactor': lambda val: expr(f'Principalactor({val})'),
    'concept': lambda val: expr(f'Concept({val})'),
}


def final_Movie(input_data, list_data):
    agenda = []
    allMovies = []
    for key, value in input_data.items():
        if key in mapper:
            agenda.append(expr(str(mapper[key](value))))
    seen = set()
    memory = {}
    while agenda:
        p = agenda.pop(0)
        if p in seen:
            print(f'{p}')
            continue
        seen.add(p)
        if fol_fc_ask(movie_kb, p):
            memory[p] = True
        else:
            memory[p] = False
        data_one = {
            'language': list_data[1],
            'type': list_data[2],
            'time': list_data[4],
            'genre': list_data[3],

        }
        print("data_one", data_one)
        if memory.get(expr(f'Language({list_data[1]})'), False) and memory.get(expr(f'Type({list_data[2]})'),
                                                                               False) and memory.get(
                expr(f'Time({list_data[4]})'), False) and memory.get(expr(f'Genre({list_data[3]})'), False):
            concept = list(fol_fc_ask(movie_kb, expr(generateLogicConcept(data_one))))
            print("concept", concept)
            if concept:
                for elem in concept:
                    for value in elem.values():
                        value_concept = value
                        expr_concept = str(expr(f'Concept({value})'))
                        agenda.append(expr(expr_concept))
                        data_two = {
                            'principalactor': list_data[0],
                            'concept': value_concept,
                        }
                        print("data_two", data_two)
                        if memory.get(expr(f'Concept({value_concept})'), False) and memory.get(
                                expr(f'Principalactor({list_data[0]})'), False):
                            movie_exp = generateLogicMovie(data_two)
                            movies = list(fol_fc_ask(movie_kb, expr(movie_exp)))
                            print("movies", movies)
                            if movies:
                                for elem in movies:
                                    print("elem", type(elem))

                                    if (type(elem) == dict):
                                        for values in elem.values():
                                            allMovies.append(str(values))
                                            agenda.append(str('movie: ' + values))
                                    else:
                                        continue

    print(type(list(set(allMovies))[0]))
    return list(set(allMovies))
