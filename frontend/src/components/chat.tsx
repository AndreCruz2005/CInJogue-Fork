import axios from "axios";
import React, { useEffect, useState } from "react";
import { backend } from "../global";

export const Chat = ({ userData, setUserData, library, setLibrary }: any) => {
	const [input, setInput] = useState("");
	const [output, setOutput] = useState("");

	function fetchLibrary() {
		axios
			.post(`${backend}/getlibrary`, {
				username: userData.username,
				password: userData.password,
			})
			.then((response) => {
				setLibrary(response.data);
				console.log(response.data);
			})
			.catch((e) => console.error(e));
	}

	const sendMessage = () => {
		axios
			.post(`${backend}/genai`, {
				prompt: input,
				username: userData.username,
				password: userData.password,
			})
			.then((response) => {
				setOutput(`${response.data[0].message}`);
				fetchLibrary();
			})
			.catch((error) => console.error(error));
	};

	useEffect(() => {
		fetchLibrary();
    }, []);
	return (
		<div>
			<textarea value={output}></textarea>
			<br></br>
			<input onChange={(e) => setInput(e.target.value)} value={input}></input>
			<button onClick={() => {sendMessage();}}>SEND</button>
		</div>
	);
};
