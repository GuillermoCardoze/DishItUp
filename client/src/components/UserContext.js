import { createContext, useState, useEffect } from "react";

export const UserContext = createContext();

export function UserProvider({ children }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Check if user is already logged in
        fetch("/check_session")
            .then((res) => (res.ok ? res.json() : Promise.reject()))
            .then((data) => setUser(data))
            .catch(() => setUser(null))
            .finally(() => setLoading(false));
    }, []);

    function login(username, password) {
        return fetch("/signin", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password }),
        })
            .then((res) => (res.ok ? res.json() : Promise.reject("Invalid credentials")))
            .then((data) => setUser(data));
    }

    function logout() {
        return fetch("/logout", { method: "DELETE" }).then(() => setUser(null));
    }

    return (
        <UserContext.Provider value={{ user, login, logout, loading }}>
            {children}
        </UserContext.Provider>
    );
}
