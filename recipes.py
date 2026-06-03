class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name
        self._quantity = None
        self.quantity = quantity
        self.unit = unit
    
    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, value):
        if value <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = float(value)
    
    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"
    
    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"
    
    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            return False
        return self.name == other.name and self.unit == other.unit


class Recipe:
    def __init__(self, title, ingredients=None):
        self.title = title
        self._ingredients = {}
        if ingredients:
            for ing in ingredients:
                self.add_ingredient(ing)
    
    def add_ingredient(self, ingredient):
        key = (ingredient.name, ingredient.unit)
        if key in self._ingredients:
            self._ingredients[key].quantity += ingredient.quantity
        else:
            self._ingredients[key] = ingredient
    
    @staticmethod
    def is_valid_ratio(ratio):
        return isinstance(ratio, (int, float)) and ratio > 0
    
    def scale(self, ratio):
        if not self.is_valid_ratio(ratio):
            raise ValueError("Коэффициент должен быть положительным числом")
        new_ingredients = []
        for ing in self._ingredients.values():
            new_ing = Ingredient(ing.name, ing.quantity * ratio, ing.unit)
            new_ingredients.append(new_ing)
        return Recipe(self.title, new_ingredients)
    
    def __len__(self):
        return len(self._ingredients)
    
    def __str__(self):
        result = f"Рецепт: {self.title}\nИнгредиенты:\n"
        for ing in self._ingredients.values():
            result += f"  - {ing}\n"
        return result


class ShoppingList:
    def __init__(self):
        self._items = []
    
    def add_recipe(self, recipe, portions):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        scaled = recipe.scale(portions)
        for ing in scaled._ingredients.values():
            self._items.append((ing, recipe.title))
    
    def remove_recipe(self, title):
        self._items = [item for item in self._items if item[1] != title]
    
    def get_list(self):
        total = {}
        for ingredient, _ in self._items:
            key = (ingredient.name, ingredient.unit)
            total[key] = total.get(key, 0) + ingredient.quantity
        result = []
        for (name, unit), quantity in total.items():
            result.append(Ingredient(name, quantity, unit))
        result.sort(key=lambda x: x.name)
        return result
    
    def __add__(self, other):
        new_list = ShoppingList()
        new_list._items = self._items + other._items
        return new_list


class DietaryRecipe(Recipe):
    def __init__(self, title, diet_type, ingredients=None):
        self.diet_type = diet_type
        super().__init__(title, ingredients)
    
    def scale(self, ratio):
        scaled = super().scale(ratio)
        return DietaryRecipe(scaled.title, self.diet_type, list(scaled._ingredients.values()))
    
    def __str__(self):
        return f"[{self.diet_type}] {self.title}"
