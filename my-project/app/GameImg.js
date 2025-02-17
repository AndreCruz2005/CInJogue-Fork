import styles from "./GameImg.module.css"
export default function GameImg({image_path, className}){
    return<img className={`${styles.GameImg} ${className}`} src={image_path}/>
}