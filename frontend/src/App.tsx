import { useState, useEffect } from "react";
import { Login } from "./components/login";
import { Signup } from "./components/signup";
import { Library } from "./components/library";
import { Chat } from "./components/chat";
import { LoginProps } from "./global";

function App() {
	const [userData, setUserData] = useState(null);

	return userData == null ? (
		<InitialScreen userData={userData} setUserData={setUserData} />
	) : (
		<LibraryScreen userData={userData} setUserData={setUserData} />
	);
}

const InitialScreen = ({ userData, setUserData }: LoginProps) => {
	return (
		<div id="initial-screen">
			<Signup />
			<Login userData={userData} setUserData={setUserData} />
		</div>
	);
};

const LibraryScreen = ({ userData, setUserData }: LoginProps) => {
	return (
		<div>
			<Library userData={userData} setUserData={setUserData} />
			<Chat userData={userData} setUserData={setUserData} />
		</div>
	);
};

export default App;
