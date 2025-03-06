import { useState, useEffect } from "react";
import { Auth } from "./components/auth";
import { Library } from "./components/library";
import { Chat } from "./components/chat";
import { ProfileBox } from "./components/profile-box";
import { Preferences } from "./components/preferences";
import { Blacklist } from "./components/blacklist";
import axios from "axios";
import { backend } from "./global";

// Icons
import profileIcon from "./assets/user_icon.svg";
import preferencesIcon from "./assets/preferences.svg";
import blacklistIcon from "./assets/blacklist.svg";
import logoutIcon from "./assets/logout.svg";

// Styles
import "./styles/App.css";
import "./styles/infobox.css";

function App() {
	const [serverStatus, setServerStatus] = useState(null);
	useEffect(() => {
		const interval = setInterval(() => {
			axios
				.get(`${backend}`)
				.then((response) => {
					response.status == 200 ? setServerStatus(true) : serverStatus(false);
				})
				.catch(() => {
					setServerStatus(false);
				});
		}, 5000);

		return () => clearInterval(interval);
	}, []);

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
					<img src={profileIcon} />
				</button>
				<button
					onClick={() => {
						getPrefs();
						setPrefsStatus(true);
					}}
				>
					<img src={preferencesIcon} />
				</button>
				<button
					onClick={() => {
						getBlacklist();
						setBlacklistStatus(true);
					}}
				>
					<img src={blacklistIcon} />
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
					<img src={logoutIcon} />
				</button>
			</div>
		);
	};

	return userData == null ? (
		<div>
			<div id="backend-status" className={serverStatus ? "ok" : "not-ok"}>
				<label>Backend ({serverStatus ? "Online" : "Offline"})</label>
				<a href={import.meta.env.VITE_BACKEND_URL}>{import.meta.env.VITE_BACKEND_URL}</a>
			</div>
			<Auth userData={userData} setUserData={setUserData} />
		</div>
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
