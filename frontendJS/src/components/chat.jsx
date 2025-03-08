import axios from "axios";
import React, { useEffect, useState, useRef } from "react";
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
									<text>Plataformas: {infoBoxData.data.platforms.map((platform) => platform.name).join(", ")}</text>
									<br />
									<text>Lançamento: {infoBoxData.data.original_release_date}</text>
									<br />
									<text>Avaliação média: {currAvrgRating}</text>
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
		return (
			<div id="recommendations-grid">
				{recommendations
					? recommendations.map((it) => {
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
					  })
					: null}
			</div>
		);
	};

	/* Gravar áudio */
	const [isRecording, setIsRecording] = useState(false);
	const [audioBlob, setAudioBlob] = useState(null);
	const mediaRecorderRef = useRef(null);

	const startRecording = () => {
		navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
			const mediaRecorder = new MediaRecorder(stream);
			mediaRecorderRef.current = mediaRecorder;
			mediaRecorder.start();

			const audioChunks = [];
			mediaRecorder.addEventListener("dataavailable", (event) => {
				audioChunks.push(event.data);
			});

			mediaRecorder.addEventListener("stop", () => {
				const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
				setAudioBlob(audioBlob);
				sendAudio(audioBlob);
			});

			setIsRecording(true);
		});
	};

	const sendAudio = (audioBlob) => {
		const formData = new FormData();
		formData.append("audio", audioBlob, "recording.wav");

		axios
			.post(`${backend}/uploadaudio`, formData, {
				headers: {
					"Content-Type": "multipart/form-data",
				},
			})
			.then((response) => {
				setInput(response.data);
				sendMessage();
			})
			.catch((error) => console.error(error));
	};

	const stopRecording = () => {
		mediaRecorderRef.current.stop();
		setIsRecording(false);
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
				<button
					className={isRecording ? "active" : "inactive"}
					onClick={() => {
						if (isRecording) {
							stopRecording();
						} else {
							startRecording();
						}
					}}
				>
					<img src={microphoneIcon}></img>
				</button>
			</div>
		</div>
	);
};
