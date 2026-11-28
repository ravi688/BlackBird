import { useOutletContext } from 'react-router-dom';

interface OutletContext {
	authenticated: boolean;
	username: string;
}


export default function DashboardPage() {
	const { authenticated, username } = useOutletContext<OutletContext>();
	return (
		<div>
			<h1> This is Dashboard</h1>
			<p>Logged in as: {username}</p>
		</div>
	);
}
