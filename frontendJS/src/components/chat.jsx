import axios from "axios";
import React, { useEffect, useState } from "react";
import { backend } from "../global";
import "../styles/chat.css";

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
					<svg
						width="40px"
						height="40px"
						viewBox="0 0 24 24"
						fill="none"
						xmlns="http://www.w3.org/2000/svg"
						stroke="#ffffff"
					>
						<g id="SVGRepo_bgCarrier" stroke-width="0" />
						<g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round" />
						<g id="SVGRepo_iconCarrier">
							<path
								fill-rule="evenodd"
								clip-rule="evenodd"
								d="M3.3938 2.20468C3.70395 1.96828 4.12324 1.93374 4.4679 2.1162L21.4679 11.1162C21.7953 11.2895 22 11.6296 22 12C22 12.3704 21.7953 12.7105 21.4679 12.8838L4.4679 21.8838C4.12324 22.0662 3.70395 22.0317 3.3938 21.7953C3.08365 21.5589 2.93922 21.1637 3.02382 20.7831L4.97561 12L3.02382 3.21692C2.93922 2.83623 3.08365 2.44109 3.3938 2.20468ZM6.80218 13L5.44596 19.103L16.9739 13H6.80218ZM16.9739 11H6.80218L5.44596 4.89699L16.9739 11Z"
								fill="#ffffff"
							/>
						</g>
					</svg>
				</button>
				<button onClick={() => {}}>
					<svg
						width="40px"
						height="40px"
						viewBox="0 0 24 24"
						fill="none"
						xmlns="http://www.w3.org/2000/svg"
						stroke="#ffffff"
					>
						<g id="SVGRepo_bgCarrier" stroke-width="0" />
						<g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round" />
						<g id="SVGRepo_iconCarrier">
							<rect
								x="9"
								y="3"
								width="6"
								height="11"
								rx="3"
								stroke="#ffffff"
								stroke-width="2"
								stroke-linejoin="round"
							/>
							<path
								d="M5 11C5 12.8565 5.7375 14.637 7.05025 15.9497C8.36301 17.2625 10.1435 18 12 18C13.8565 18 15.637 17.2625 16.9497 15.9497C18.2625 14.637 19 12.8565 19 11"
								stroke="#ffffff"
								stroke-width="2"
								stroke-linecap="round"
								stroke-linejoin="round"
							/>
							<path d="M12 21V19" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />{" "}
						</g>
					</svg>
				</button>
			</div>
		</div>
	);
};
