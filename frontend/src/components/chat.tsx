import axios from "axios";
import React, { useEffect, useState } from "react";
import { backend } from "../global";
import "../styles/chat.css";

export const Chat = ({ userData, setUserData, library, setLibrary, recommendations, setRecommendations }: any) => {
	const [input, setInput] = useState("");
	const [output, setOutput] = useState("");

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

	function fetchRecommendations() {
		axios
			.post(`${backend}/getrecommendations`, {
				username: userData.username,
				password: userData.password,
			})
			.then((response) => {
				setRecommendations(response.data);
				console.log(response.data);
			})
			.catch((e) => console.error(e));
	}

	const sendMessage = () => {
		axios
			.post(`${backend}/genai`, {
				prompt: input,
				username: userData.username,
				password: userData.password,
			})
			.then((response) => {
				setOutput(`${response.data[0].message}`);
				fetchLibrary();
				fetchRecommendations();
			})
			.catch((error) => console.error(error));
	};

	const RecommendationsGrid = () => {
		let lst: any[] = [];
		Object.entries(recommendations ? recommendations : {}).forEach((item: any) =>
			lst.push({ title: item[0], data: item[1].data }),
		);

		return (
			<div id="recommendations-grid">
				{lst.map((it) => {
					return <img src={it.data.image.original_url} alt={it.title}></img>;
				})}
			</div>
		);
	};

	useEffect(() => {
		fetchLibrary();
		fetchRecommendations();
	}, []);

	return (
		<div id="chat">
			<text id="output">{output}</text>
			<RecommendationsGrid />
			<div id="input-and-send">
				<input onChange={(e) => setInput(e.target.value)} value={input} placeholder="Digite sua mensagem"></input>
				<button
					onClick={() => {
						sendMessage();
					}}
				>
					ENVIAR
				</button>
			</div>
		</div>
	);
};
