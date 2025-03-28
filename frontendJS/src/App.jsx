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

	// Estado para armazenar o status do backend
	const [serverStatus, setServerStatus] = useState(null);
	// Função para verificar o status do backend
	const checkServerStatus = () => {
		axios
			.get(`${backend}`)
			.then((response) => {
				response.status == 200 ? setServerStatus(true) : setServerStatus(false);
			})
			.catch(() => {
				setServerStatus(false);
			});
	};

	// Efeito para verificar o status do backend periodicamente somente na tela de login/signup
	// (quando o usuário não está logado)
	useEffect(() => {
		checkServerStatus();
		const interval = setInterval(() => {
			if (!userData) {
				checkServerStatus();
			}
		}, 3000);

		return () => clearInterval(interval);
	}, [userData]);

	// Renderiza a tela de login/signup ou a biblioteca/chat dependendo se o usuário está logado ou não
	return userData == null ? (
		<div>
			{/* Exibição do status do backend */}
			<div id="backend-status" className={serverStatus ? "ok" : "not-ok"}>
				<label>Backend ({serverStatus ? "Online" : "Offline"})</label>
				<a href={backend}>{backend}</a>
			</div>

			{/*Tela de login/signup*/}
			<Auth userData={userData} setUserData={setUserData} />
		</div>
	) : (
		<div id="App">
			<Social
				userData={userData}
				socialStatus={socialStatus}
				setSocialStatus={setSocialStatus}
				fetchLibrary={() => {
					axios
						.get(`${backend}/getlibrary?username=${userData.username}`)
						.then((response) => {
							setLibrary(response.data);
						})
						.catch((e) => {
							console.error(e);
						});
				}}
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
				setUserData={setUserData}
				library={library}
				setLibrary={setLibrary}
				recommendations={recommendations}
				setRecommendations={setRecommendations}
			/>
		</div>
	);
}

// Componente para exibir a biblioteca e o chat
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
