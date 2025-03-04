import React, { useEffect, useRef, useState } from "react";
import { backend } from "../global";
import axios from "axios";
import "../styles/library.css";

export const Library = ({ userData, setUserData, library, setLibrary }) => {
	const [filter, setFilter] = useState(" ");
	const [gameCount, setGameCount] = useState(0);
	const libraryRef = useRef(null);
	const states = ["UNPLAYED", "PLAYED", "PLAYING", "COMPLETED", "ABANDONED", "WISHLISTED"];

	const [infoBoxData, setInfoBoxData] = useState(null);
	const [infoBoxStatus, setInfoBoxStatus] = useState(false);
	const [currAvrgRating, setCurrAvrgRating] = useState(0);

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
				console.error(e);
			});
	}

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
									<br />
									<text>Average Rating: {currAvrgRating}</text>
								</div>
								<div id="user-info">
									<div id="rating">
										<label>RATING</label>
										<select
											value={infoBoxData.rating}
											onChange={(e) => changeGameRating(infoBoxData.title, e.target.value)}
										>
											{[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((it) => (
												<option key={it} value={it}>
													{it}
												</option>
											))}
										</select>
									</div>
									<div id="state">
										<label>STATE</label>
										<select
											value={infoBoxData.state}
											onChange={(e) => changeGameState(infoBoxData.title, e.target.value)}
										>
											{states.map((state) => (
												<option key={state} value={state}>
													{state}
												</option>
											))}
										</select>
									</div>
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
										REMOVE
									</button>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		);
	};

	const GameCard = ({ title, rating, state, data }) => {
		const isVisible = filter == state || filter == " ";
		return isVisible ? (
			<img
				src={data.image.original_url}
				alt={title}
				onClick={() => {
					setInfoBoxData({ title: title, rating: rating, state: state, data: data });
					getGameAverageRating(title);
					setInfoBoxStatus(true);
				}}
			/>
		) : null;
	};

	let lst = [];
	Object.entries(library ? library : {}).forEach((item) =>
		lst.push({ title: item[0], rating: item[1].rating, state: item[1].state, data: item[1].data }),
	);

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
					{states.map((it) => {
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
					})}
				</div>
				<text id="counter">
					{gameCount} {gameCount > 1 ? "JOGOS" : "JOGO"}
				</text>
			</div>
			<div id="library" ref={libraryRef}>
				{lst.map((it) => {
					return <GameCard title={it.title} rating={it.rating} state={it.state} data={it.data} />;
				})}
			</div>
		</div>
	);
};
