import { useState } from "react";
import { submitRating } from "../services/recipes";

export function SubmitRating({ recipeId, onRatingSubmit }) {
    const [rating, setRating] = useState("");
    const [error, setError] = useState(null);
    const [successMessage, setSuccessMessage] = useState("");

    const handleRatingSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setSuccessMessage("");

        // Validate input
        const parsedRating = parseInt(rating, 10);
        if (isNaN(parsedRating) || parsedRating < 1 || parsedRating > 5) {
            setError("Please enter a rating between 1 and 5.");
            return;
        }

        try {
            const token = localStorage.getItem("token");
            await submitRating({ recipeId, rating: parsedRating, token });
            setSuccessMessage("Rating submitted successfully!");
            setRating(""); // Reset the input field
            onRatingSubmit(); // Update the parent component with the new rating
        } catch (err) {
            console.error("Error submitting rating:", err);
            setError("Failed to submit rating. Please try again.");
        }
    };

    return (
        <div>
            <form onSubmit={handleRatingSubmit}>
                <label htmlFor="rating">Submit a Rating (1-5):</label>
                <input
                    type="number"
                    id="rating"
                    value={rating}
                    onChange={(e) => setRating(e.target.value)}
                    min="1"
                    max="5"
                />
                <button type="submit">Submit</button>
            </form>
            {error && <p style={{ color: "red" }}>{error}</p>}
            {successMessage && <p style={{ color: "green" }}>{successMessage}</p>}
        </div>
    );
}
