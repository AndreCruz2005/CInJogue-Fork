import axios from "axios";
import React, { useState } from "react";
import { backend } from "../global";
import "./../styles/auth.css";

export const Auth = ({ userData, setUserData }) => {
	const [loginMode, setLoginMode] = useState(true);

	const Login = () => {
		const [username, setUsername] = useState("");
		const [password, setPassword] = useState("");

		function login() {
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

		return (
			<div id="login">
				<h1>ENTRE NA SUA CONTA</h1>
				<label>
					Usuário:
					<input type="username" value={username} onChange={(e) => setUsername(e.target.value)}></input>
				</label>
				<label>
					Senha:
					<input type="password" value={password} onChange={(e) => setPassword(e.target.value)}></input>
				</label>
				<button onClick={login}>ENTRAR</button>
				<a onClick={() => setLoginMode(false)}>{"Não possui conta? Clique aqui para criar uma"}</a>
			</div>
		);
	};

	const SignUp = () => {
		const [username, setUsername] = useState("");
		const [password, setPassword] = useState("");
		const [passwordConfirm, setPasswordConfirm] = useState("");
		const [email, setEmail] = useState("");
		const [birthdate, setBirthdate] = useState("");

		function signUp() {
			if (password != passwordConfirm) {
				console.error("Passwords do not match!");
				return;
			}

			axios
				.post(`${backend}/signup`, {
					username,
					password,
					email,
					birthdate,
				})
				.then((response) => {
					console.log(response.data);
					setLoginMode(true);
				})
				.catch((error) => {
					console.error("There was an error signing up!", error);
				});
		}

		return (
			<div id="signup">
				<h1>CRIE SUA CONTA</h1>
				<label>
					Usuário:
					<input type="username" value={username} onChange={(e) => setUsername(e.target.value)} />
				</label>
				<label>
					Senha:
					<input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
				</label>
				<label>
					Confirme Senha:
					<input type="password" value={passwordConfirm} onChange={(e) => setPasswordConfirm(e.target.value)} />
				</label>
				<label>
					Email:
					<input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
				</label>
				<label>
					Data de nascimento:
					<input type="date" value={birthdate} onChange={(e) => setBirthdate(e.target.value)} />
				</label>
				<button onClick={signUp}>CRIAR CONTA</button>
				<a onClick={() => setLoginMode(true)}>{"Já possui conta? Clique aqui para entrar"}</a>
			</div>
		);
	};

	return (
		<div id="auth">
			<h1 id="website-title">CInJogue</h1>
			{loginMode ? <Login /> : <SignUp />}
		</div>
	);
};
