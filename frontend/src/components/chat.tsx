import axios from "axios";
import React, { useEffect, useState } from "react";
import { backend, LoginProps } from "../global";

export const Chat = ({ userData, setUserData }: LoginProps) => {
	const [input, setInput] = useState("");
	const [output, setOutput] = useState("");

	const sendMessage = () => {
		axios
			.post(`${backend}/genai`, {
				prompt: input,
				username: userData.username,
				password: userData.password,
			})
			.then((response) => {
				setOutput(`${response.data[0].message}`);
			})
			.catch((error) => console.error(error));
	};
	return (
		<div>
			<textarea value={output}></textarea>
			<br></br>
			<input onChange={(e) => setInput(e.target.value)} value={input}></input>
			<button onClick={sendMessage}>SEND</button>
		</div>
	);
};
