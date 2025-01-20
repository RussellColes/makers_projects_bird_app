import { useState, useEffect } from "react";
import BirdSighting from "./BirdSighting"
import { getMyBirdSightings } from "../services/sightings"
import './DisplayMyBirdSightings.css';

export function DisplayMyBirdSightings({user_id, username}) {
    const [birdSightings, setBirdSightings] = useState([]);
    console.log("bird data", birdSightings)
    const [error, setError] = useState(null);

    useEffect(() => {
        if(!user_id) return;

        const fetchBirdSightings = async () => {
            try {
                const token = localStorage.getItem("token");
                getMyBirdSightings(token)
                .then((data) => {
                    setBirdSightings(data)
                })

            } catch (err) {
                console.error(
                    "Failed to fetch recipes DisplayMyRecipes.jsx Component - line 20:", err);
                setError(err.message);
            }
            
        };
        fetchBirdSightings();
    }, [user_id])
        
    if (error) return <p>Error: {error}</p>
    if (!birdSightings.length) return <p>No sightings uploaded yet.</p>

    return (
        <div className="sightings-list" role="sightings-list">
    {birdSightings.map((birdSighting) => (
        <div className="individual-sighting-card" role="individual-sighting-card" key={birdSighting.id}>
            <BirdSighting birdSighting={birdSighting} username={username} />
        </div>
    ))}
        </div>)
}