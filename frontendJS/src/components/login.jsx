import axios from "axios";
import { useState } from "react";
import { backend } from "../global";
import React from "react";
import "./../styles/login.css";

export const Login = ({ userData, setUserData }) => {
	const [name, setName] = useState("");
	const [password, setPassword] = useState("");

	const handleSubmit = () => {
		login(name, password, setUserData);
	};

	return (
		<div id="login">
			<h1>LOGIN</h1>
			<label>
				Username:
				<input type="username" value={name} onChange={(e) => setName(e.target.value)}></input>
			</label>
			<label>
				Password:
				<input type="password" value={password} onChange={(e) => setPassword(e.target.value)}></input>
			</label>
			<button onClick={handleSubmit}>SUBMIT</button>
		</div>
	);
};

function login(username, password, setUserData) {
	axios
		.post(`${backend}/login`, {
			username,
			password,
		})
		.then((response) => {
			response.data.password = password;
			setUserData("error" in response.data ? null : response.data);
		})
		.catch((error) => {
			console.error("There was an error signing up!", error);
			setUserData(null);
		});
}
