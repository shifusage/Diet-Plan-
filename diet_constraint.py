# this code will set limitations for the program, including calorie limit, and food group category, and daily meal count
import json
import random


def load_ingredient_list():
    with open("ingredients_list.json", "r") as file:
        file_contents = file.read()
        return json.loads(file_contents)


def main():
    ingredients = load_ingredient_list()
    meal = generate_meal(ingredients)
    print('your meal is', meal)


def split_ingredients_into_categories(ingredients_list):
    categories = {
        'vegetable': [],
        'protein': [],
        'fruit': []
    }
    for ingredient in ingredients_list:
        food_category = ingredient['food_category'].strip()
        if food_category == 'protein':
            categories['protein'].append(ingredient)
        elif food_category == 'vegetable':
            categories['vegetable'].append(ingredient)
        elif food_category == 'fruit':
            categories['fruit'].append(ingredient)
    return categories


def pick_protein_from_categories(categories,calories):
    return pick_item_from_category(categories, 'protein',calories)


def pick_vegetable_from_categories(categories,calories):
    return pick_item_from_category(categories, 'vegetable',calories)


def pick_fruit_from_categories(categories,calories):
    return pick_item_from_category(categories, 'fruit',calories)


def pick_item_from_category(categories, index_category, current_calorie_sum):
    if not categories[index_category]:
        return None
    items_to_choose_from = list(
        filter(lambda ingredient: ingredient['calorie'] + current_calorie_sum <= 400, categories[index_category]))
    random.shuffle(items_to_choose_from)
    item = items_to_choose_from[0]
    index = categories[index_category].index(item)
    if item['quantity'] == 1:
        categories[index_category].remove(item)
    else:
        categories[index_category][index]['quantity'] = item['quantity'] - 1

    return item


def generate_meal(ingredients_list):
    meal = []
    calories = 0
    # split ingredients list into 3 main food categories vegetable, protein and fruit

    categories = split_ingredients_into_categories(ingredients_list)
    print('old categories', categories)
    protein = pick_protein_from_categories(categories, calories)
    if protein:
        meal.append(protein)
        calories = calories + protein['calorie']
    vegetable = pick_vegetable_from_categories(categories,calories)
    if vegetable:
        meal.append(vegetable)
        calories = calories + vegetable['calorie']
    fruit = pick_fruit_from_categories(categories,calories)
    if fruit:
        meal.append(fruit)
        calories = calories + fruit['calorie']
    # choose from protein category one item of one quantity and add to calorie counter choose one item from vegetable
    # category of one quantity and add to calorie counter limit that cannot exceed 400 or will reshuffle choose one
    # item from fruit category of one quantity and add to calorie counter only if below 400 calorie on calorie
    # counter. if no fruit can fit under 400 cal, omit fruit.
    print('calories',calories)
    print('categories after picking', categories)
    return meal


if __name__ == "__main__":
    main()
