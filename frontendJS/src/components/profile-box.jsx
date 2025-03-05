import axios from "axios";
import { useState } from "react";
import { backend } from "../global";
import "./../styles/profile-box.css";

export const ProfileBox = ({ userData, setUserData, profileBoxStatus, setProfileBoxStatus }) => {
	const [oldPassword, setOldPassword] = useState("");
	const [newPassword, setNewPassword] = useState("");
	const [passwordConfirm, setPasswordConfirm] = useState("");
	const [deletePassword, setDeletePassword] = useState("");

	function changePassword() {
		axios
			.post(`${backend}/changepassword`, {
				username: userData.username,
				oldPassword: oldPassword,
				newPassword: newPassword,
			})
			.then((response) => {
				if (response.status === 200) {
					setUserData({ ...userData, password: newPassword });
				}
			})
			.catch((error) => {
				console.error(error);
			});
	}

	function deleteAccount() {
		axios
			.post(`${backend}/removeuser`, {
				username: userData.username,
				password: deletePassword,
			})
			.then((response) => {
				if (response.status === 200) {
					setProfileBoxStatus(false);
					setUserData(null);
				}
			})
			.catch((error) => {
				console.error(error);
			});
	}

	return !profileBoxStatus ? null : (
		<div id="profile-box-layer">
			<div id="profile-box">
				<div id="header">
					<h2>CONFIGURAÇÕES DE CONTA</h2>
					<button onClick={() => setProfileBoxStatus(false)}>X</button>
				</div>
				<div id="options">
					<h3>SEUS DADOS</h3>
					<p>Nome de usuário: {userData.username}</p>
					<p>Email: {userData.email}</p>
					<p>Data de nascimento: {userData.birthdate}</p>
					<p>ID: {userData.id}</p>

					<h3>MUDE SUA SENHA</h3>
					<label>
						Senha atual:
						<input onChange={(e) => setOldPassword(e.target.value)} type="password"></input>
					</label>
					<label>
						Nova senha:
						<input onChange={(e) => setNewPassword(e.target.value)} type="password"></input>
					</label>
					<label>
						Confirme nova senha:
						<input onChange={(e) => setPasswordConfirm(e.target.value)} type="password"></input>
					</label>
					<button
						onClick={() => {
							if (passwordConfirm == newPassword) changePassword();
						}}
					>
						Mudar senha
					</button>

					<h3>DANGER ZONE</h3>
					<label>
						Senha:
						<input onChange={(e) => setDeletePassword(e.target.value)} type="password"></input>
					</label>
					<button onClick={deleteAccount}>Deletar conta</button>
				</div>
			</div>
		</div>
	);
};
