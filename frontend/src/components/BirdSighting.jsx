import { Link } from "react-router-dom";
import { BirdImageDisplay } from "../components/BirdImageDisplay";
import './BirdSighting.css';

function BirdSighting({ birdSighting, username }) {
    const birdImageFilepath = birdSighting.image;
    const dateSpotted = birdSighting.date_spotted;
    const locationSpotted = birdSighting.location;
    console.log(birdImageFilepath);
    return (
        <div className="bird-sighting-container">
            <div className="bird-sighting-card">
                <div className="grid-container-bird-sighting">
                    <BirdImageDisplay filepath={birdImageFilepath} />
                    <Link
                        className="birdSighting-title-link"
                        to={`/sightings/${username}/${birdSighting.id}`}>
                        {birdSighting.bird_name}
                    </Link>
                    <h5>Location Spotted: {locationSpotted}</h5>
                    <h5>Date Spotted: {dateSpotted}</h5>
                </div>
            </div>
        </div>
    );
}

export default BirdSighting;