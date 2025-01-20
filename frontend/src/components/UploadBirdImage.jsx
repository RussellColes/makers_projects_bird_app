import { useState } from "react";
import { uploadBirdSighting } from "../services/sightings"; 
// const BACKEND_URL = import.meta.env.BACKEND_URL; - hardcoded in and needs looking at
// import { recognizeBirdFile } from "../services/users";
import { VALID_BIRDS } from "../../utils/valid_birds";
import './UploadBirdImage.css';

export function UploadImage() {
  const [file, setFile] = useState(null);
  const [birdName, setBirdName] = useState("");
  const [location, setLocation] = useState("");
  const [error, setError] = useState(null);
  // const [isLoading, setIsLoading] = useState(false);
  // const [uploadedImages, setUploadedImages] = useState([]);

  const current_user_string = localStorage.getItem("currentUser")
  const current_user = JSON.parse(current_user_string)
  const token = localStorage.getItem("token")

   // Validate bird name
  const validateBirdName = (name) => {
    if (!name) return false;
    return VALID_BIRDS.includes(name.toLowerCase().trim());
  };
  
  // Handle file selection and bird recognition
  const handleFileChange = async (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setBirdName(""); // Reset previous bird name
    setError(null);
  };

  // Upload file with bird name and location
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return alert("Please select an image.");

    if (birdName.toLowerCase() === "chicken") {
      setError("404 Not Found!");
      return;
    }
    // Validate bird name before submission
    if (birdName && !validateBirdName(birdName)) {
      setError("Squawk! That doesn't sound like a bird!");
      return;
    } 

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("user_id", current_user.id)

      if (birdName) {
        formData.append("birdName", birdName); // Append bird name if provided
      }
      if (location) {
        formData.append("location", location); // Append location if provided
      }
      const result = await uploadBirdSighting(token, formData);
      console.log("Upload successful:", result);
      // setUploadedImages((prevImages) => [...prevImages, result.image]);

      setFile(null);
      setBirdName("");
      setLocation("");
      setError(null);
      window.location.reload()
    } catch {
      setError("Upload failed. Please try again.");
    }
  };

  return (
    <div className='upload-container'>
    <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column" }}>
      <label>Upload Bird Image:</label>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      {/* {isLoading && <p>Recognizing bird...</p>} */}

      <label>Bird Name:</label>
      <input
        type="text"
        value={birdName}
        onChange={(e) => setBirdName(e.target.value)}
        placeholder="Enter bird name (e.g., Robin, Blue Jay)"
      />
      <label>Location:</label>
      <input
        type="text"
        value={location}
        onChange={(e) => setLocation(e.target.value)}
        placeholder="Enter location"
        />
        <div className="upload-button">
          <button type="submit">Upload</button>
        </div>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </form>
    </div>
    )
    }

//       <div className="gallery">
//         {uploadedImages.map((url, index) => (
//           <img
//             key={index}
//             src={`http://localhost:8000/bird_uploads/${url}`}
//             alt={`Uploaded ${index + 1}`}
//             style={{ width: "150px", margin: "10px", borderRadius: "8px" }}
//           />
//         ))}
//       </div>
// );


// disabled={isLoading} from line 123 submit button


 //  API STUFF THAT DOESN'T WORK
  // 
  //   if (selectedFile) {
  //     setIsLoading(true);
  //     try {
  //       const result = await recognizeBirdFile("API_URL", selectedFile);
  //       setBirdName(result.birdName || "Unknown Bird");
  //     } catch {
  //       setError("Bird recognition failed.");
  //     } finally {
  //       setIsLoading(false);
  //     }
  //   }

  // API RELATED CODE vv

//       formData.append("birdName", birdName);
//       formData.append("location", location);
//       await uploadUserFile(token, formData);
//       alert("File uploaded successfully!");