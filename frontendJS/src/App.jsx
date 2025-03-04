import { useState, useEffect } from "react";
import { Login } from "./components/login";
import { Signup } from "./components/signup";
import { Library } from "./components/library";
import { Chat } from "./components/chat";
import axios from "axios";
import { backend } from "./global";

// Icons
import UserIcon from "./assets/user_icon.svg";
import Preferences from "./assets/preferences.svg";
import Blacklist from "./assets/blacklist.svg";
import Logout from "./assets/logout.svg";

// Styles
import "./styles/App.css";
import "./styles/infobox.css";
import "./styles/blacklist.css";
import "./styles/profile-box.css";
import "./styles/preferences.css";

function App() {
	const [userData, setUserData] = useState(null);
	const [library, setLibrary] = useState(null);
	const [recommendations, setRecommendations] = useState(null);

	const [blacklistStatus, setBlacklistStatus] = useState(false);
	const [blacklist, setBlacklist] = useState(null);

	const [profileBoxStatus, setProfileBoxStatus] = useState(false);

	const [prefsStatus, setPrefsStatus] = useState(false);
	const [prefs, setPrefs] = useState(null);
	const tagTypes = ["Plataformas", "Gêneros", "Temas", "Classificações Etárias"];

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
				console.log(response.data);
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

	const ProfileBox = () => {
		const [oldPassword, setOldPassword] = useState("");
		const [newPassword, setNewPassword] = useState("");
		const [passwordConfirm, setPasswordConfirm] = useState("");
		const [deletePassword, setDeletePassword] = useState("");

		function changePassword() {
			axios
				.post(`${backend}/changepassword`, {
					username: userData.username,
					oldPassword: oldPassword,
					newPassword: newPassword,
				})
				.then((response) => {
					if (response.data === true) {
						setUserData({ ...userData, password: newPassword });
					}
				})
				.catch((error) => {
					console.error(error);
				});
		}

		function deleteAccount() {
			setUserData(null);
			axios
				.post(`${backend}/removeuser`, {
					username: userData.username,
					password: deletePassword,
				})
				.then(() => {})
				.catch((error) => {
					console.error(error);
				});
		}

		return !profileBoxStatus ? null : (
			<div id="profile-box-layer">
				<div id="profile-box">
					<div id="header">
						<h2>CONFIGURAÇÕES DE CONTA</h2>
						<button onClick={() => setProfileBoxStatus(false)}>X</button>
					</div>
					<div id="options">
						<h3>SEUS DADOS</h3>
						<p>Nome de usuário: {userData.username}</p>
						<p>Email: {userData.email}</p>
						<p>Data de nascimento: {userData.birthdate}</p>
						<p>ID: {userData.id}</p>

						<h3>MUDE SUA SENHA</h3>
						<label>
							Senha atual:
							<input onChange={(e) => setOldPassword(e.target.value)} type="password"></input>
						</label>
						<label>
							Nova senha:
							<input onChange={(e) => setNewPassword(e.target.value)} type="password"></input>
						</label>
						<label>
							Confirme nova senha:
							<input onChange={(e) => setPasswordConfirm(e.target.value)} type="password"></input>
						</label>
						<button
							onClick={() => {
								if (passwordConfirm == newPassword) changePassword();
							}}
						>
							Mudar senha
						</button>

						<h3>DANGER ZONE</h3>
						<label>
							Senha:
							<input onChange={(e) => setDeletePassword(e.target.value)} type="password"></input>
						</label>
						<button onClick={deleteAccount}>Deletar conta</button>
					</div>
				</div>
			</div>
		);
	};

	const Preferences = () => {
		function addTags(text, type) {
			axios
				.post(`${backend}/addtags`, {
					username: userData.username,
					password: userData.password,
					text: text,
					tag_type: type,
				})
				.then(() => {
					getPrefs();
				})
				.catch((error) => {
					console.error(error);
				});
		}

		function removeTags(text) {
			axios
				.post(`${backend}/removetags`, {
					username: userData.username,
					password: userData.password,
					text: text,
				})
				.then(() => {
					getPrefs();
				})
				.catch((error) => {
					console.error(error);
				});
		}

		const Tag = ({ text }) => {
			return (
				<div id="tag">
					<text>{text}</text>
					<button
						onClick={() => {
							removeTags(text);
						}}
					>
						X
					</button>
				</div>
			);
		};

		const TagManager = ({ type }) => {
			return (
				<div id="tag-manager">
					<h3>{type}</h3>
					<div id="tag-area">
						{prefs && type in prefs
							? prefs[type].map((tag) => {
									return <Tag text={tag} />;
							  })
							: null}
					</div>

					<input
						id="tag-input"
						onKeyDown={(e) => {
							if (e.key === "Enter") {
								addTags(e.target.value, type);
							}
						}}
					></input>
				</div>
			);
		};

		return !prefsStatus ? null : (
			<div id="prefs-layer">
				<div id="prefs-box">
					<div id="header">
						<h2>PREFERÊNCIAS</h2>
						<button
							onClick={() => {
								setPrefsStatus(false);
							}}
						>
							X
						</button>
					</div>
					<p>Digite tags e as adicione pressionando ENTER. As tags guiarão a resposta do modelo de IA.</p>
					{tagTypes.map((tag) => {
						return <TagManager type={tag} />;
					})}
				</div>
			</div>
		);
	};

	const Blacklist = () => {
		const BlacklistEntry = ({ title }) => {
			function removeEntry() {
				axios
					.post(`${backend}/unblacklistgame`, {
						username: userData.username,
						password: userData.password,
						title: title,
					})
					.then((response) => {
						getBlacklist();
					})
					.catch((error) => {
						console.error(error);
					});
			}
			return (
				<div>
					<text>{title}</text>
					<button onClick={removeEntry}>X</button>
				</div>
			);
		};

		return !blacklistStatus ? null : (
			<div id="blacklist-layer">
				<div id="blacklist-box">
					<div id="header">
						<h2>BLACKLIST</h2>
						<button onClick={() => setBlacklistStatus(false)}>X</button>
					</div>
					<text>Os jogos exibidos aqui não serão recomendados pelo assistente de IA</text>
					<div id="blacklist">
						{blacklist
							? blacklist.map((it) => {
									console.log(it);
									return <BlacklistEntry title={it} />;
							  })
							: null}
					</div>
				</div>
			</div>
		);
	};

	return userData == null ? (
		<InitialScreen userData={userData} setUserData={setUserData} />
	) : (
		<div id="App">
			<ProfileBox />
			<Preferences />
			<Blacklist />
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
