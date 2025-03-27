import { useState } from "react";

export const Social = ({ userData, socialStatus, setSocialStatus }) => {
	const [searchedUser, setSearchedUser] = useState(userData.username);
	const [visualizedLibrary, setVisualizedLibrary] = useState([]);

	function fetchLibrary() {
		axios
			.get(`${backend}/getlibrary?username=${searchedUser}`)
			.then((response) => {
				setVisualizedLibrary(response.data);
				console.log(response.data);
			})
			.catch((e) => {
				console.error(e);
				setVisualizedLibrary([]);
			});
	}

	return (
		<div id="social-layer">
			<div id="social-box">
				<p></p>
			</div>
		</div>
	);
};
