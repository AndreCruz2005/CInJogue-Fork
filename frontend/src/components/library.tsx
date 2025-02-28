import axios from "axios";
import React, { useEffect, useState } from "react";
import { backend, LoginProps } from "../global";
import "../styles/library.sass";

export const Library = ({ userData, setUserData }: LoginProps) => {
	type Game = {
		title: string;
		data: any;
		rating: number;
		state: string;
	};

	type Library = {
		[title: string]: Game;
	};

	const [library, setLibrary] = useState<Library | null>(null);

	function fetchLibrary() {
		axios
			.post(`${backend}/getlibrary`, {
				username: userData.username,
				password: userData.password,
			})
			.then((response) => {
				setLibrary(response.data);
				console.log(response.data);
			})
			.catch((e) => console.error(e));
	}

	const GameCard = (g: Game) => {
		return (
			<div id="game-card-display">
				<p>{g.title}</p>
				<img src={g.data.image.original_url} alt={g.title}></img>
				<p>{g.rating}</p>
				<p>{g.state}</p>
			</div>
		);
	};

	const GameLibrary = () => {
		console.log(library);
		let lst: Game[] = [];
		Object.entries(library ? library : {}).forEach((item) =>
			lst.push({ title: item[0], rating: item[1].rating, state: item[1].state, data: item[1].data }),
		);

		return (
			<div>
				{lst.map((it) => {
					return <GameCard title={it.title} rating={it.rating} state={it.state} data={it.data} />;
				})}
			</div>
		);
	};

	return (
		<div id="library">
			<button onClick={fetchLibrary}>UPDATE</button>
			<br></br>
			<GameLibrary />
		</div>
	);
};
