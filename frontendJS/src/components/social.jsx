import axios from "axios";
import { useState } from "react";
import { backend } from "../global";
import "./../styles/social.css";

export const Social = ({ userData, socialStatus, setSocialStatus }) => {
	const [searchedUser, setSearchedUser] = useState(userData.username);
	const [visualizedLibrary, setVisualizedLibrary] = useState([]);

	function fetchLibrary() {
		axios
			.get(`${backend}/getlibrary?username=${searchedUser}`)
			.then((response) => {
				setVisualizedLibrary(response.data);
				console.log(response.data);
			})
			.catch((e) => {
				console.error(e);
				setVisualizedLibrary([]);
			});
	}

	const LibraryItem = ({ game }) => {
		return (
			<div id="library-item">
				<p>{game.title}</p>
				<img src={game.data.image.original_url}></img>
				<p>{game.state}</p>
				<p>{game.rating}/10</p>
			</div>
		);
	};

	return socialStatus ? (
		<div id="social-layer">
			<div id="social-box">
				<div id="header">
					<h2>COMPARTILHAR</h2>
					<button
						onClick={() => {
							setSocialStatus(false);
						}}
					>
						X
					</button>
					<p>Insira o nome de um usuário e pressione ENTER para visualizar sua biblioteca aqui.</p>
					<input
						value={searchedUser}
						onChange={(e) => setSearchedUser(e.target.value)}
						onKeyDown={(e) => {
							if (e.key == "Enter") {
								fetchLibrary();
							}
						}}
					></input>
				</div>
				<div id="visualized-library">
					{visualizedLibrary.map((it, i) => {
						return <LibraryItem key={i} game={it} />;
					})}
				</div>
			</div>
		</div>
	) : null;
};
