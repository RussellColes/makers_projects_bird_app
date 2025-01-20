import { jwtDecode } from 'jwt-decode';

const BACKEND_URL = import.meta.env.BACKEND_URL || "http://localhost:8000";

console.log("<==== services/sightings.js says ====>\nBackend url: ", BACKEND_URL, "FIX THE ENV FILE")

export async function getAllSightings(token) {
    const requestOptions = {
        method: "GET",
        headers: {
            Authorization: `Bearer ${token}`
        }
    }
    const response = await fetch(`${BACKEND_URL}/sightings`, requestOptions);

    if (response.status !== 200) {
        throw new Error("Unable to fetch users");
    }
    const data = await response.json();
    return data;
}

export async function getSighting({token, sighting_id}) {
    const requestOptions = {
        method: "GET",
        headers: {
            Authorization: `Bearer ${token}`
        }
    }
    const response = await fetch(`${BACKEND_URL}/sighting/${sighting_id}`, requestOptions);

    if (response.status !== 200) {
        throw new Error("Unable to fetch users");
    }
    const data = await response.json();
    return data;
}

export async function getMyBirdSightings(token) {
    const requestOptions = {
        method: "GET",
        headers: {
            Authorization: `Bearer ${token}`
        }
    }

    // Destringify token; Get id from token; Put token id into URL placeholder
    const user_id = jwtDecode(token).sub.id

    const response = await fetch(`${BACKEND_URL}/sightings/${user_id}`, requestOptions);
    if (response.status !== 200) {
        throw new Error("Unable to fetch sightings");
    }
    const data = await response.json();
    console.log("HERE IS THE DATA", data)
    return data;
}

// Create new bird-sighting & recipe
export async function uploadBirdSighting(token, formData) {
    console.log("formData recipes services line 28 --->", JSON.stringify(formData))
    const response = await fetch(`${BACKEND_URL}/bird_sighting`, { 
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        // "Content-Type": "multipart/form-data",
      },
      body: formData,
    });
  
    if (!response.ok) {
      throw new Error("Failed to upload the image.");
    }
  
    const result = await response.json();
    console.log("Upload successful:", result);
    return result;
  }
