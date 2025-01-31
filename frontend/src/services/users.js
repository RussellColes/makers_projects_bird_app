const BACKEND_URL = import.meta.env.BACKEND_URL;

export async function getUsers(token) {
  const requestOptions = {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };

  const response = await fetch(`${BACKEND_URL}/users`, requestOptions);

  if (response.status !== 200) {
    throw new Error("Unable to fetch users");
  }

  const data = await response.json();
  return data;
}

export async function getUserInfo(token) {
  const requestOptions = {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };

  const response = await fetch(`${BACKEND_URL}/users/profile`, requestOptions);

  if (response.status !== 200) {
    throw new Error("Unable to fetch users");
  }

  return await response.json();
}

export async function getAnotherUserInfo(token, username) {
  const requestOptions = {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };

  const response = await fetch(`${BACKEND_URL}/users/profile/${username}`, requestOptions);

  if (response.status !== 200) {
    throw new Error("Unable to fetch users");
  }

  return await response.json();
}

export const updateUserInfo = async (token, userData) => {
  const response = await fetch(`${BACKEND_URL}/users/profile`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
    },
    body: JSON.stringify(userData),  
  });

  return await response.json();
};

export const getUserByUsername = async (friendUsername, token) => {
  const requestOptions = {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };

  const response = await fetch(`${BACKEND_URL}/users/${friendUsername}`, requestOptions);

  if (response.status !== 200) {
    throw new Error(`Unable to fetch user info for user`);
  }

  return await response.json();
}



// Function to handle image recognition using a bird recognition API
export async function recognizeBirdFile(apiUrl, imageFile) {
  const formData = new FormData();
  formData.append("image", imageFile);

  const response = await fetch(apiUrl, { method: "POST", body: formData });

  if (!response.ok) throw new Error("Bird recognition failed.");
  
  return await response.json();
}