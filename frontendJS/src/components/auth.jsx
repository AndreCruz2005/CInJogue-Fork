import axios from "axios";
import React, { useState } from "react";
import { backend } from "../global";
import "./../styles/auth.css";

// Backgrounds
import terrariaBG from "./../assets/background/terraria-bg.jpeg";
import hollowKnightBG from "./../assets/background/hollowknight-bg.jpg";
import skyrimBG from "./../assets/background/skyrim-bg.jpg";
import nomansSkyBG from "./../assets/background/nomanssky-bg.jpg";
import outerworldsBG from "./../assets/background/outerworlds-bg.jpg";
import baldursgateBG from "./../assets/background/baldursgate-bg.jpg";
import falloutBG from "./../assets/background/fallout-bg.jpg";
import outerwildsBG from "./../assets/background/outerwilds-bg.png";
import spidermanBG from "./../assets/background/spiderman-bg.jpg";
import rainworldBG from "./../assets/background/rainworld-bg.png";
import rdr2BG from "./../assets/background/rdr2-bg.jpg";
import subnauticaBG from "./../assets/background/subnautica-bg.jpg";
export const Auth = ({ userData, setUserData }) => {
	const [loginMode, setLoginMode] = useState(true);
	const [errorMessage, setErrorMessage] = useState("");
	const background = [
		terrariaBG,
		rainworldBG,
		hollowKnightBG,
		skyrimBG,
		nomansSkyBG,
		outerworldsBG,
		baldursgateBG,
		falloutBG,
		outerwildsBG,
		spidermanBG,
		rdr2BG,
		subnauticaBG,
	][Date.now() % 12];

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
					setErrorMessage("Um erro ocorreu. Cheque se seus dados estão corretos e a sua conexão.");
					setUserData(null);
				});
		}

		return (
			<div id="login">
				<h1>ENTRE NA SUA CONTA</h1>
				<p id="error-message">{errorMessage}</p>
				<label>
					Usuário:
					<input type="username" value={username} onChange={(e) => setUsername(e.target.value)}></input>
				</label>
				<label>
					Senha:
					<input type="password" value={password} onChange={(e) => setPassword(e.target.value)}></input>
				</label>
				<button onClick={login}>ENTRAR</button>
				<a
					onClick={() => {
						setErrorMessage("");
						setLoginMode(false);
					}}
				>
					{"Não possui conta? Clique aqui para criar uma"}
				</a>
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
			if (!username || !password || !passwordConfirm || !email || !birthdate) {
				setErrorMessage("Preencha todos os campos.");
				return;
			}

			if (password != passwordConfirm) {
				setErrorMessage("As senhas são diferentes.");
				return;
			}

			if (password.length < 8) {
				setErrorMessage("A senha deve ter pelo menos 8 caracteres.");
				return;
			}

			if (email.split("").filter((i) => i == "@").length != 1) {
				setErrorMessage("Endereço de email inválido.");
				return;
			}

			if (Number(birthdate.split("-").length[0]) >= 2012) {
				setErrorMessage("Você deve ter mais de 12 anos para criar uma conta.");
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
					setErrorMessage("");
				})
				.catch((error) => {
					console.error("There was an error signing up!", error);
					setErrorMessage("Seu nome e email já foi usado ou você não está conectado.");
				});
		}

		return (
			<div id="signup">
				<h1>CRIE SUA CONTA</h1>
				<p id="error-message">{errorMessage}</p>
				<label>
					Usuário:
					<input type="username" value={username} onChange={(e) => setUsername(e.target.value)} />
				</label>
				<label>
					Senha:
					<input type="password" value={password} minLength={8} onChange={(e) => setPassword(e.target.value)} />
				</label>
				<label>
					Confirme Senha:
					<input
						type="password"
						value={passwordConfirm}
						minLength={8}
						onChange={(e) => setPasswordConfirm(e.target.value)}
					/>
				</label>
				<label>
					Email:
					<input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
				</label>
				<label>
					Data de nascimento:
					<input type="date" value={birthdate} max="2012-01-01" onChange={(e) => setBirthdate(e.target.value)} />
				</label>
				<button onClick={signUp}>CRIAR CONTA</button>
				<a
					onClick={() => {
						setErrorMessage("");
						setLoginMode(true);
					}}
				>
					{"Já possui conta? Clique aqui para entrar"}
				</a>
			</div>
		);
	};

	return (
		<div id="auth">
			<img id="background-image" src={background}></img>
			{loginMode ? <Login /> : <SignUp />}
			<div id="description">
				<h1 id="website-title">CInJogue</h1>
				<p id="website-subtitle">
					Descubra, catalogue e explore o universo dos jogos como nunca antes. Com inteligência artificial de ponta,
					transformamos sua coleção de games em uma experiência personalizada de descoberta. Recomendações sob medida,
					análises inteligentes e um acervo totalmente seu - tudo em um único lugar épico. Sua jornada gamer nunca mais
					vai ser a mesma!{" "}
				</p>
			</div>
		</div>
	);
};
