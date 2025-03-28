import React, { useEffect, useRef, useState } from "react";
import { backend } from "../global";
import axios from "axios";
import "../styles/library.css";

export const Library = ({ userData, library, fetchLibrary }) => {
	const [filter, setFilter] = useState(" ");
	const states = ["NÃO JOGADO", "JOGADO", "AINDA JOGANDO", "CONCLUÍDO", "ABANDONADO", "LISTA DE DESEJOS"];

	// Referência à grid de id='library'
	const libraryRef = useRef(null);
	// Conta o número de jogos na biblioteca
	// sob o atual filtro mostrando o número de componentes filhos de #library
	const [gameCount, setGameCount] = useState(0);

	// Estado para armazenar os dados do jogo selecionado para exibir na info box
	const [infoBoxData, setInfoBoxData] = useState(null);
	// Estado para controlar a visibilidade da InfoBox
	const [infoBoxStatus, setInfoBoxStatus] = useState(false);
	// Estado para armazenar a média de todas as avaliações do jogo selecionado
	const [currAvrgRating, setCurrAvrgRating] = useState(0);

	function changeGameRating(title, rating) {
		axios
			.post(`${backend}/updaterating`, {
				username: userData.username,
				password: userData.password,
				title: title,
				rating: rating,
			})
			.then(() => {
				fetchLibrary();
				setInfoBoxData({ ...infoBoxData, rating: rating });
			})
			.catch((e) => console.error(e));
	}

	function changeGameState(title, state) {
		axios
			.post(`${backend}/updatestate`, {
				username: userData.username,
				password: userData.password,
				title: title,
				state: state,
			})
			.then(() => {
				fetchLibrary();
				setInfoBoxData({ ...infoBoxData, state: state });
			})
			.catch((e) => console.error(e));
	}

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
				console.error(error);
			});
	}

	// Componente que representa a InfoBox, que exibe informações detalhadas sobre o jogo selecionado
	const InfoBox = () => {
		// Se a InfoBox não estiver visível, retorna null
		return !infoBoxStatus ? null : (
			<div id="info-box-layer">
				<div id="info-box">
					<div id="header">
						{/* Título do jogo e botão para fechar a InfoBox */}
						<text id="title">{infoBoxData.title}</text>
						<button id="close-button" onClick={() => setInfoBoxStatus(false)}>
							X
						</button>
					</div>
					<div id="content">
						<div id="image-container">
							{/* Imagem do jogo */}
							<img src={infoBoxData.data.image.original_url} alt={infoBoxData.title} />
						</div>
						<div id="description-info-container">
							{/* Descrição do jogo */}
							<textarea id="description" readOnly value={infoBoxData.data.deck}></textarea>
							<div id="other-info">
								<div id="game-info">
									{/* Informações adicionais sobre o jogo */}
									<text>Plataformas: {infoBoxData.data.platforms.map((platform) => platform.name).join(", ")}</text>
									<br />
									<text>Lançamento: {infoBoxData.data.original_release_date}</text>
									<br />
									<text>Avaliação média: {currAvrgRating}</text>
								</div>
								<div id="user-info">
									{/* Avaliação do usuário */}
									<div id="rating">
										<label>AVALIAÇÃO</label>
										<select
											value={infoBoxData.rating}
											onChange={(e) => {
												changeGameRating(infoBoxData.title, e.target.value);
											}}
										>
											{[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((it) => (
												<option key={it} value={it}>
													{it}
												</option>
											))}
										</select>
									</div>
									{/* Estado do jogo */}
									<div id="state">
										<label>STATUS</label>
										<select
											value={infoBoxData.state}
											onChange={(e) => {
												changeGameState(infoBoxData.title, e.target.value);
											}}
										>
											{states.map((state) => (
												<option key={state} value={state}>
													{state}
												</option>
											))}
										</select>
									</div>
									{/* Botão para remover o jogo da biblioteca */}
									<button
										id="remove-button"
										onClick={() => {
											axios
												.post(`${backend}/removegamefromlibrary`, {
													username: userData.username,
													password: userData.password,
													title: infoBoxData.title,
												})
												.then(() => {
													fetchLibrary();
													setInfoBoxStatus(false);
												})
												.catch((e) => console.error(e));
										}}
									>
										REMOVER
									</button>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		);
	};

	// Componente que representa um cartão de jogo na biblioteca
	const GameCard = ({ title, rating, state, data }) => {
		// Verifica se o cartão deve ser visível com base no filtro atual
		const isVisible = filter == state || filter == " ";
		return isVisible ? (
			<div
				id="game-card"
				// Quando o card é clicado, seleciona o jogo para ser exibido na infobox
				onClick={() => {
					// Define os dados do jogo selecionado na InfoBox
					setInfoBoxData({ title: title, rating: rating, state: state, data: data });
					// Obtém a avaliação média do jogo
					getGameAverageRating(title);
					// Exibe a InfoBox
					setInfoBoxStatus(true);
				}}
			>
				<div id="centered-text">{title}</div> {/* Texto exibido sobre o card */}
				<img src={data.image.original_url} alt={title} />
			</div>
		) : null;
	};

	// Atualiza a contagem de jogos sempre que o filtro ou a biblioteca sofrem alterações
	useEffect(() => {
		if (libraryRef.current) {
			setGameCount(libraryRef.current.children.length);
		}
	}, [filter, library]);

	return (
		<div id="library-container">
			<InfoBox />
			<div id="header">
				<div id="filter-buttons">
					{
						// Cria os botões de filtro, quando um botão é clicado o hook filter é atualizado
						// para o filtro selecionado a não ser que aquele filtro já tivesse sido selecionado,
						// nesse caso o filtro é resetado para " ".
						states.map((it) => {
							return (
								<button
									className={filter == it ? "active-filter" : "inactive-filter"}
									onClick={() => {
										setFilter(filter == it ? " " : it);
									}}
								>
									{it}
								</button>
							);
						})
					}
				</div>
				<text id="counter">
					{gameCount} {gameCount == 1 ? "JOGO" : "JOGOS"}
				</text>
			</div>
			<div id="library" ref={libraryRef}>
				{library
					? library.map((it) => {
							return <GameCard title={it.title} rating={it.rating} state={it.state} data={it.data} />;
					  })
					: null}
			</div>
		</div>
	);
};
