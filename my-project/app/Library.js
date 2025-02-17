"use client";
import Widget from "./Widget"
import styles from "./LibraryContainer.module.css"

export default function LibraryContainer({ownedGames}){
    


return (
    <div className= {styles.LibraryContainer}>
        {ownedGames.map ((game) => (
        <Widget key = {game.id} name = {game.id} rating={game.rating}></Widget>
        ))}
    </div>
)
}