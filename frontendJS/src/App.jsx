import { useState, useEffect } from "react";
import { Login } from "./components/login";
import { Signup } from "./components/signup";
import { Library } from "./components/library";
import { Chat } from "./components/chat";
import { ProfileBox } from "./components/profile-box";
import { Preferences } from "./components/preferences";
import { Blacklist } from "./components/blacklist";
import axios from "axios";
import { backend } from "./global";

// Styles
import "./styles/App.css";
import "./styles/infobox.css";

function App() {
	const [userData, setUserData] = useState(null);
	const [library, setLibrary] = useState(null);
	const [recommendations, setRecommendations] = useState(null);

	const [blacklistStatus, setBlacklistStatus] = useState(false);
	const [blacklist, setBlacklist] = useState(null);

	const [profileBoxStatus, setProfileBoxStatus] = useState(false);

	const [prefsStatus, setPrefsStatus] = useState(false);
	const [prefs, setPrefs] = useState(null);

	function getBlacklist() {
		axios
			.post(`${backend}/getblacklist`, {
				username: userData.username,
				password: userData.password,
			})
			.then((response) => {
				setBlacklist(response.data);
			})
			.catch((error) => {
				console.error("Error fetching blacklist:", error);
			});
	}

	function getPrefs() {
		axios
			.post(`${backend}/gettags`, {
				username: userData.username,
				password: userData.password,
			})
			.then((response) => {
				setPrefs(response.data);
			})
			.catch((error) => {
				console.error("Error fetching blacklist:", error);
			});
	}
	const SideBar = () => {
		return (
			<div id="side-bar">
				<button
					onClick={() => {
						setProfileBoxStatus(true);
					}}
				>
					CONTA
				</button>
				<button
					onClick={() => {
						getPrefs();
						setPrefsStatus(true);
					}}
				>
					PREFERÊNCIAS
				</button>
				<button
					onClick={() => {
						getBlacklist();
						setBlacklistStatus(true);
					}}
				>
					BLACKLIST
				</button>
				<button
					onClick={() => {
						axios
							.post(`${backend}/logout`)
							.then(() => setUserData(null))
							.catch((error) => {
								console.log(error);
							});
					}}
				>
					SAIR
				</button>
			</div>
		);
	};

	return userData == null ? (
		<InitialScreen userData={userData} setUserData={setUserData} />
	) : (
		<div id="App">
			<ProfileBox
				userData={userData}
				setUserData={setUserData}
				profileBoxStatus={profileBoxStatus}
				setProfileBoxStatus={setProfileBoxStatus}
			/>

			<Preferences
				userData={userData}
				prefs={prefs}
				getPrefs={getPrefs}
				prefsStatus={prefsStatus}
				setPrefsStatus={setPrefsStatus}
			/>

			<Blacklist
				userData={userData}
				blacklist={blacklist}
				getBlacklist={getBlacklist}
				blacklistStatus={blacklistStatus}
				setBlacklistStatus={setBlacklistStatus}
			/>

			<SideBar />

			<LibraryScreen
				userData={userData}
				setUserData={setUserData}
				library={library}
				setLibrary={setLibrary}
				recommendations={recommendations}
				setRecommendations={setRecommendations}
			/>
		</div>
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
		<div id="library-chat-container">
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
