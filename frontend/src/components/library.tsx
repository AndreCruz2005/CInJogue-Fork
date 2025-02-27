import axios from "axios";
import React, { useState } from "react";
import { backend, LoginProps } from "../global";

export const Library = ({ userData, setUserData }: LoginProps) => {
	const [library, setLibrary] = useState("");

	function fetchLibrary() {
		axios
			.post(`${backend}/getlibrary`, {
				username: userData.username,
				password: userData.password,
			})
			.then((response) => {
				setLibrary(`${response.data}`);
				console.log(response.data);
			})
			.catch((e) => console.error(e));
	}

	return (
		<div>
			<textarea value={library}></textarea>
			<br></br>
			<button onClick={fetchLibrary}>GET LIBRARY</button>
		</div>
	);
};
