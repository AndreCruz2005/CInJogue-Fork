import axios from "axios";
import React, { useEffect, useRef, useState } from "react";
import { backend } from "../global";
import "../styles/library.css";

export const Library = ({ userData, setUserData, library, setLibrary }) => {
	const [filter, setFilter] = useState(" ");
	const [gameCount, setGameCount] = useState(0);
	const libraryRef = useRef(null);
	const filters = ["UNPLAYED", "PLAYED", "PLAYING", "COMPLETED", "ABANDONED", "WISHLISTED"];

	const [infoBoxData, setInfoBoxData] = useState(null);
	const [infoBoxStatus, setInfoBoxStatus] = useState(false);

	const InfoBox = () => {
		return (
			!infoBoxStatus ? (
				null
			) : (
			<div id="info-box-layer">
				<div id="info-box">
					<div id="info-box-content">
						<img src={infoBoxData.data.image.original_url} alt={infoBoxData.title} />
						<div id="info-box-text">
							<text id="info-box-title">{infoBoxData.title}</text>
							<text id="info-box-rating">{infoBoxData.rating}</text>
							<text id="info-box-state">{infoBoxData.state}</text>
						</div>
					</div>
					<button id="info-box-close" onClick={() => setInfoBoxStatus(false)}>X</button>
				</div>
			</div>	
		));
	}

	const GameCard = ({title, rating, state, data}) => {
		const isVisible = filter == state || filter == " ";
		return isVisible ? <img src={data.image.original_url} alt={title} onClick={ () => {
			setInfoBoxData({ title: title, rating: rating, state: state, data: data });
			setInfoBoxStatus(true);
		}}/> : null;
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
		<div id='library-container'>
			<InfoBox />
			<div id="header">
				<div id="filter-buttons">
					{filters.map((it) => {
						return <button className={filter == it ? 'active-filter' : 'inactive-filter'} onClick={() => {setFilter(filter == it ? " " : it)}}>{it}</button>;
					})}
				</div>
				<text id="counter">{gameCount} GAMES</text>
			</div>
			<div id="library" ref={libraryRef}>
				{lst.map((it) => {
					return <GameCard title={it.title} rating={it.rating} state={it.state} data={it.data} />;
				})}
			</div>
		</div>
	);
};
