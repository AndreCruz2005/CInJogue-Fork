import { useState, useEffect } from "react";
import { Login } from "./components/login";
import { Signup } from "./components/signup";
import axios from "axios";

const backend: string = "http://192.168.15.6:5000";

function App() {
	return (
		<div>
			<div>
				<Signup />
				<Login />
				<br></br>
			</div>
		</div>
	);
}

export default App;
