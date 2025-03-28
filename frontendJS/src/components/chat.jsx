import axios from "axios";
import React, { useEffect, useState, useRef } from "react";
import { backend } from "../global";
import "../styles/chat.css";

import microphoneIcon from "../assets/microphone.svg";
import sendIcon from "../assets/send-message.svg";

export const Chat = ({ userData, recommendations, setRecommendations, fetchLibrary }) => {
	// Input = Message enviada pelo usuário. Output = mensagem recebida da Gemini
	const [input, setInput] = useState("");
	const [output, setOutput] = useState(
		"Olá, bem vindo à CInJogue! Envie uma mensagem para começar a construir sua biblioteca.",
	);

	// Estado para armazenar os dados do jogo selecionado para exibir na info box
	const [infoBoxData, setInfoBoxData] = useState(null);
	// Estado para controlar a visibilidade da InfoBox
	const [infoBoxStatus, setInfoBoxStatus] = useState(false);
	// Estado para armazenar a média de todas as avaliações do jogo selecionado
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

	// Componente InfoBox para exibir informações detalhadas sobre um jogo
	const InfoBox = () => {
		// Dados a serem enviados nas requisições
		const dataToSend = {
			username: userData.username,
			password: userData.password,
			title: infoBoxData ? infoBoxData.title : "",
		};

		// Retorna null se a InfoBox não estiver visível
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

		setInput("");
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
	// Estado para controlar se a gravação está ativa ou não
	const [isRecording, setIsRecording] = useState(false);
	// Estado para armazenar o blob de áudio gravado
	const [audioBlob, setAudioBlob] = useState(null);
	// Referência para o MediaRecorder
	const mediaRecorderRef = useRef(null);

	// Função para iniciar a gravação de áudio
	const startRecording = () => {
		// Solicita permissão para acessar o microfone do usuário
		navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
			// Cria uma nova instância do MediaRecorder com o stream de áudio
			const mediaRecorder = new MediaRecorder(stream);
			// Armazena a instância do MediaRecorder na referência
			mediaRecorderRef.current = mediaRecorder;
			// Inicia a gravação
			mediaRecorder.start();

			// Array para armazenar os chunks de áudio gravados
			const audioChunks = [];
			// Adiciona um listener para o evento dataavailable, que é disparado quando há dados de áudio disponíveis
			mediaRecorder.addEventListener("dataavailable", (event) => {
				// Adiciona os dados de áudio ao array de chunks
				audioChunks.push(event.data);
			});

			// Adiciona um listener para o evento stop, que é disparado quando a gravação é interrompida
			mediaRecorder.addEventListener("stop", () => {
				// Cria um blob de áudio a partir dos chunks gravados, armazena-o no estado e o envia para o backend
				const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
				setAudioBlob(audioBlob);
				sendAudio(audioBlob);
			});
			setIsRecording(true);
		});
	};

	// Função para enviar o áudio gravado para o backend
	const sendAudio = (audioBlob) => {
		// Cria um FormData para enviar o blob de áudio
		const formData = new FormData();
		formData.append("audio", audioBlob, "recording.wav");

		// Faz uma requisição POST para enviar o áudio para o backend
		axios
			.post(`${backend}/uploadaudio`, formData, {
				headers: {
					"Content-Type": "multipart/form-data",
				},
			})
			.then((response) => {
				// Atualiza o input com a transcrição do áudio recebida do backend
				setInput(response.data);
				// Envia a mensagem transcrita para a IA
				sendMessage();
			})
			.catch((error) => console.error(error));
	};

	// Função para interromper a gravação de áudio
	const stopRecording = () => {
		mediaRecorderRef.current.stop();
		setIsRecording(false);
	};

	// Atualiza a biblioteca e recomendações quando a página carrega
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
				<input
					onKeyDown={(e) => {
						if (e.key == "Enter") {
							sendMessage();
						}
					}}
					onChange={(e) => setInput(e.target.value)}
					value={input}
					placeholder="Digite sua mensagem"
				></input>
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
