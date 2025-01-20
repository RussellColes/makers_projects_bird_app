import {useState} from "react";
const BACKEND_URL = import.meta.env.BACKEND_URL || "http://localhost:8000";
import './ProfileImageForm.css';

export const ImageForm = () => {
  const [file, setFile] = useState();
  const current_user_string = localStorage.getItem("currentUser");
  const currentUser = JSON.parse(current_user_string);
  const token = localStorage.getItem("token")

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("user_id", currentUser.id)
    formData.append("file", file);

    const response = await fetch(`${BACKEND_URL}/files/upload`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`
      },
      body: formData,
    });

    // RESET LOCAL STORAGE
    const result = await response.json()
    const filepath = result.filepath
    currentUser.profile_picture = filepath
    localStorage.setItem("currentUser", JSON.stringify(currentUser))
    window.location.reload();
  };
  return (
    <>
      <div className="file">
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      </div>
      <div className="upload-photo">
        <button onClick={handleUpload}>Upload photo</button>
      </div>
    </>
  );
};
