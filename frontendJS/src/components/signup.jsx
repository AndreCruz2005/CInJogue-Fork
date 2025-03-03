import axios from "axios";
import { useState } from "react";
import { backend } from "../global";
import "../styles/signup.css";

export const Signup = () => {
	const [username, setUsername] = useState("");
	const [password, setPassword] = useState("");
	const [passwordConfirm, setPasswordConfirm] = useState("");
	const [email, setEmail] = useState("");
	const [birthdate, setBirthdate] = useState("");

	const handleSubmit = () => {
		SignUp(username, password, passwordConfirm, email, birthdate);
	};

	return (
		<div id="signup">
			<h1>SIGN UP</h1>
			<label>
				Username:
				<input type="username" value={username} onChange={(e) => setUsername(e.target.value)} />
			</label>
			<br />
			<label>
				Password:
				<input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
			</label>
			<br />
			<label>
				Confirm Password:
				<input type="password" value={passwordConfirm} onChange={(e) => setPasswordConfirm(e.target.value)} />
			</label>
			<br />
			<label>
				Email:
				<input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
			</label>
			<br />
			<label>
				Birthdate:
				<input type="date" value={birthdate} onChange={(e) => setBirthdate(e.target.value)} />
			</label>
			<br />
			<button onClick={handleSubmit}>SUBMIT</button>
		</div>
	);
};

function SignUp(username, password, passwordConfirm, email, birthdate) {
	if (password != passwordConfirm) console.error("Passwords do not match!");

	axios
		.post(`${backend}/signup`, {
			username,
			password,
			email,
			birthdate,
		})
		.then((response) => {
			console.log(response.data);
		})
		.catch((error) => {
			console.error("There was an error signing up!", error);
		});
}
