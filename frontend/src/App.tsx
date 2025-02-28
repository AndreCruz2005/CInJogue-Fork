import { useState, useEffect } from "react";
import { Login } from "./components/login";
import { Signup } from "./components/signup";
import { Library } from "./components/library";
import { Chat } from "./components/chat";
import { backend, LoginProps } from "./global";
import axios from "axios";

function App() {
	const [userData, setUserData] = useState(null);
	const [library, setLibrary] = useState(null);

	return userData == null ? (
		<InitialScreen userData={userData} setUserData={setUserData} />
	) : (
		<LibraryScreen userData={userData} setUserData={setUserData} library={library} setLibrary={setLibrary} />
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

const LibraryScreen = ({ userData, setUserData, library, setLibrary }: any) => {
	return (
		<div>
			<Library userData={userData} setUserData={setUserData} library={library} setLibrary={setLibrary} />
			<Chat userData={userData} setUserData={setUserData} library={library} setLibrary={setLibrary} />
		</div>
	);
};

export default App;
