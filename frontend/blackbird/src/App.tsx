
import Login from "./components/Login.tsx";

import './App.css';

function App() {

	const handleLogin = async (username: string, password: string) => {
        const response = await fetch(`/api/admin/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            credentials: "include",
            body: JSON.stringify({ username, password }),
        });

        if (!response.ok) {
            throw new Error("Invalid username or password");
        }
	};
	return (
		<div className="login-container">
			<Login onLogin={handleLogin} />
		</div>
	)
}

export default App;
