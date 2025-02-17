"use client";
import Widget from "./Widget";
import { useState, useEffect } from "react";
import styles from "./Recommend.module.css"

export default function Recommend({ownedGames}){

    const [newRecommendations, setGames] = useState([]);
    useEffect(() => {
        fetch('http://localhost:5000/send-library',{
            method : 'GET',
            headers: 
            {
                "Content-Type": "application/json",
            },
        })
        .then(response => response.json())
        .then(data => {
            const gameRecommendations = data.game_recommendations;
            const highPriority = gameRecommendations["High Priority"]
            const recommended = Object.keys(highPriority).map(key => ({
                id:key
            }));
            const newRecommendations = recommended.filter(game => !ownedGames.includes(game));

            setGames(newRecommendations);
        })
        .catch(error => console.error("JSON loading error:", error));
        }, []);


return (
    <div className= {styles.Recommend}>
        {newRecommendations.map ((game) => (
        <Widget key = {game.id} name = {game.id}></Widget>  
        ))}
    </div>
)
}