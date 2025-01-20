import React from "react";
import { useParams } from "react-router-dom";
import { Navbar } from "../components/Navbar";
import './IndividualBirdSighting.css';

export const IndividualBirdSighting = () => {
    const { username, sighting_id } = useParams();

    return (
        <>
        <Navbar />
        <div className="contacts-container">
            <h1>Recipes</h1>
            <h3>Recipes go here...</h3>
            </div>
        </>
    );
};