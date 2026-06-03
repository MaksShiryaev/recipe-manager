import pytest
from recipes import Ingredient, Recipe, ShoppingList, DietaryRecipe

def test_ingredient_creation():
    ing = Ingredient("Мука", 500, "г")
    assert ing.name == "Мука"
    assert ing.quantity == 500
    assert ing.unit == "г"

def test_ingredient_positive_quantity():
    with pytest.raises(ValueError, match="Количество должно быть положительным"):
        Ingredient("Соль", -5, "г")
    with pytest.raises(ValueError):
        Ingredient("Сахар", 0, "г")

def test_ingredient_str():
    ing = Ingredient("Мука", 500, "г")
    assert str(ing) == "Мука: 500.0 г"

def test_ingredient_eq():
    ing1 = Ingredient("Мука", 500, "г")
    ing2 = Ingredient("Мука", 1000, "г")
    ing3 = Ingredient("Сахар", 500, "г")
    ing4 = Ingredient("Мука", 500, "кг")
    assert ing1 == ing2
    assert ing1 != ing3
    assert ing1 != ing4

def test_recipe_creation():
    recipe = Recipe("Пицца")
    assert recipe.title == "Пицца"
    assert len(recipe) == 0

def test_add_ingredient_new():
    recipe = Recipe("Пицца")
    recipe.add_ingredient(Ingredient("Мука", 300, "г"))
    assert len(recipe) == 1

def test_add_ingredient_existing():
    recipe = Recipe("Пицца")
    recipe.add_ingredient(Ingredient("Мука", 300, "г"))
    recipe.add_ingredient(Ingredient("Мука", 200, "г"))
    assert len(recipe) == 1
    for ing in recipe._ingredients.values():
        assert ing.quantity == 500

def test_is_valid_ratio():
    assert Recipe.is_valid_ratio(2) == True
    assert Recipe.is_valid_ratio(0.5) == True
    assert Recipe.is_valid_ratio(0) == False
    assert Recipe.is_valid_ratio(-1) == False

def test_scale():
    recipe = Recipe("Пицца", [Ingredient("Мука", 300, "г")])
    scaled = recipe.scale(2)
    assert scaled is not recipe
    for ing in scaled._ingredients.values():
        assert ing.quantity == 600
    with pytest.raises(ValueError):
        recipe.scale(-1)

def test_len():
    recipe = Recipe("Пицца")
    recipe.add_ingredient(Ingredient("Мука", 300, "г"))
    recipe.add_ingredient(Ingredient("Сыр", 200, "г"))
    recipe.add_ingredient(Ingredient("Мука", 100, "г"))
    assert len(recipe) == 2

def test_shoppinglist_add_recipe():
    recipe = Recipe("Пицца", [Ingredient("Мука", 300, "г")])
    shopping = ShoppingList()
    shopping.add_recipe(recipe, 2)
    assert len(shopping._items) == 1
    assert shopping._items[0][1] == "Пицца"

def test_shoppinglist_invalid_portions():
    recipe = Recipe("Пицца")
    shopping = ShoppingList()
    with pytest.raises(ValueError, match="Количество порций должно быть положительным"):
        shopping.add_recipe(recipe, -1)
    with pytest.raises(ValueError):
        shopping.add_recipe(recipe, 0)

def test_shoppinglist_remove_recipe():
    pizza = Recipe("Пицца", [Ingredient("Мука", 300, "г")])
    cake = Recipe("Торт", [Ingredient("Сахар", 200, "г")])
    shopping = ShoppingList()
    shopping.add_recipe(pizza, 1)
    shopping.add_recipe(cake, 1)
    assert len(shopping._items) == 2
    shopping.remove_recipe("Пицца")
    assert len(shopping._items) == 1
    assert shopping._items[0][1] == "Торт"
    shopping.remove_recipe("Несуществующий")
    assert len(shopping._items) == 1

def test_shoppinglist_get_list_aggregation():
    pizza = Recipe("Пицца", [Ingredient("Мука", 300, "г")])
    bread = Recipe("Хлеб", [Ingredient("Мука", 200, "г")])
    shopping = ShoppingList()
    shopping.add_recipe(pizza, 1)
    shopping.add_recipe(bread, 1)
    result = shopping.get_list()
    assert len(result) == 1
    assert result[0].name == "Мука"
    assert result[0].quantity == 500

def test_shoppinglist_get_list_sorted():
    shopping = ShoppingList()
    shopping.add_recipe(Recipe("А", [Ingredient("Сахар", 100, "г")]), 1)
    shopping.add_recipe(Recipe("Б", [Ingredient("Мука", 100, "г")]), 1)
    shopping.add_recipe(Recipe("В", [Ingredient("Яйца", 2, "шт")]), 1)
    result = shopping.get_list()
    names = [ing.name for ing in result]
    assert names == sorted(names)

def test_shoppinglist_add():
    list1 = ShoppingList()
    list1.add_recipe(Recipe("Пицца", [Ingredient("Мука", 300, "г")]), 1)
    list2 = ShoppingList()
    list2.add_recipe(Recipe("Торт", [Ingredient("Сахар", 200, "г")]), 1)
    combined = list1 + list2
    assert len(combined._items) == 2
    assert len(list1._items) == 1
    assert len(list2._items) == 1

def test_dietary_recipe_creation():
    recipe = DietaryRecipe("Салат", "веган")
    assert recipe.title == "Салат"
    assert recipe.diet_type == "веган"

def test_dietary_recipe_scale():
    recipe = DietaryRecipe("Салат", "веган", [Ingredient("Огурец", 100, "г")])
    scaled = recipe.scale(2)
    assert isinstance(scaled, DietaryRecipe)
    assert scaled.diet_type == "веган"

def test_dietary_recipe_str():
    recipe = DietaryRecipe("Салат", "веган")
    assert str(recipe) == "[веган] Салат"
