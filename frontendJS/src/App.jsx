import { useState, useEffect } from "react";
import { Auth } from "./components/auth";
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
					<svg
						width="60px"
						height="60px"
						viewBox="0 0 24 24"
						fill="none"
						xmlns="http://www.w3.org/2000/svg"
						stroke="#ffffff"
					>
						<g id="SVGRepo_bgCarrier" stroke-width="0" />
						<g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round" />
						<g id="SVGRepo_iconCarrier">
							<path
								d="M5 21C5 17.134 8.13401 14 12 14C15.866 14 19 17.134 19 21M16 7C16 9.20914 14.2091 11 12 11C9.79086 11 8 9.20914 8 7C8 4.79086 9.79086 3 12 3C14.2091 3 16 4.79086 16 7Z"
								stroke="#ffffff"
								stroke-width="2"
								stroke-linecap="round"
								stroke-linejoin="round"
							/>
						</g>
					</svg>
				</button>
				<button
					onClick={() => {
						getPrefs();
						setPrefsStatus(true);
					}}
				>
					<svg width="60px" height="60px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
						<g id="SVGRepo_bgCarrier" strokeWidth="0" />
						<g id="SVGRepo_tracerCarrier" strokeLinecap="round" strokeLinejoin="round" />
						<g id="SVGRepo_iconCarrier">
							<path
								d="M15.7 4C18.87 4 21 6.98 21 9.76C21 15.39 12.16 20 12 20C11.84 20 3 15.39 3 9.76C3 6.98 5.13 4 8.3 4C10.12 4 11.31 4.91 12 5.71C12.69 4.91 13.88 4 15.7 4Z"
								stroke="#ffffff"
								strokeWidth="2"
								strokeLinecap="round"
								strokeLinejoin="round"
							/>
						</g>
					</svg>
				</button>
				<button
					onClick={() => {
						getBlacklist();
						setBlacklistStatus(true);
					}}
				>
					<svg width="60px" height="60px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
						<g id="SVGRepo_bgCarrier" stroke-width="0" />
						<g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round" />
						<g id="SVGRepo_iconCarrier">
							<path
								d="M15 18.5L20 13.5M20 18.5L15 13.5"
								stroke="#ffffff"
								stroke-width="1.5"
								stroke-linecap="round"
								stroke-linejoin="round"
							/>
							<path d="M11 14L3 14" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round" />{" "}
							<path d="M11 18H3" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round" />{" "}
							<path d="M3 6L13.5 6M20 6L17.75 6" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round" />{" "}
							<path d="M20 10L9.5 10M3 10H5.25" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round" />{" "}
						</g>
					</svg>
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
					<svg width="60px" height="60px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
						<g id="SVGRepo_bgCarrier" stroke-width="0" />
						<g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round" />
						<g id="SVGRepo_iconCarrier">
							{" "}
							<g id="Interface / Log_Out">
								<path
									id="Vector"
									d="M12 15L15 12M15 12L12 9M15 12H4M9 7.24859V7.2002C9 6.08009 9 5.51962 9.21799 5.0918C9.40973 4.71547 9.71547 4.40973 10.0918 4.21799C10.5196 4 11.0801 4 12.2002 4H16.8002C17.9203 4 18.4796 4 18.9074 4.21799C19.2837 4.40973 19.5905 4.71547 19.7822 5.0918C20 5.5192 20 6.07899 20 7.19691V16.8036C20 17.9215 20 18.4805 19.7822 18.9079C19.5905 19.2842 19.2837 19.5905 18.9074 19.7822C18.48 20 17.921 20 16.8031 20H12.1969C11.079 20 10.5192 20 10.0918 19.7822C9.71547 19.5905 9.40973 19.2839 9.21799 18.9076C9 18.4798 9 17.9201 9 16.8V16.75"
									stroke="#ffffff"
									stroke-width="2"
									stroke-linecap="round"
									stroke-linejoin="round"
								/>
							</g>
						</g>
					</svg>
				</button>
			</div>
		);
	};

	return userData == null ? (
		<Auth userData={userData} setUserData={setUserData} />
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
