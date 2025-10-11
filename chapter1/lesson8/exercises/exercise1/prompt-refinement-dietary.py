from dotenv import load_dotenv

from app.util import openai_client, get_completion, print_in_box_all_prompts_and_response

load_dotenv()

# Define sample recipes
sample_recipes = [
    {
        "name": "Classic Spaghetti Bolognese",
        "ingredients": [
            "1 lb ground beef",
            "1 onion, finely chopped",
            "2 garlic cloves, minced",
            "1 carrot, finely diced",
            "1 celery stalk, finely diced",
            "1 can (14 oz) crushed tomatoes",
            "2 tbsp tomato paste",
            "1 cup beef broth",
            "1 tsp dried oregano",
            "1 bay leaf",
            "1 lb spaghetti",
            "2 tbsp olive oil",
            "Salt and pepper to taste",
            "Grated Parmesan cheese for serving",
        ],
        "instructions": [
            "Heat olive oil in a large pot over medium heat.",
            "Add onion, garlic, carrot, and celery. Cook until softened, about 5 minutes.",
            "Add ground beef and cook until browned, breaking it up as it cooks.",
            "Stir in tomato paste and cook for 1 minute.",
            "Add crushed tomatoes, beef broth, oregano, bay leaf, salt, and pepper.",
            "Bring to a simmer, then reduce heat to low and cook for 1-2 hours.",
            "Cook spaghetti according to package instructions until al dente.",
            "Drain pasta and serve topped with the Bolognese sauce.",
            "Sprinkle with grated Parmesan cheese.",
        ],
    },
    {
        "name": "Vegetable Stir Fry",
        "ingredients": [
            "2 cups mixed vegetables (bell peppers, broccoli, carrots, snap peas)",
            "1 block firm tofu, cubed",
            "2 tbsp vegetable oil",
            "2 cloves garlic, minced",
            "1 tsp ginger, grated",
            "3 tbsp soy sauce",
            "1 tbsp rice vinegar",
            "1 tsp sesame oil",
            "1 tsp cornstarch",
            "2 green onions, sliced",
            "Sesame seeds for garnish",
            "Cooked rice for serving",
        ],
        "instructions": [
            "Press tofu to remove excess water, then cut into cubes.",
            "Mix soy sauce, rice vinegar, sesame oil, and cornstarch in a small bowl.",
            "Heat vegetable oil in a wok or large skillet over high heat.",
            "Add tofu and cook until golden, about 3-4 minutes. Remove and set aside.",
            "Add garlic and ginger to the wok and stir for 30 seconds.",
            "Add vegetables and stir-fry for 4-5 minutes until crisp-tender.",
            "Return tofu to the wok, add sauce mixture, and cook for 1-2 minutes until sauce thickens.",
            "Garnish with green onions and sesame seeds.",
            "Serve over rice.",
        ],
    },
    {
        "name": "Chocolate Chip Cookies",
        "ingredients": [
            "2 1/4 cups all-purpose flour",
            "1 tsp baking soda",
            "1 tsp salt",
            "1 cup (2 sticks) butter, softened",
            "3/4 cup granulated sugar",
            "3/4 cup packed brown sugar",
            "2 large eggs",
            "2 tsp vanilla extract",
            "2 cups semi-sweet chocolate chips",
            "1 cup chopped nuts (optional)",
        ],
        "instructions": [
            "Preheat oven to 375°F (190°C).",
            "Combine flour, baking soda, and salt in a small bowl.",
            "Beat butter, granulated sugar, and brown sugar in a large mixer bowl.",
            "Add eggs one at a time, beating well after each addition.",
            "Beat in vanilla extract.",
            "Gradually beat in flour mixture.",
            "Stir in chocolate chips and nuts if using.",
            "Drop by rounded tablespoon onto ungreased baking sheets.",
            "Bake for 9 to 11 minutes or until golden brown.",
            "Cool on baking sheets for 2 minutes; remove to wire racks to cool completely.",
        ],
    },
]

# Define common dietary restrictions
dietary_restrictions = [
    "vegetarian",
    "vegan",
    "gluten-free",
    "dairy-free",
    "nut-free",
    "egg-free",
    "low-sodium",
    "keto",
    "paleo",
    "kosher",
]


def format_prompt(recipe, prompt):
    ingredients_str = "\n".join(
        ["- " + ingredient for ingredient in recipe["ingredients"]]
    )
    instructions_str = "\n".join(
        [
            f"{i + 1}. {instruction}"
            for i, instruction in enumerate(recipe["instructions"])
        ]
    )
    restrictions_str = ", ".join(dietary_restrictions)

    return prompt.format(
        recipe_name=recipe["name"],
        recipe_ingredients=ingredients_str,
        recipe_instructions=instructions_str,
        dietary_restrictions=restrictions_str
    )


def main():
    client = openai_client()

    initial_prompt = """
You are a dietary consultant specializing in food allergies and dietary restrictions.

Your task is to analyze the following recipe and determine whether it satisfies each dietary restriction in the list.
For each restriction, classify it as "satisfied," "not satisfied," or "undeterminable" based on the recipe information.

Important context and definitions for dietary restrictions:
- Vegetarian: No meat, poultry, fish, or seafood. May include eggs and dairy.
- Vegan: No animal products or byproducts, including meat, poultry, fish, seafood, eggs, dairy, honey, and gelatin.
- Gluten-free: No ingredients containing wheat, barley, rye, or triticale. Oats must be certified gluten-free.
- Dairy-free: No milk or milk-derived ingredients, including cheese, butter, yogurt, and cream.
- Nut-free: No tree nuts or peanuts, nor ingredients derived from them.
- Egg-free: No eggs or ingredients containing eggs.
- Low-sodium: Contains minimal added salt; typically less than 140mg sodium per serving.
- Keto: Low in carbohydrates (usually under 20-50g net carbs per day), high in fat, moderate in protein.
- Paleo: No grains, legumes, dairy, refined sugar, or processed foods. Focuses on meat, fish, vegetables, fruits, nuts, and seeds.
- Kosher: Meets Jewish dietary laws, including permitted ingredients, preparation, and separation of meat and dairy.


Guidelines for your analysis:
- Mark a restriction as "satisfied" only if you are certain the recipe meets it.
- Mark a restriction as "not satisfied" if any ingredient or instruction clearly violates the restriction based on the provided definitions.
- Mark a restriction as "undeterminable" if the recipe does not provide enough information to confidently assess compliance (e.g., ambiguous ingredients, missing details, or unclear preparation methods).
For each classification, briefly explain the reasoning behind your decision, referencing specific ingredients or instructions that influenced the classification

Handling ambiguities:
- For "vegetable oil" or unspecified oil, consider it plant-based unless otherwise noted.
- For "broth" or "stock," assume it matches the recipe's main protein (e.g., beef broth is not vegetarian or vegan; vegetable broth is plant-based unless specified otherwise.)
- For "flour" assume it is wheat-based unless labeled gluten-free.
- For "cheese" "yogurt," or "cream," assume dairy-based unless specified as plant-based or dairy-free.
- For "sugar" assume standard refined sugar unless specified as unrefined or alternative sweetener.
- For "nuts" if unspecified, assume tree nuts unless clarified.
- For "soy sauce" assume it contains gluten unless labeled gluten-free.
- For "chocolate" assume it contains dairy unless specified as dairy-free or vegan.
- For "mayonnais," assume it contains eggs unless specified as egg-free or vegan.

Example analysis for a simple recipe:

Recipe: Basic Pancakes
Ingredients:
- 1 cup all-purpose flour
- 2 tbsp sugar
- 1 tsp baking powder
- 1/2 tsp salt
- 1 egg
- 1 cup milk
- 2 tbsp butter, melted

Response:
{{
  "vegetarian": {{
    "classification": "satisfied",
    "explanation": "All ingredients are vegetarian; contains no meat, poultry, fish, or seafood.",
    "critical_ingredients": []
  }},
  "vegan": {{
    "classification": "not satisfied",
    "explanation": "Contains animal products.",
    "critical_ingredients": ["1 egg", "1 cup milk", "2 tbsp butter, melted"]
  }},
  "gluten-free": {{
    "classification": "not satisfied",
    "explanation": "Contains all-purpose flour which contains gluten.",
    "critical_ingredients": ["1 cup all-purpose flour"]
  }}
}}


Recipe: {recipe_name}

Ingredients:
{recipe_ingredients}

Instructions:
{recipe_instructions}

Dietary Restrictions to Check:
{dietary_restrictions}

Please format your response as a JSON object where:
- Each key is the name of a dietary restriction
- Each value is an object with properties:
  - "classification": "satisfied", "not satisfied", or "undeterminable"
  - "explanation": brief reasoning for your classification
  - "critical_ingredients": array of ingredients that determined your classification
    """

    test_recipe = sample_recipes[2]
    formatted_prompt = format_prompt(test_recipe, initial_prompt)
    initial_response = get_completion(client, None, formatted_prompt)
    print_in_box_all_prompts_and_response("N/A", formatted_prompt, initial_response)


if __name__ == '__main__':
    main()
