import axios from "axios";
import { useEffect, useState } from "react";
import { backend } from "../global";
import "./../styles/social.css";

export const Social = ({ userData, socialStatus, setSocialStatus, library, fetchLibrary }) => {
	const [searchedUser, setSearchedUser] = useState(userData.username);
	const [visualizedLibrary, setVisualizedLibrary] = useState([]);

	function fetchVisualizedLibrary() {
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
			<div
				id="library-item"
				className={library.some((it) => it.title == game.title) ? "in-library" : "not-in-library"}
				onClick={() => {
					axios
						.post(`${backend}/addgametolibrary`, {
							username: userData.username,
							password: userData.password,
							title: game.title,
						})
						.then(() => {
							fetchLibrary();
						});
				}}
			>
				<p>{game.title}</p>
				<img src={game.data.image.original_url}></img>
				<p>{game.state}</p>
				<p>{game.rating}/10</p>
			</div>
		);
	};

	useEffect(() => {
		fetchVisualizedLibrary();
	}, [socialStatus]);

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
				</div>
				<p>
					Insira o nome de um usuário e pressione ENTER para visualizar a biblioteca do usuário aqui. Clique em um jogo
					para adiciona-lo à sua própria biblioteca.
				</p>
				<input
					value={searchedUser}
					placeholder="Nome de usuário"
					onChange={(e) => setSearchedUser(e.target.value)}
					onKeyDown={(e) => {
						if (e.key == "Enter") {
							fetchVisualizedLibrary();
						}
					}}
				></input>
				<div id="visualized-library">
					{visualizedLibrary.map((it, i) => {
						return <LibraryItem key={i} game={it} />;
					})}
				</div>
				<div id="footer">
					<div></div>
					<span>Jogos em comum</span>
				</div>
			</div>
		</div>
	) : null;
};
