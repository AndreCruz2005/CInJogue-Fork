import axios from "axios";
import React, { useEffect, useState } from "react";
import { backend } from "../global";
import "../styles/chat.css";

import microphoneIcon from "../assets/microphone.svg";
import sendIcon from "../assets/send-message.svg";

export const Chat = ({ userData, setUserData, library, setLibrary, recommendations, setRecommendations }) => {
	const [input, setInput] = useState("");
	const [output, setOutput] = useState(
		"Olá, bem vindo à CInJogue! Envie uma mensagem para começar a construir sua biblioteca.",
	);

	const [infoBoxData, setInfoBoxData] = useState(null);
	const [infoBoxStatus, setInfoBoxStatus] = useState(false);
	const [currAvrgRating, setCurrAvrgRating] = useState(0);

	function getGameAverageRating(title) {
		axios
			.get(`${backend}/gameratings?title=${title}`)
			.then((response) => {
				let rating = 0;
				let reviewsAmount = 0;
				for (const r of response.data) {
					rating += r;
					reviewsAmount++;
				}
				rating /= Math.max(reviewsAmount, 1);
				rating = Math.round(rating * 10) / 10;
				setCurrAvrgRating(rating);
			})
			.catch((error) => {
				setCurrAvrgRating(0);
				console.error(e);
			});
	}

	const InfoBox = () => {
		const dataToSend = {
			username: userData.username,
			password: userData.password,
			title: infoBoxData ? infoBoxData.title : "",
		};

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
									<br />
									<text>Average Rating: {currAvrgRating}</text>
								</div>
								<div id="user-info">
									<button
										id="add-button"
										onClick={() => {
											axios.post(`${backend}/addgametolibrary`, dataToSend);
											axios.post(`${backend}/removegamefromrecommendations`, dataToSend).then(() => {
												fetchLibrary();
												fetchRecommendations();
												setInfoBoxStatus(false);
											});
										}}
									>
										ADICIONAR À BIBLIOTECA
									</button>
									<button
										id="reject-button"
										onClick={() => {
											axios.post(`${backend}/removegamefromrecommendations`, dataToSend).then(() => {
												fetchRecommendations();
												setInfoBoxStatus(false);
											});
										}}
									>
										REJEITAR
									</button>
									<button
										id="blacklist-button"
										onClick={() => {
											axios.post(`${backend}/blacklistgame`, dataToSend);
											axios.post(`${backend}/removegamefromrecommendations`, dataToSend).then(() => {
												fetchRecommendations();
												setInfoBoxStatus(false);
											});
										}}
									>
										NÃO RECOMENDE
									</button>
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
		if (input == "") {
			return;
		}
		setOutput("Aguardando resposta do modelo.");
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
						<div
							id="recommended-card"
							onClick={() => {
								setInfoBoxData({ title: it.title, rating: it.rating, state: it.state, data: it.data });
								getGameAverageRating(it.title);
								setInfoBoxStatus(true);
							}}
						>
							<div id="centered-text">{it.title}</div>
							<img src={it.data.image.original_url} alt={it.title} />
						</div>
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
				<label>Assistente de IA</label>
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
					<img src={sendIcon}></img>
				</button>
				<button onClick={() => {}}>
					<img src={microphoneIcon}></img>
				</button>
			</div>
		</div>
	);
};
