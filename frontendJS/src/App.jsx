import { useState, useEffect } from "react";
import { Auth } from "./components/auth";
import { Library } from "./components/library";
import { Chat } from "./components/chat";
import { ProfileBox } from "./components/profile-box";
import { Preferences } from "./components/preferences";
import { Blacklist } from "./components/blacklist";
import { Social } from "./components/social";
import axios from "axios";
import { backend } from "./global";

// Ícones
import profileIcon from "./assets/user_icon.svg";
import preferencesIcon from "./assets/preferences.svg";
import blacklistIcon from "./assets/blacklist.svg";
import logoutIcon from "./assets/logout.svg";
import shareIcon from "./assets/share.svg";

// Estilos
import "./styles/App.css";
import "./styles/infobox.css";

function App() {
	// Estado para armazenar dados do usuário (null == usuário não logado)
	const [userData, setUserData] = useState(null);

	// Estados biblioteca/recomendações
	const [library, setLibrary] = useState(null);
	const [recommendations, setRecommendations] = useState(null);

	// Estados não recomende
	const [blacklistStatus, setBlacklistStatus] = useState(false);
	const [blacklist, setBlacklist] = useState(null);

	// Estado para configurações de perfil
	const [profileBoxStatus, setProfileBoxStatus] = useState(false);

	// Estados preferências
	const [prefsStatus, setPrefsStatus] = useState(false);
	const [prefs, setPrefs] = useState(null);

	// Estados para tela social
	const [socialStatus, setSocialStatus] = useState(false);

	// Função para buscar a biblioteca do usuário
	function fetchLibrary() {
		axios
			.get(`${backend}/getlibrary?username=${userData.username}`)
			.then((response) => {
				setLibrary(response.data);
				console.log(response.data);
			})
			.catch((e) => console.error(e));
	}

	// Função para obter o não recomende do usuário
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
				console.error("Erro ao buscar lista negra:", error);
			});
	}

	// Função para obter as preferências do usuário
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
				console.error("Erro ao buscar preferências:", error);
			});
	}

	// Componente da barra lateral
	const SideBar = () => {
		return (
			<div id="side-bar">
				{/* Botão para abrir a caixa de perfil */}
				<button
					onClick={() => {
						setProfileBoxStatus(true);
					}}
				>
					<img src={profileIcon} />
				</button>
				{/* Botão para abrir a caixa social */}
				<button
					onClick={() => {
						setSocialStatus(true);
					}}
				>
					<img src={shareIcon} />
				</button>
				{/* Botão para abrir as preferências */}
				<button
					onClick={() => {
						getPrefs();
						setPrefsStatus(true);
					}}
				>
					<img src={preferencesIcon} />
				</button>
				{/* Botão para abrir o não recomende */}
				<button
					onClick={() => {
						getBlacklist();
						setBlacklistStatus(true);
					}}
				>
					<img src={blacklistIcon} />
				</button>
				{/* Botão para fazer logout */}
				<button
					onClick={() => {
						setUserData(null);
						setRecommendations(null);
						setLibrary(null);
						setBlacklist(null);
						setPrefs(null);
					}}
				>
					<img src={logoutIcon} />
				</button>
			</div>
		);
	};

	// Renderiza a tela de login/signup ou a biblioteca/chat dependendo se o usuário está logado ou não
	return userData == null ? (
		// Tela de login/signup
		<Auth userData={userData} setUserData={setUserData} />
	) : (
		<div id="App">
			<Social
				userData={userData}
				socialStatus={socialStatus}
				setSocialStatus={setSocialStatus}
				library={library}
				fetchLibrary={fetchLibrary}
			/>

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
				library={library}
				recommendations={recommendations}
				setRecommendations={setRecommendations}
				fetchLibrary={fetchLibrary}
			/>
		</div>
	);
}

// Componente para exibir a biblioteca e o chat
const LibraryScreen = ({ userData, library, recommendations, setRecommendations, fetchLibrary }) => {
	return (
		<div id="library-chat-container">
			<Library userData={userData} library={library} fetchLibrary={fetchLibrary} />
			<Chat
				userData={userData}
				recommendations={recommendations}
				setRecommendations={setRecommendations}
				fetchLibrary={fetchLibrary}
			/>
		</div>
	);
};

export default App;
