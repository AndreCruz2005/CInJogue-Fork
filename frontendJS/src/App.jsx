import { useState, useEffect } from "react";
import { Login } from "./components/login";
import { Signup } from "./components/signup";
import { Library } from "./components/library";
import { Chat } from "./components/chat";
import "./styles/App.css";
import axios from "axios";

function App() {
	const [userData, setUserData] = useState(null);
	const [library, setLibrary] = useState(null);
	const [recommendations, setRecommendations] = useState(null);

	return userData == null ? (
		<InitialScreen userData={userData} setUserData={setUserData} />
	) : (
		<LibraryScreen
			userData={userData}
			setUserData={setUserData}
			library={library}
			setLibrary={setLibrary}
			recommendations={recommendations}
			setRecommendations={setRecommendations}
		/>
	);
}

const InitialScreen = ({ userData, setUserData }) => {
	return (
		<div id="initial-screen">
			<Signup />
			<Login userData={userData} setUserData={setUserData} />
		</div>
	);
};

const LibraryScreen = ({ userData, setUserData, library, setLibrary, recommendations, setRecommendations }) => {
	return (
		<div id="library-screen">
			<Library
				userData={userData}
				setUserData={setUserData}
				library={library}
				setLibrary={setLibrary}
				recommendations={recommendations}
				setRecommendations={setRecommendations}
			/>
			<Chat
				userData={userData}
				setUserData={setUserData}
				library={library}
				setLibrary={setLibrary}
				recommendations={recommendations}
				setRecommendations={setRecommendations}
			/>
		</div>
	);
};

export default App;