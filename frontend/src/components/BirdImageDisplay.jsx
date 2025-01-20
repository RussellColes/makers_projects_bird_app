const BACKEND_URL = import.meta.env.BACKEND_URL || "http://localhost:8000";
// import "../assets/App.css"

export function BirdImageDisplay({ filepath }) {
    return (
        <div>
            <img 
            className="image" 
            src={`${BACKEND_URL}/uploads/${filepath}`} 
            width="100"></img>
        </div>
    );
}