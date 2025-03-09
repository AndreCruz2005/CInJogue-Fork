import axios from "axios";
import { backend } from "../global";
import "./../styles/preferences.css";

export const Preferences = ({ userData, prefs, getPrefs, prefsStatus, setPrefsStatus }) => {
	const tagTypes = ["Plataformas", "Gêneros", "Temas", "Classificações Etárias"];

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
