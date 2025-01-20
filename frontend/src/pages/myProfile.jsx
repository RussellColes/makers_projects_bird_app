import { useEffect, useState } from "react";
import { Navbar } from "../components/Navbar"; 
import { PhotoDisplay } from "../components/PhotoDisplay";
import { useNavigate } from "react-router-dom";
// import { UserDetails } from "../components/UserDetails";
// import { getUserInfo } from "../services/users";
// import { PhotoUpload } from "../../components/PhotoUpload";
import { UploadImage } from "../components/UploadBirdImage";
import { DisplayMyBirdSightings } from "../components/DisplayMyBirdSightings";
// import { getRecipesForUser } from "../services/recipes";
import pluckerIcon from "../assets/icon/pluckers.png";
import "./MyProfile.css";
import { ImageForm } from "../components/ProfileImageForm";

export function MyProfile() {

  // const goToRecipe = () => {
  //   //add to go to recipe functionality here
  //   console.log("Recipe Clicked");}

    const [username, setUsername] = useState("");
    const [user_id, setUserId] = useState("");
    const [profile_picture, setProfilePicture] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
      const token = localStorage.getItem("token");
      const current_user_string = localStorage.getItem("currentUser");
      const current_user = JSON.parse(current_user_string);
        if (!token) {
            console.error("No token found - myProfile.jsx line 30; redirect to login");
            navigate("/login");
            return;
        }

        // Set user details
        if (current_user) {
            setUsername(current_user.username);
            setProfilePicture(current_user.profile_picture);
            setUserId(current_user.id);
        }

        // Example API call - uncomment if you need real user data
        // getUserInfo(token).then((data) => {
        //     localStorage.setItem("token", data.token);
        // });
    }, [username, profile_picture, user_id, navigate]);

    return (
    <>
    <Navbar />
      <div className='main-container'>
        <div className='plucker-logo-my-profile'>
          <img src={pluckerIcon} alt='Plucker logo' />
        </div>
          <div className='user-container'>
            <h3>{username}</h3>
            <div className="profile-picture">
              <div className="photo">
                <PhotoDisplay profile_picture={profile_picture} />
              </div>
            </div>
            <div>
              <ImageForm />
            </div>
          <div className="upload-image">
            <UploadImage />
          </div>
        </div>
        <div className='recipe-card'>
          <h1>Sightings:</h1>
          <DisplayMyBirdSightings user_id={user_id} username={username}/>
        </div>
        <br></br>
      </div>
      <div className='grid-item'></div>
    </>
  );
}
