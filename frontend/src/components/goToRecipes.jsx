import { useState } from "react";
import { fetchRecipe } from "../services/recipes"; 

const Recipe = () => {
  const [recipe, setRecipe] = useState(null); 
  const [showRecipe, setShowRecipe] = useState(false); 
  const [error, setError] = useState(null); 

  // Function to toggle the recipe display and fetch if necessary
  const toggleRecipe = async () => {
    if (!recipe) {
      try {
        const data = await fetchRecipe(); 
        setRecipe(data);
      } catch (error) {
        setError("Failed to fetch the recipe. Please try again later.");
      }
    }
    setShowRecipe((prevShow) => !prevShow); // Toggle recipe visibility
  };

  return (
    <div>
      <button onClick={toggleRecipe}>goToRecipe</button>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {showRecipe && recipe && (
        <div>
          <h2>{recipe.title}</h2>
          <p>Cooking Time: {recipe.cooking_time} minutes</p>
          <h3>Ingredients:</h3>
          <ul>
            {recipe.ingredients.map((ingredient, index) => (
              <li key={index}>
                {ingredient.ingredient_name}
              </li>
            ))}
          </ul>
          <h3>Steps:</h3>
          <ol>
            {recipe.steps.map((step) => (
              <li key={step.step_order}>
                {step.step_description}
              </li>
            ))}
          </ol>
        </div>
      )}
    </div>
  );
};

export default Recipe;