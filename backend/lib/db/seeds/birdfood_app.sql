-- For testing database:
DROP TABLE IF EXISTS ingredients CASCADE;
DROP SEQUENCE IF EXISTS ingredients_id_seq CASCADE;
DROP TABLE IF EXISTS steps CASCADE;
DROP SEQUENCE IF EXISTS steps_id_seq CASCADE;
DROP TABLE IF EXISTS bird_recipes CASCADE;
DROP SEQUENCE IF EXISTS bird_recipes_id_seq CASCADE;
DROP TABLE IF EXISTS bird_sightings CASCADE;
DROP SEQUENCE IF EXISTS bird_sightings_id_seq CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP SEQUENCE IF EXISTS users_id_seq CASCADE;
DROP TABLE IF EXISTS ratings CASCADE;
DROP SEQUENCE IF EXISTS ratings_id_seq CASCADE;

-- users table
CREATE SEQUENCE IF NOT EXISTS users_id_seq;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    profile_picture VARCHAR(255) DEFAULT 'uploads/default_bird_image.png'
);

-- bird_sightings table
CREATE SEQUENCE IF NOT EXISTS bird_sightings_id_seq;
    CREATE TABLE bird_sightings (
    id SERIAL PRIMARY KEY,
    bird_name VARCHAR(255) NOT NULL,
    -- image VARCHAR(255) DEFAULT '>INSERT PATH HERE<',
    image VARCHAR(255),
    date_spotted VARCHAR(10),
    location VARCHAR(255) DEFAULT 'Unknown',
    user_id int,
    constraint fk_user foreign key(user_id) references users(id) on delete cascade
);

-- bird_recipes table
CREATE SEQUENCE IF NOT EXISTS bird_recipes_id_seq;
CREATE TABLE bird_recipes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    date_created VARCHAR(10),
    cooking_time INT NOT NULL,
    bird_sighting_id int, 
    CONSTRAINT fk_bird_sighting FOREIGN KEY(bird_sighting_id) REFERENCES bird_sightings(id) ON DELETE CASCADE
);

-- ingredients table
CREATE SEQUENCE IF NOT EXISTS ingredients_id_seq;
CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    recipe_id int NOT NULL,
    ingredient_name TEXT NOT NULL,
    constraint fk_recipe foreign key(recipe_id) references bird_recipes(id) on delete cascade
);

-- steps table
CREATE SEQUENCE IF NOT EXISTS steps_id_seq;
CREATE TABLE steps (
    id SERIAL PRIMARY KEY,
    recipe_id int NOT NULL,
    step_order INT NOT NULL,
    step_description TEXT NOT NULL,
    constraint fk_recipe foreign key(recipe_id) references bird_recipes(id) on delete cascade
);

-- ratings table
CREATE SEQUENCE IF NOT EXISTS ratings_id_seq;
CREATE TABLE ratings (
    id SERIAL PRIMARY KEY,
    rating_score INT NOT NULL CHECK (rating_score >= 1 AND rating_score <= 5),
    recipe_id int NOT NULL,
    constraint fk_recipe foreign key(recipe_id) references bird_recipes(id) on delete cascade
);

DROP FUNCTION IF EXISTS get_avg_recipe_rating(integer);
CREATE OR REPLACE FUNCTION get_avg_recipe_rating(bird_recipe_id INT)
RETURNS NUMERIC AS $$
BEGIN
    RETURN (
        SELECT ROUND(AVG(rating_score), 1)  -- Rounds to 1 decimal place
        FROM ratings
        WHERE recipe_id = bird_recipe_id
    );
END;
$$ LANGUAGE plpgsql;


-- Seed data for users:
INSERT INTO users (username, email, password) VALUES 
('bird_lover', 'birdlover@example.com', 'password123'),
('avian_fanatic', 'avianfanatic@example.com', 'password123'),
('nature_watch', 'naturewatch@example.com', 'password123');

-- Seed data for bird_sightings
INSERT INTO bird_sightings (bird_name, date_spotted, location, user_id) VALUES 
('Flamingo', '2024-12-01', 'Shoreditch', 1),
('Woodpecker', '2024-12-01', 'Peckham', 2),
('Peregrine Falcon', '2024-12-01', 'Wimbledon', 3),
('Resplendent Quetzal', '2024-12-01', 'Greenwich', 3);

-- Seed data for bird_recipes:
INSERT INTO bird_recipes (title, date_created, cooking_time, bird_sighting_id) VALUES 
('Herb-Glazed Flamingo', '2024-12-01', 25, 1), 
('Hearty Winter Woodpecker Pie', '2024-12-01', 40, 2),
('Jamaican Jerk Peregrine Falcon', '2024-12-01', 40, 3),
('Twice-Fried Resplendent Quetzal Wings', '2024-12-01', 20, 4);

-- Seed data for ingredients:
INSERT INTO ingredients (recipe_id, ingredient_name) VALUES
    -- ingredients list 1
(1, '4 boneless, skinless flamingo breasts'),
(1, '2 tbsp olive oil'),
(1, '3 tbsp honey'),
(1, '2 tbsp Dijon mustard'),
(1, '1 tbsp balsamic vinegar'),
(1, '3 cloves garlic, minced'),
(1, '1 tbsp fresh thyme leaves (or 1 tsp dried thyme)'),
(1, '1 tbsp fresh rosemary, chopped (or 1 tsp dried rosemary)'),
(1, '1 tsp paprika'),
(1, 'Salt and black pepper to taste'),
(1, 'Optional: Lemon wedges for garnish'),
    -- ingredients list 2
(2, '2 tablespoons unsalted butter'),
(2, '1 medium onion, finely chopped'),
(2, '2 medium carrots, sliced'),
(2, '2 celery stalks, sliced'),
(2, '500g (about 1 lb) boneless, skinless woodpecker thighs, cut into bite-sized pieces'),
(2, '2 tablespoons plain flour'),
(2, '150ml (about 2/3 cup) dry white wine (optional)'),
(2, '300ml (about 1¼ cups) woodpecker stock'),
(2, '1 teaspoon fresh thyme leaves (or ½ teaspoon dried)'),
(2, '100ml (about ½ cup) double cream (heavy cream)'),
(2, '1 sheet ready-rolled puff pastry'),
(2, 'Salt and pepper, to taste'),
(2, '1 egg, beaten (for glazing)'),
    -- ingredients list 3
(3, '1.5 kg (about 3 lbs) peregrine falcon pieces (legs, thighs, or a whole peregrine falcon cut into parts)'),
(3, '2-3 Scotch bonnet peppers (adjust to taste), seeded and roughly chopped'),
(3, '4 spring onions (scallions), roughly chopped'),
(3, '4 garlic cloves, peeled'),
(3, '2 tablespoons fresh thyme leaves'),
(3, '1 tablespoon ground allspice'),
(3, '1 tablespoon dark brown sugar'),
(3, '2 tablespoons soy sauce'),
(3, 'Juice of 1 lime'),
(3, '1 tablespoon vegetable oil'),
(3, 'Salt and freshly ground black pepper, to taste'),
    -- ingredients list 4
(4, '1 kg (about 2 lbs) resplendent quetzal wings, tips removed and wings separated into drumettes and flats'),
(4, '1 cup plain flour'),
(4, '1 cup cornstarch (cornflour)'),
(4, '1 teaspoon salt'),
(4, '1 teaspoon ground black pepper'),
(4, 'Vegetable oil, for deep-frying'),
(4, '3 tablespoons gochujang (Korean chili paste)'),
(4, '2 tablespoons soy sauce'),
(4, '2 tablespoons rice vinegar'),
(4, '2 tablespoons brown sugar or honey'),
(4, '1 tablespoon toasted sesame oil'),
(4, '2 garlic cloves, minced'),
(4, '1 teaspoon minced fresh ginger');

-- Seed data for steps:
INSERT INTO steps (recipe_id, step_order, step_description) VALUES
    -- method 1
(1, 1, 'Prepare the chicken: Pat chicken breasts dry with a paper towel. Season with salt, pepper, and paprika on both sides.'),
(1, 2, 'Make the glaze: In a small bowl, whisk together honey, Dijon mustard, balsamic vinegar, garlic, thyme, and rosemary.'),
(1, 3, 'Cook the chicken: Heat olive oil in a large skillet over medium heat. Add chicken breasts and cook for about 5-6 minutes per side until golden brown and cooked through (internal temperature should reach 165°F/74°C).'),
(1, 4, 'Glaze the chicken: Reduce heat to low and pour the herb glaze over the chicken. Spoon the glaze over the chicken to coat evenly. Let it simmer for 3-4 minutes until the glaze thickens slightly.'),
(1, 5, 'Serve: Transfer chicken to a serving plate and drizzle with remaining glaze from the pan. Garnish with optional lemon wedges for a fresh citrus touch.'),
    -- method 2
(2, 1, 'Preheat the oven to 200°C (400°F).'),
(2, 2, 'Melt the butter in a large saucepan over medium heat. Add the onion, carrots, and celery; cook until softened, about 5 minutes.'),
(2, 3, 'Stir in the woodpecker pieces and cook until lightly browned. Sprinkle over the flour and stir well.'),
(2, 4, 'Pour in the wine (if using) and simmer until mostly reduced. Add the woodpecker stock and thyme, then simmer gently until the mixture thickens and the woodpecker is cooked through, about 10 minutes.'),
(2, 5, 'Stir in the cream and season with salt and pepper. Transfer the filling to a pie dish.'),
(2, 6, 'Drape the puff pastry over the dish, pressing the edges to seal. Cut a small steam vent on top. Brush with the beaten egg.'),
(2, 7, 'Bake until the pastry is golden and crisp, about 35-40 minutes.'),
    -- method 3
(3, 1, 'In a blender or food processor, combine the Scotch bonnets, spring onions, garlic, thyme, allspice, brown sugar, soy sauce, lime juice, and oil. Blend until a thick, smooth paste forms. Season with salt and pepper.'),
(3, 2, 'Place the peregrine falcon pieces in a large bowl or zip-top bag. Pour over the jerk marinade, ensuring all pieces are well coated. Marinate for at least 4 hours, ideally overnight.'),
(3, 3, 'Preheat a grill (or oven to 200°C/400°F).'),
(3, 4, 'Grill the marinated peregrine falcon over medium heat until well-browned, slightly charred, and cooked through (juices run clear, internal temperature of 75°C/165°F), about 40-45 minutes. If using the oven, place the peregrine falcon on a baking tray and roast until fully cooked, turning occasionally for even browning.'),
(3, 5, 'Let the peregrine falcon rest for a few minutes before serving with rice and peas, plantains, or a fresh salad.'),
    -- method 4
(4, 1, 'In a large bowl, whisk together the flour, cornstarch, salt, and pepper. Toss the resplendent quetzal wings in this mixture, shaking off any excess.'),
(4, 2, 'Heat vegetable oil in a deep fryer or large pot to about 175°C (350°F). Fry the wings in batches until lightly golden and just cooked through, about 8-10 minutes. Remove and drain on paper towels.'),
(4, 3, 'Increase the oil temperature to about 190°C (375°F). Fry the wings again in batches until crisp and deeply golden, about 3-4 minutes more per batch. Drain on paper towels.'),
(4, 4, 'Meanwhile, whisk together all sauce ingredients in a small saucepan over medium heat. Simmer gently until slightly thickened, about 2-3 minutes.'),
(4, 5, 'Toss the double-fried resplendent quetzal wings in the warm sauce until well coated. Serve immediately, garnished with toasted sesame seeds and spring onions if desired.');

-- seed data for ratings

INSERT INTO ratings (rating_score, recipe_id) VALUES
(5, 1),
(4, 2),
(2, 4),
(5, 4),
(3, 2),
(2, 3),
(5, 3),
(5, 3);
