"use client"
import Library from "./Library"
import RecommendContainer from "./Recommend"
import Textbox from "./Textbox"
import styles from "./MainPage.module.css"
import { useState, useEffect } from "react"


export default function mainPage(){
    const [ownedGames, setGames] = useState([]);
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
            const gameLibrary = data.game_library;
            const gameArray = Object.keys(gameLibrary).map(key => ({
                id:key,
                ...gameLibrary[key]
            }));
            setGames(gameArray);
        })
        .catch(error => console.error("JSON loading error:", error));
        }, []);

    return (<div className={styles.MainPage}>
        <div className={styles.topSection}>
        <Library ownedGames={ownedGames}/>
        <RecommendContainer ownedGames={ownedGames}/>
        </div>
        <Textbox/>
    </div>
    )
}