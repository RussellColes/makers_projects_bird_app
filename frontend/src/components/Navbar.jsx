import React from "react";
import "./Navbar.css";

export function Navbar() {
  return (
    <nav className='navbar'>
      <ul>
        <li>
          <a href='/myprofile'>My Profile</a>
        </li>
        <li>
          <a href='/team'>Team</a>
        </li>
        <li>
          <a href='/'>Log out</a>
        </li>
      </ul>
    </nav>
  );
}
