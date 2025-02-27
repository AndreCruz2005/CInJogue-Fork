import { useState, useEffect } from "react";
import axios from "axios";
import { Login } from "./components/login";
import { Signup } from "./components/signup";
import { Library } from "./components/library";
import { Chat } from "./components/chat";

function App() {
	const [userData, setUserData] = useState(null);

	return (
		<div>
			<div>
				<Signup />
				<Login userData={userData} setUserData={setUserData} />
				<br></br>
				<Library userData={userData} setUserData={setUserData} />
				<br></br>
				<Chat userData={userData} setUserData={setUserData} />
			</div>
		</div>
	);
}

export default App;
