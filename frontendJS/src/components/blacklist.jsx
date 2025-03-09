import axios from "axios";
import { backend } from "../global";
import "./../styles/blacklist.css";

export const Blacklist = ({ userData, blacklist, getBlacklist, blacklistStatus, setBlacklistStatus }) => {
	const BlacklistEntry = ({ title }) => {
		return (
			<div>
				<text>{title}</text>
				<button
					onClick={() => {
						axios
							.post(`${backend}/unblacklistgame`, {
								username: userData.username,
								password: userData.password,
								title: title,
							})
							.then((response) => {
								getBlacklist();
							})
							.catch((error) => {
								console.error(error);
							});
					}}
				>
					X
				</button>
			</div>
		);
	};

	return !blacklistStatus ? null : (
		<div id="blacklist-layer">
			<div id="blacklist-box">
				<div id="header">
					<h2>NÃO RECOMENDE</h2>
					<button onClick={() => setBlacklistStatus(false)}>X</button>
				</div>
				<text>Os jogos exibidos aqui não serão recomendados pelo assistente de IA</text>
				<div id="blacklist">
					{blacklist
						? blacklist.map((it) => {
								console.log(it);
								return <BlacklistEntry title={it} />;
						  })
						: null}
				</div>
			</div>
		</div>
	);
};
