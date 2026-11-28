
import React, { useEffect, useState } from 'react';

import { BrowserRouter, Routes, Route, Navigate, Outlet } from 'react-router-dom';


import Login from "./components/Login.tsx";
import DashboardPage from './DashboardPage.tsx';

import './App.css';

interface Admin {
    authenticated: boolean;
    username: string;
}

function RedirectIfLoggedIn() {
    const [status, setStatus] = useState<"loading" | "authorized" | "unauthorized">("loading");
    const [admin, setAdmin] = useState<Admin | null>(null);

    useEffect(() => {
        const verifySession = async() => {
            try {
                const res = await fetch("/api/admin/me", {
                    method: "GET",
                    credentials: "include"
                });

                if (res.ok) {
                    const data: Admin = await res.json();
                    setAdmin(data);
                    setStatus("authorized");
                } else {
                    setStatus("unauthorized");
                }
            } catch {
                setStatus("unauthorized");
            }
        };
        verifySession();
    }, []);

    if (status == "loading") {
        return (<span>Verifying Session...</span>);
    }

    if (status == "unauthorized") {
        return <Outlet />;
    }

    return <Navigate to="/dashboard" replace />;
}

function ProtectedRoute() {

    const [status, setStatus] = useState<"loading" | "authorized" | "unauthorized">("loading");
    const [admin, setAdmin] = useState<Admin | null>(null);

    useEffect(() => {
        const verifySession = async() => {
            try {
                const res = await fetch("/api/admin/me", {
                    method: "GET",
                    credentials: "include"
                });

                if (res.ok) {
                    const data: Admin = await res.json();
                    setAdmin(data);
                    setStatus("authorized");
                } else {
                    setStatus("unauthorized");
                }
            } catch {
                setStatus("unauthorized");
            }
        };
        verifySession();
    }, []);

    if (status == "loading") {
        return (<span>Verifying Session...</span>);
    }

    if (status == "unauthorized") {
        return <Navigate to="/login" replace />;
    }

    return <Outlet context={admin}/>;
}

function LoginPage() {
    const [isSuccess, setIsSuccess] = useState<boolean>(false);
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

        setIsSuccess(true);
    };
    if(isSuccess) {
        return <Navigate to="/dashboard" replace />;
    }
    return (
        <div className="login-container">
            <Login onLogin={handleLogin} />
        </div>);
}


function App() {
	return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Navigate to="/login" replace />} />
                <Route element={<RedirectIfLoggedIn />}>
                    <Route path="/login" element={<LoginPage />} />
                </Route>
                <Route element={<ProtectedRoute />}>
                    <Route path="/dashboard" element={<DashboardPage />} />
                </Route>
            </Routes>
        </BrowserRouter>
	)
}

export default App;
