import style from "./Rating.module.css"

export default function Rating({rating = 'unrated', className}){
    return <p className={`${style.Rating} ${className}`}>{rating}</p>
}