import React from "react";
import "./Team.css";
import { Navbar } from "../components/Navbar";
import pluckerIcon from "../assets/icon/pluckers.png";

export function Team() {
  return (
    <>
      <Navbar />
        <div className='plucker-logo-my-profile'>
          <img src={pluckerIcon} alt='Plucker logo' />
        </div>
      <div className="team-container">
        <h1>Meet the Pluckers</h1>
        <div className="team-member">
          <h3>Ben Cole</h3>
          <a href="https://github.com/benawcole">Github</a>
        </div>
        <div className="team-member">
          <h3>Russell Coles</h3>
          <a href="https://github.com/russellColes">Github</a>
        </div>
        <div className="team-member">
          <h3>Doug Fairfield</h3>
          <a href="https://github.com/DougF-5749">Github</a>
        </div>
        <div className="team-member">
          <h3>Max Joseph</h3>
          <a href="https://github.com/maxjoseph22">Github</a>
        </div>
        <div className="team-member">
          <h3>John O'Neill</h3>
          <a href="https://github.com/JohnHertility">Github</a>
        </div>
        <div className="team-member">
          <h3>Alberto Tobarra</h3>
          <a href="https://github.com/altota90">Github</a>
        </div>
      </div>
    </>
  );
}
