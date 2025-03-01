import axios from "axios";
import React, { useEffect, useState } from "react";
import { backend, LoginProps } from "../global";
import "../styles/library.css";

export const Library = ({ userData, setUserData, library, setLibrary }: any) => {
	type Game = {
		title: string;
		data: any;
		rating: number;
		state: string;
	};

	const GameCard = (g: Game) => {
		return <img src={g.data.image.original_url} alt={g.title}></img>;
	};

	const GameLibrary = () => {
		let lst: Game[] = [];
		Object.entries(library ? library : {}).forEach((item: any) =>
			lst.push({ title: item[0], rating: item[1].rating, state: item[1].state, data: item[1].data }),
		);

		return (
			<div id="library">
				{lst.map((it) => {
					return <GameCard title={it.title} rating={it.rating} state={it.state} data={it.data} />;
				})}
			</div>
		);
	};

	return <GameLibrary />;
};
