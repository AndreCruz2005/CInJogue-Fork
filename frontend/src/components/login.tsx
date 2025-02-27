import axios from "axios";
import { useState } from "react";
import { backend, LoginProps } from "../global";

export const Login = ({ userData, setUserData }: LoginProps) => {
	const [name, setName] = useState("");
	const [password, setPassword] = useState("");

	const handleSubmit = () => {
		login(name, password, setUserData);
	};

	return (
		<div>
			<h1>LOGIN</h1>
			<label>
				Username
				<input type="text" value={name} onChange={(e) => setName(e.target.value)}></input>
			</label>
			<br />
			<label>
				Password
				<input type="password" value={password} onChange={(e) => setPassword(e.target.value)}></input>
			</label>
			<br />
			<button onClick={handleSubmit}>SUBMIT</button>
			<br />
			<h1>LOGGED IN USER: {userData && "username" in userData ? userData["username"] : "NOT LOGGED IN"}</h1>
			<button
				onClick={() => {
					axios
						.post(`${backend}/logout`)
						.then(() => setUserData(null))
						.catch((error) => {
							error.log(error);
						});
				}}
			>
				LOG OUT
			</button>
		</div>
	);
};

function login(username: string, password: string, setUserData: (data: any) => void): void {
	axios
		.post(`${backend}/login`, {
			username,
			password,
		})
		.then((response) => {
			response.data.password = password;
			setUserData(response.data);
		})
		.catch((error) => {
			console.error("There was an error signing up!", error);
			setUserData(null);
		});
}
