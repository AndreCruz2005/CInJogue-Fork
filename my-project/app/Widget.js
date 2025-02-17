import GameImg from "./GameImg"
import GameName from "./GameName"
import Rating from "./Rating"

import style from "./Widget.module.css"


export default function Widget({name, rating}){
    const path = `/game/${name}.png`;
    return <div className = {style.Widget}>
    <GameImg image_path={path} className={style.GameImg}></GameImg>
    <GameName name={name} className={style.GameName}></GameName>
    <Rating rating={rating} className={style.Rating}></Rating>
    </div>
}