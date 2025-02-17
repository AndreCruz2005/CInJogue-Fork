"use client"
import { useEffect, useState, useRef } from "react"
import styles from "./Textbox.module.css"
import { IoMdSend } from "react-icons/io";
export default function Textbox(){

    const divRef = useRef(null);

    const [placeholderVisible, setPlaceholderVisible] = useState(true);

    const [message, setMessage] = useState("");


    useEffect(() => 
    {
        const div = divRef.current
        const handleInput = () =>
        {
            const text = div.textContent || ""; 
            setMessage(text);
            setPlaceholderVisible(text === "");
        }
        const handleKeyDown = (event) => {
            if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                handleSubmit();
            }
        };
        div.addEventListener("keydown", handleKeyDown);
        div.addEventListener("input", handleInput);
        return () =>
        {
            div.removeEventListener("input", handleInput);
            div.removeEventListener("keydown", handleKeyDown);
        }
    }, [message])

    const handleSubmit = async () => 
    {
        if (message.trim() === "") return;
        const sentmessage = message;
        divRef.current.textContent = "";
        setMessage("");
        setPlaceholderVisible(true);
        try 
        {
            const response = await fetch("http://localhost:5000/submit-message", {
            method: "POST",
            headers: 
            {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({message}),
            });
           /* if (response.ok)
                {
                console.log("Mensagem enviada com sucesso");
                } 
            else
                {
                console.error("Falha ao enviar mensagem");
                divRef.current.textContent = sentmessage;
                setMessage(sentmessage);
                setPlaceholderVisible(false);
                }*/
            }
            catch (error) {
                console.error("Erro ao enviar:", error);
                divRef.current.textContent = sentmessage;
                setMessage(sentmessage);
                setPlaceholderVisible(false);
            }
        };

    return(
    <div className={styles.TextboxContainer}>
    <div contentEditable ="true" 
    className = {`${styles.Textbox} ${placeholderVisible ? styles.placeholderVisible : ""} `}
    ref={divRef}
    data-placeholder="Digite um comando para a IA fazer">
    </div>
    <button onClick={handleSubmit} className={styles.submitButton}>
    <IoMdSend className={styles.buttonIcon}/>
    </button>
    </div>
    )
}