import axios from "axios";
import React, { useEffect, useState } from "react";
import { backend } from "../global";
import "../styles/chat.css";

export const Chat = ({ userData, setUserData, library, setLibrary, recommendations, setRecommendations }) => {
	const [input, setInput] = useState("");
	const [output, setOutput] = useState("Hi there, how can I help you today?");

	const [infoBoxData, setInfoBoxData] = useState(null);
	const [infoBoxStatus, setInfoBoxStatus] = useState(false);

	const InfoBox = () => {
		return !infoBoxStatus ? null : (
			<div id="info-box-layer">
				<div id="info-box">
					<div id="header">
						<text id="title">{infoBoxData.title}</text>
						<button id="close-button" onClick={() => setInfoBoxStatus(false)}>
							X
						</button>
					</div>
					<div id="content">
						<div id="image-container">
							<img src={infoBoxData.data.image.original_url} alt={infoBoxData.title} />
						</div>
						<div id="description-info-container">
							<textarea id="description" readOnly value={infoBoxData.data.deck}></textarea>
							<div id="other-info">
								<div id="game-info">
									<text>Platforms: {infoBoxData.data.platforms.map((platform) => platform.name).join(", ")}</text>
									<br />
									<text>Release: {infoBoxData.data.original_release_date}</text>
								</div>
								<div id="user-info">
									<button id="add-button">ADD TO LIBRARY</button>
									<button id="reject-button">REJECT</button>
									<button id="blacklist-button">BLACKLIST</button>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		);
	};

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
		let lst = [];
		Object.entries(recommendations ? recommendations : {}).forEach((item) =>
			lst.push({ title: item[0], data: item[1].data }),
		);

		return (
			<div id="recommendations-grid">
				{lst.map((it) => {
					return (
						<img
							src={it.data.image.original_url}
							alt={it.title}
							onClick={() => {
								setInfoBoxData({ title: it.title, rating: it.rating, state: it.state, data: it.data });
								setInfoBoxStatus(true);
							}}
						/>
					);
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
			<InfoBox />
			<div id="output">
				<label>AI Assistant</label>
				<text>{output}</text>
			</div>
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
