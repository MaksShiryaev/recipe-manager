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
