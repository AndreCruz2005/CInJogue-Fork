import axios from "axios";
import React, { useEffect, useState } from "react";
import { backend } from "../global";
import "../styles/library.css";

export const Library = ({ userData, setUserData, library, setLibrary }) => {

	const GameCard = (g) => {
		return <img src={g.data.image.original_url} alt={g.title}></img>;
	};

	const GameLibrary = () => {
		let lst = [];
		Object.entries(library ? library : {}).forEach((item) =>
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
