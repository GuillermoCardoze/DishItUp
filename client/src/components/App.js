import { useContext } from "react";
import { UserContext } from "./UserContext";
import Login from "./Login";

function App() {
    const { user, logout, loading } = useContext(UserContext);

    if (loading) return <h1>Loading...</h1>;

    return (
        <div>
            {user ? (
                <>
                    <h1>Welcome, {user.username}!</h1>
                    <button onClick={logout}>Logout</button>
                </>
            ) : (
                <Login />
            )}
        </div>
    );
}

export default App;
