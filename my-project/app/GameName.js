import style from "./GameName.module.css"
export default function GameName({name, className}){
    return <div className={`${style.GameName} ${className}`}>{name}</div>
}